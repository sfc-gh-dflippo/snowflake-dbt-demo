CREATE OR REPLACE PROCEDURE dbo.GetEmployeeWorkload (DEPARTMENT STRING DEFAULT NULL)
RETURNS TABLE()
LANGUAGE SQL
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 46,  "patch": "0-Pr.305" }, "attributes": {  "component": "transact",  "convertedOn": "09/25/2026",  "domain": "no-domain-provided",  "migrationid": "PNugAcH15XaIL/Tn1HztAg==" }}'
EXECUTE AS CALLER
AS
$$
    DECLARE
        ProcedureResultSet RESULTSET;
    BEGIN
--        --** SSC-FDM-TS0029 - SET NOCOUNT STATEMENT IS COMMENTED OUT, WHICH IS NOT APPLICABLE IN SNOWFLAKE. **
--        SET NOCOUNT ON;
        ProcedureResultSet := (
        SELECT
            AssigneeName,
            Department,
            COUNT(*) AS TotalTasks,
            SUM(CASE WHEN Status = 'Open' THEN 1 ELSE 0 END) AS OpenTasks,
            SUM(CASE WHEN Status = 'In Progress' THEN 1 ELSE 0 END) AS InProgressTasks,
            SUM(CASE WHEN Status = 'Done' THEN 1 ELSE 0 END) AS DoneTasks,
            AVG(AgeDays) AS AvgAgeDays
        FROM
            dbo.TaskSummary
        WHERE
            :DEPARTMENT IS NULL OR Department = :DEPARTMENT
        GROUP BY
            AssigneeName,
            Department
        ORDER BY OpenTasks DESC);
        RETURN TABLE(ProcedureResultSet);
    END;
$$;