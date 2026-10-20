USE DATABASE AdventureWorksDW2022;

-- vTimeSeries view supports the creation of time series data mining models.
--      - Replaces earlier bike models with successor models.
--      - Abbreviates model names to improve readability in mining model viewer
--      - Concatenates model and region so that table only has one input.
--      - Creates a date field indexed to monthly reporting date for use in prediction.
CREATE OR REPLACE VIEW dbo.vTimeSeries
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
AS
SELECT
    CASE
    	Model
        WHEN 'Mountain-100' THEN 'M200'
        WHEN 'Road-150' THEN 'R250'
        WHEN 'Road-650' THEN 'R750'
        WHEN 'Touring-1000' THEN 'T1000'
        ELSE LEFT(Model, 1) || RIGHT(Model, 3)
    END || ' ' || Region AS ModelRegion
    ,(CAST(CalendarYear AS INTEGER) * 100) + CAST(Month AS INTEGER) AS TimeIndex
    ,
    SUM(Quantity) AS Quantity
    ,
    SUM(Amount) AS Amount
,
    CalendarYear
,
    Month
,
    -- SSC-EWI-0067 inlined: udfBuildISO8601Date logic expanded (procedure cannot be called in a query)
    TO_TIMESTAMP_NTZ(CAST(CalendarYear AS VARCHAR) || '-' || LPAD(CAST(Month AS VARCHAR), 2, '0') || '-25T00:00:00') as ReportingDate
FROM
    dbo.vDMPrep
WHERE
    Model IN ('Mountain-100', 'Mountain-200', 'Road-150', 'Road-250',
        'Road-650', 'Road-750', 'Touring-1000')
GROUP BY
    CASE
    	Model
        WHEN 'Mountain-100' THEN 'M200'
        WHEN 'Road-150' THEN 'R250'
        WHEN 'Road-650' THEN 'R750'
        WHEN 'Touring-1000' THEN 'T1000'
        ELSE LEFT(Model,1) || RIGHT(Model,3)
    END || ' ' || Region
    ,(CAST(CalendarYear AS INTEGER) * 100) + CAST(Month AS INTEGER)
,
    CalendarYear
,
    Month
,
    TO_TIMESTAMP_NTZ(CAST(CalendarYear AS VARCHAR) || '-' || LPAD(CAST(Month AS VARCHAR), 2, '0') || '-25T00:00:00');