USE DATABASE AdventureWorksDW2022;

/* vAssocSeqOrders supports assocation and sequence clustering data mmining models.
      - Limits data to FY2004.
      - Creates order case table and line item nested table.*/
CREATE OR REPLACE VIEW dbo.vAssocSeqOrders
      COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
      AS
      SELECT DISTINCT
            OrderNumber,
            CustomerKey,
            Region,
            IncomeGroup
      FROM
            dbo.vDMPrep
      WHERE     (FiscalYear = '2013');