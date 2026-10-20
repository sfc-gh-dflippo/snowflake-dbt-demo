USE DATABASE AdventureWorksDW2022;

-- ******************************************************
-- Create User Defined Functions
-- ******************************************************
-- Builds an ISO 8601 format date from a year, month, and day specified as integers.
-- This format of date should parse correctly regardless of SET DATEFORMAT and SET LANGUAGE.
-- See SQL Server Books Online for more details.
-- SSC-EWI-0068: UDF converted to PROCEDURE (calls udfTwoDigitZeroFill which is a UDF)
CREATE OR REPLACE PROCEDURE dbo.udfBuildISO8601Date (YEAR INT, MONTH INT, DAY INT)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
EXECUTE AS CALLER
AS
$$
	BEGIN
		RETURN TO_TIMESTAMP_NTZ(CAST(:YEAR AS VARCHAR) || '-' || dbo.udfTwoDigitZeroFill(:MONTH) || '-' || dbo.udfTwoDigitZeroFill(:DAY) || 'T00:00:00');
	END;
$$;