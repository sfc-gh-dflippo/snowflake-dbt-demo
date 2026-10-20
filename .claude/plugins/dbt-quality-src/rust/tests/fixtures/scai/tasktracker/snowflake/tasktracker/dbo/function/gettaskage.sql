CREATE OR REPLACE FUNCTION dbo.GetTaskAge (P_TASKID INT /*** SSC-FDM-TS0074 - PARAMETER '@TaskID' WAS RENAMED TO 'P_TASKID' BECAUSE ITS CONVERTED NAME CONFLICTS WITH ANOTHER IDENTIFIER IN THE FUNCTION ***/)
RETURNS INT
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 46,  "patch": "0-Pr.305" }, "attributes": {  "component": "transact",  "convertedOn": "09/25/2026",  "domain": "no-domain-provided",  "migrationid": "PNugAcH15XaIL/Tn1HztAg==" }}'
AS
$$
    WITH CTE1 AS
    (

        SELECT
            DATEDIFF(DAY, t.CreatedAt, NVL(t.CompletedAt, CURRENT_TIMESTAMP() :: TIMESTAMP)) AS AGE
        FROM
            dbo.Tasks t
        WHERE
            t.TaskID = P_TASKID
    )
    SELECT
        AGE
    FROM
        CTE1
$$;