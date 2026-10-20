CREATE OR REPLACE VIEW dbo.TaskSummary
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 46,  "patch": "0-Pr.305" }, "attributes": {  "component": "transact",  "convertedOn": "09/25/2026",  "domain": "no-domain-provided",  "migrationid": "PNugAcH15XaIL/Tn1HztAg==" }}'
AS
SELECT
    t.TaskID,
    t.Title,
    t.Priority,
    t.Status,
    t.CreatedAt,
    t.DueDate,
    e.FirstName || ' ' || e.LastName AS AssigneeName,
    e.Department,
    DATEDIFF(DAY, t.CreatedAt, NVL(t.CompletedAt, CURRENT_TIMESTAMP() :: TIMESTAMP)) AS AgeDays
FROM
    dbo.Tasks t
INNER JOIN
        dbo.Employees e
        ON t.AssigneeID = e.EmployeeID;