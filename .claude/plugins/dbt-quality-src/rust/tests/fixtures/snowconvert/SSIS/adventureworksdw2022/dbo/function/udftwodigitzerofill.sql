USE DATABASE AdventureWorksDW2022;

-- Converts the specified integer (which should be < 100 and > -1)
-- into a two character string, zero filling from the left 
-- if the number is < 10.
CREATE OR REPLACE FUNCTION dbo.udfTwoDigitZeroFill (NUMBER INT)
RETURNS CHAR(2)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
AS
$$
	DECLARE
		RESULT CHAR(2);
	BEGIN
		 
		IF (:NUMBER > 9) THEN
			RESULT := CAST(LEFT(:NUMBER, 2) AS CHAR(2));
		ELSE
			RESULT := CAST(LEFT('0' || CAST(:NUMBER AS VARCHAR), 2) AS CHAR(2));
		END IF;
		RETURN :RESULT;
	END;
$$;