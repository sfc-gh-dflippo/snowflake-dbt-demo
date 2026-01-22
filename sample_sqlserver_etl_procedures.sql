-- ============================================================================
-- SQL Server Stored Procedures for Loading Dimension and Fact Tables
-- Demonstrates common ETL/ELT patterns for data warehousing
-- ============================================================================

-- ============================================================================
-- DIMENSION LOAD: SCD Type 2 (Slowly Changing Dimension with History)
-- ============================================================================
CREATE OR ALTER PROCEDURE dbo.usp_Load_DimCustomer
    @BatchID INT = NULL,
    @RowsInserted INT OUTPUT,
    @RowsUpdated INT OUTPUT,
    @RowsExpired INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @CurrentDateTime DATETIME2 = SYSDATETIME();
    DECLARE @EndOfTime DATETIME2 = '9999-12-31';
    DECLARE @ErrorMessage NVARCHAR(4000);
    DECLARE @ErrorSeverity INT;
    DECLARE @ErrorState INT;

    -- Initialize output parameters
    SET @RowsInserted = 0;
    SET @RowsUpdated = 0;
    SET @RowsExpired = 0;

    BEGIN TRY
        BEGIN TRANSACTION;

        -- ====================================================================
        -- STEP 1: Expire existing records where source data has changed
        -- (SCD Type 2: Track history by expiring old records)
        -- ====================================================================
        UPDATE dim
        SET
            dim.EffectiveEndDate = @CurrentDateTime,
            dim.IsCurrent = 0,
            dim.UpdatedDate = @CurrentDateTime,
            dim.UpdatedBy = SYSTEM_USER
        FROM dbo.DimCustomer dim
        INNER JOIN staging.Customer src
            ON dim.CustomerBusinessKey = src.CustomerID
        WHERE dim.IsCurrent = 1
          AND (
              -- Check for changes in tracked attributes (Type 2)
              ISNULL(dim.CustomerName, '') <> ISNULL(src.CustomerName, '')
              OR ISNULL(dim.CustomerSegment, '') <> ISNULL(src.CustomerSegment, '')
              OR ISNULL(dim.Region, '') <> ISNULL(src.Region, '')
              OR ISNULL(dim.Country, '') <> ISNULL(src.Country, '')
          );

        SET @RowsExpired = @@ROWCOUNT;

        -- ====================================================================
        -- STEP 2: Insert new version of changed records (Type 2 history)
        -- ====================================================================
        INSERT INTO dbo.DimCustomer (
            CustomerBusinessKey,
            CustomerName,
            CustomerSegment,
            Region,
            Country,
            Email,
            Phone,
            EffectiveStartDate,
            EffectiveEndDate,
            IsCurrent,
            CreatedDate,
            CreatedBy
        )
        SELECT
            src.CustomerID AS CustomerBusinessKey,
            src.CustomerName,
            src.CustomerSegment,
            src.Region,
            src.Country,
            src.Email,
            src.Phone,
            @CurrentDateTime AS EffectiveStartDate,
            @EndOfTime AS EffectiveEndDate,
            1 AS IsCurrent,
            @CurrentDateTime AS CreatedDate,
            SYSTEM_USER AS CreatedBy
        FROM staging.Customer src
        INNER JOIN dbo.DimCustomer dim
            ON dim.CustomerBusinessKey = src.CustomerID
        WHERE dim.IsCurrent = 0
          AND dim.EffectiveEndDate = @CurrentDateTime  -- Just expired
          AND NOT EXISTS (
              -- Ensure we don't create duplicate current records
              SELECT 1 FROM dbo.DimCustomer x
              WHERE x.CustomerBusinessKey = src.CustomerID
                AND x.IsCurrent = 1
          );

        SET @RowsUpdated = @@ROWCOUNT;

        -- ====================================================================
        -- STEP 3: Insert brand new customers (never seen before)
        -- ====================================================================
        INSERT INTO dbo.DimCustomer (
            CustomerBusinessKey,
            CustomerName,
            CustomerSegment,
            Region,
            Country,
            Email,
            Phone,
            EffectiveStartDate,
            EffectiveEndDate,
            IsCurrent,
            CreatedDate,
            CreatedBy
        )
        SELECT
            src.CustomerID AS CustomerBusinessKey,
            src.CustomerName,
            src.CustomerSegment,
            src.Region,
            src.Country,
            src.Email,
            src.Phone,
            @CurrentDateTime AS EffectiveStartDate,
            @EndOfTime AS EffectiveEndDate,
            1 AS IsCurrent,
            @CurrentDateTime AS CreatedDate,
            SYSTEM_USER AS CreatedBy
        FROM staging.Customer src
        WHERE NOT EXISTS (
            SELECT 1 FROM dbo.DimCustomer dim
            WHERE dim.CustomerBusinessKey = src.CustomerID
        );

        SET @RowsInserted = @@ROWCOUNT;

        -- ====================================================================
        -- STEP 4: Update non-tracked attributes (SCD Type 1 - overwrite)
        -- ====================================================================
        UPDATE dim
        SET
            dim.Email = src.Email,
            dim.Phone = src.Phone,
            dim.UpdatedDate = @CurrentDateTime,
            dim.UpdatedBy = SYSTEM_USER
        FROM dbo.DimCustomer dim
        INNER JOIN staging.Customer src
            ON dim.CustomerBusinessKey = src.CustomerID
        WHERE dim.IsCurrent = 1
          AND (
              ISNULL(dim.Email, '') <> ISNULL(src.Email, '')
              OR ISNULL(dim.Phone, '') <> ISNULL(src.Phone, '')
          );

        COMMIT TRANSACTION;

        -- Log results
        PRINT 'DimCustomer Load Complete:';
        PRINT '  - Rows Inserted (New): ' + CAST(@RowsInserted AS VARCHAR(10));
        PRINT '  - Rows Updated (Type 2 New Version): ' + CAST(@RowsUpdated AS VARCHAR(10));
        PRINT '  - Rows Expired (Type 2 Old Version): ' + CAST(@RowsExpired AS VARCHAR(10));

    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;

        SET @ErrorMessage = ERROR_MESSAGE();
        SET @ErrorSeverity = ERROR_SEVERITY();
        SET @ErrorState = ERROR_STATE();

        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH;
