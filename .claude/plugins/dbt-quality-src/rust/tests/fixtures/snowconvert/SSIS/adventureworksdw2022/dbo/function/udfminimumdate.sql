USE DATABASE AdventureWorksDW2022;

CREATE OR REPLACE FUNCTION dbo.udfMinimumDate (X TIMESTAMP_NTZ(3), Y TIMESTAMP_NTZ(3))
RETURNS TIMESTAMP_NTZ(3)
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "AFqgAYoc4nmXmiUg6NUuiQ==" }}'
AS
$$
    DECLARE
        Z TIMESTAMP_NTZ(3);
    BEGIN
         
        IF (:X <= :Y) THEN
            Z := :X;
        ELSE
            Z := :Y;
        END IF;
        RETURN (:Z);
    END;
$$;