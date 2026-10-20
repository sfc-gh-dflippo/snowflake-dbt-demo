USE DATABASE SampleStoreDB;

CREATE OR REPLACE TABLE Store.OrderDetails (
    OrderDetailID INT IDENTITY(1,1) ORDER NOT NULL,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(18, 2) NOT NULL,
    Discount DECIMAL(5, 2) NULL DEFAULT ((0)),
    CreatedDate TIMESTAMP_NTZ(3) NULL DEFAULT (CURRENT_TIMESTAMP() :: TIMESTAMP_NTZ(3))
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 10,  "patch": "0" }, "attributes": {  "component": "transact",  "convertedOn": "02/26/2026",  "domain": "no-domain-provided",  "migrationid": "j5ucAW36yneHx8K6CNvJhw==" }}'
;