END;
GO


-- ============================================================================
-- FACT TABLE LOAD: Incremental Load Pattern
-- ============================================================================
CREATE OR ALTER PROCEDURE dbo.usp_Load_FactSales
    @LoadDate DATE = NULL,
    @RowsInserted INT OUTPUT,
    @RowsUpdated INT OUTPUT,
    @RowsDeleted INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @CurrentDateTime DATETIME2 = SYSDATETIME();
    DECLARE @ErrorMessage NVARCHAR(4000);
    DECLARE @ErrorSeverity INT;
    DECLARE @ErrorState INT;
    DECLARE @MinOrderDate DATE;
    DECLARE @MaxOrderDate DATE;

    -- Default to yesterday if no date specified
    SET @LoadDate = ISNULL(@LoadDate, DATEADD(DAY, -1, CAST(GETDATE() AS DATE)));

    -- Initialize output parameters
    SET @RowsInserted = 0;
    SET @RowsUpdated = 0;
    SET @RowsDeleted = 0;

    BEGIN TRY
        BEGIN TRANSACTION;

        -- ====================================================================
        -- STEP 1: Identify date range from staging data
        -- ====================================================================
        SELECT
            @MinOrderDate = MIN(OrderDate),
            @MaxOrderDate = MAX(OrderDate)
        FROM staging.SalesOrder
        WHERE OrderDate >= @LoadDate;

        IF @MinOrderDate IS NULL
        BEGIN
            PRINT 'No data to process for date: ' + CAST(@LoadDate AS VARCHAR(10));
            COMMIT TRANSACTION;
            RETURN;
        END;

        -- ====================================================================
        -- STEP 2: Delete existing facts for the date range (idempotent reload)
        -- This allows re-running the same load without duplicates
        -- ====================================================================
        DELETE FROM dbo.FactSales
        WHERE OrderDateKey IN (
            SELECT DateKey FROM dbo.DimDate
            WHERE FullDate BETWEEN @MinOrderDate AND @MaxOrderDate
        );

        SET @RowsDeleted = @@ROWCOUNT;

        -- ====================================================================
        -- STEP 3: Insert new/updated facts with dimension key lookups
        -- ====================================================================
        INSERT INTO dbo.FactSales (
            -- Dimension Keys (Surrogate Keys)
            OrderDateKey,
            ShipDateKey,
            CustomerKey,
            ProductKey,
            StoreKey,

            -- Degenerate Dimensions
            OrderNumber,
            OrderLineNumber,

            -- Measures
            Quantity,
            UnitPrice,
            UnitCost,
            DiscountAmount,
            SalesAmount,
            CostAmount,
            GrossProfit,

            -- Audit Columns
            SourceSystemKey,
            LoadDate,
            BatchID
        )
        SELECT
            -- ================================================================
            -- Dimension Key Lookups (with unknown member handling)
            -- ================================================================
            COALESCE(dd_order.DateKey, -1) AS OrderDateKey,
            COALESCE(dd_ship.DateKey, -1) AS ShipDateKey,
            COALESCE(dc.CustomerKey, -1) AS CustomerKey,
            COALESCE(dp.ProductKey, -1) AS ProductKey,
            COALESCE(ds.StoreKey, -1) AS StoreKey,

            -- Degenerate Dimensions (stored directly in fact)
            src.OrderNumber,
            src.OrderLineNumber,

            -- ================================================================
            -- Measures (calculated and sourced)
            -- ================================================================
            src.Quantity,
            src.UnitPrice,
            src.UnitCost,
            src.DiscountAmount,

            -- Sales Amount = (Quantity * UnitPrice) - Discount
            (src.Quantity * src.UnitPrice) - ISNULL(src.DiscountAmount, 0) AS SalesAmount,

            -- Cost Amount = Quantity * UnitCost
            src.Quantity * src.UnitCost AS CostAmount,

            -- Gross Profit = Sales - Cost
            ((src.Quantity * src.UnitPrice) - ISNULL(src.DiscountAmount, 0))
                - (src.Quantity * src.UnitCost) AS GrossProfit,

            -- ================================================================
            -- Audit Trail
            -- ================================================================
            src.SourceOrderID AS SourceSystemKey,
            @CurrentDateTime AS LoadDate,
            src.BatchID

        FROM staging.SalesOrder src

        -- ====================================================================
        -- Dimension Lookups using LEFT JOINs
        -- ====================================================================

        -- Order Date lookup
        LEFT JOIN dbo.DimDate dd_order
            ON dd_order.FullDate = src.OrderDate

        -- Ship Date lookup
        LEFT JOIN dbo.DimDate dd_ship
            ON dd_ship.FullDate = src.ShipDate

        -- Customer lookup (point-in-time for SCD Type 2)
        LEFT JOIN dbo.DimCustomer dc
            ON dc.CustomerBusinessKey = src.CustomerID
            AND dc.IsCurrent = 1  -- Use current version
            -- Alternative: Point-in-time lookup
            -- AND src.OrderDate BETWEEN dc.EffectiveStartDate AND dc.EffectiveEndDate

        -- Product lookup
        LEFT JOIN dbo.DimProduct dp
            ON dp.ProductBusinessKey = src.ProductID
            AND dp.IsCurrent = 1

        -- Store lookup
        LEFT JOIN dbo.DimStore ds
            ON ds.StoreBusinessKey = src.StoreID
            AND ds.IsCurrent = 1

        -- ====================================================================
        -- Filter to specified date range
        -- ====================================================================
        WHERE src.OrderDate BETWEEN @MinOrderDate AND @MaxOrderDate;

        SET @RowsInserted = @@ROWCOUNT;

        -- ====================================================================
        -- STEP 4: Log orphaned records (failed dimension lookups)
        -- ====================================================================
        INSERT INTO audit.FactLoadOrphans (
            TableName,
            SourceKey,
            OrphanType,
            OrphanValue,
            LoadDate
        )
        SELECT DISTINCT
            'FactSales' AS TableName,
            src.SourceOrderID AS SourceKey,
            'Customer' AS OrphanType,
            src.CustomerID AS OrphanValue,
            @CurrentDateTime AS LoadDate
        FROM staging.SalesOrder src
        LEFT JOIN dbo.DimCustomer dc
            ON dc.CustomerBusinessKey = src.CustomerID
            AND dc.IsCurrent = 1
        WHERE src.OrderDate BETWEEN @MinOrderDate AND @MaxOrderDate
          AND dc.CustomerKey IS NULL
          AND src.CustomerID IS NOT NULL;

        COMMIT TRANSACTION;

        -- Log results
        PRINT 'FactSales Load Complete for ' + CAST(@LoadDate AS VARCHAR(10)) + ':';
        PRINT '  - Date Range: ' + CAST(@MinOrderDate AS VARCHAR(10)) + ' to ' + CAST(@MaxOrderDate AS VARCHAR(10));
        PRINT '  - Rows Deleted (Pre-existing): ' + CAST(@RowsDeleted AS VARCHAR(10));
        PRINT '  - Rows Inserted: ' + CAST(@RowsInserted AS VARCHAR(10));

    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;

        SET @ErrorMessage = ERROR_MESSAGE();
        SET @ErrorSeverity = ERROR_SEVERITY();
        SET @ErrorState = ERROR_STATE();

        -- Log error
        INSERT INTO audit.ETLErrorLog (
            ProcedureName,
            ErrorMessage,
            ErrorSeverity,
            ErrorState,
            ErrorDate
        )
        VALUES (
            'usp_Load_FactSales',
            @ErrorMessage,
            @ErrorSeverity,
            @ErrorState,
            @CurrentDateTime
        );

        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH;
END;
GO


-- ============================================================================
-- MASTER ETL ORCHESTRATION PROCEDURE
-- ============================================================================
CREATE OR ALTER PROCEDURE dbo.usp_ExecuteDailyETL
    @LoadDate DATE = NULL
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @StartTime DATETIME2 = SYSDATETIME();
    DECLARE @BatchID INT;
    DECLARE @DimInserted INT, @DimUpdated INT, @DimExpired INT;
    DECLARE @FactInserted INT, @FactUpdated INT, @FactDeleted INT;

    -- Create batch record
    INSERT INTO audit.ETLBatch (StartTime, Status)
    VALUES (@StartTime, 'Running');

    SET @BatchID = SCOPE_IDENTITY();

    BEGIN TRY
        -- ================================================================
        -- Load Dimensions First (order matters for referential integrity)
        -- ================================================================
        PRINT '=== Loading Dimensions ===';

        EXEC dbo.usp_Load_DimCustomer
            @BatchID = @BatchID,
            @RowsInserted = @DimInserted OUTPUT,
            @RowsUpdated = @DimUpdated OUTPUT,
            @RowsExpired = @DimExpired OUTPUT;

        -- Add other dimension loads here...
        -- EXEC dbo.usp_Load_DimProduct ...
        -- EXEC dbo.usp_Load_DimStore ...

        -- ================================================================
        -- Load Facts After Dimensions
        -- ================================================================
        PRINT '=== Loading Facts ===';

        EXEC dbo.usp_Load_FactSales
            @LoadDate = @LoadDate,
            @RowsInserted = @FactInserted OUTPUT,
            @RowsUpdated = @FactUpdated OUTPUT,
            @RowsDeleted = @FactDeleted OUTPUT;

        -- Update batch record
        UPDATE audit.ETLBatch
        SET
            EndTime = SYSDATETIME(),
            Status = 'Success',
            DimensionRowsProcessed = @DimInserted + @DimUpdated,
            FactRowsProcessed = @FactInserted
        WHERE BatchID = @BatchID;

        PRINT '=== ETL Complete ===';

    END TRY
    BEGIN CATCH
        UPDATE audit.ETLBatch
        SET
            EndTime = SYSDATETIME(),
            Status = 'Failed',
            ErrorMessage = ERROR_MESSAGE()
        WHERE BatchID = @BatchID;

        THROW;
    END CATCH;
END;
GO


-- ============================================================================
-- USAGE EXAMPLES
-- ============================================================================

-- Execute full daily ETL
-- EXEC dbo.usp_ExecuteDailyETL @LoadDate = '2024-01-15';

-- Load just the dimension
-- DECLARE @Ins INT, @Upd INT, @Exp INT;
-- EXEC dbo.usp_Load_DimCustomer @RowsInserted = @Ins OUT, @RowsUpdated = @Upd OUT, @RowsExpired = @Exp OUT;
-- SELECT @Ins AS Inserted, @Upd AS Updated, @Exp AS Expired;

-- Load just the fact table
-- DECLARE @Ins INT, @Upd INT, @Del INT;
-- EXEC dbo.usp_Load_FactSales @LoadDate = '2024-01-15', @RowsInserted = @Ins OUT, @RowsUpdated = @Upd OUT, @RowsDeleted = @Del OUT;
-- SELECT @Ins AS Inserted, @Upd AS Updated, @Del AS Deleted;
