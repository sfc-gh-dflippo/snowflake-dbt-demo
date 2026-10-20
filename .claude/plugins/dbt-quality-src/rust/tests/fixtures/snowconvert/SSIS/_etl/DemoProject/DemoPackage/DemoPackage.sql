CREATE OR REPLACE TASK public.demopackage
COMMENT = '{ "description": "", "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 2,  "minor": 42,  "patch": "5-Pr.112" }, "attributes": {  "component": "transact",  "convertedOn": "08/31/2026",  "domain": "no-domain-provided",  "migrationid": "JVqgAaCUXHqylxB0fSRFtA==" }}'
CONFIG = $${
  "package": {
    "User_CustomerName": {"value": "John", "type": "VARCHAR", "is_parameter": false}
  },
  "project": {
    "Project_Schema": {"value": "DBO", "type": "VARCHAR", "is_parameter": true},
    "Project_Database": {"value": "AdventureWorksDW2022", "type": "VARCHAR", "is_parameter": true},
    "Project_DimCustomerTable": {"value": "DIMCUSTOMER", "type": "VARCHAR", "is_parameter": true}
  }
}$$
AS
BEGIN
   LET config VARCHAR := SYSTEM$GET_TASK_GRAPH_CONFIG('package');
   LET project_config VARCHAR := SYSTEM$GET_TASK_GRAPH_CONFIG('project');
   LET scope VARCHAR := 'DemoPackage';
   CALL public.ClearVariables(:scope);
   CALL public.InitVariablesFromConfig(:scope, :config);
   CALL public.InitVariablesFromConfig(:scope, :project_config);
END;
CREATE OR REPLACE TASK public.demopackage_sequence_container
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.demopackage
AS
BEGIN
   CALL public.SetRunContext();
   LET User_CustomerName VARCHAR := public.GetControlVariableUDF('User_CustomerName', 'DemoPackage') :: VARCHAR;
   LET Project_Schema VARCHAR := public.GetControlVariableUDF('Project_Schema', 'Package') :: VARCHAR;
   LET Project_Database VARCHAR := public.GetControlVariableUDF('Project_Database', 'Package') :: VARCHAR;
   LET Project_DimCustomerTable VARCHAR := public.GetControlVariableUDF('Project_DimCustomerTable', 'Package') :: VARCHAR;
   ---- Start block 'Package\Sequence Container'
   ---- Start 'Package\Sequence Container\Data Flow Task'
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0007 - SSIS EXECUTABLE CONTAINS PROPERTY EXPRESSIONS that were not converted. ***/!!!
   LET dbt_vars_json VARCHAR := public.BuildDbtVarsJsonUDF('DemoPackage');
   LET full_args VARCHAR := 'build --target dev --vars ''' || dbt_vars_json || '''';
   EXECUTE DBT PROJECT public.Sequence_Container_Data_Flow_Task ARGS=:full_args;
   ---- Start 'Package\Sequence Container\Execute SQL Task 2'
   --** SSC-FDM-0007 - MISSING DEPENDENT OBJECT "dimCustomer" **
   SELECT
      *
   FROM
      dimCustomer
   WHERE
      FirstName = :User_CustomerName;
   ---- Start 'Package\Sequence Container\Execute SQL Task'
   CALL sp_columns();
   ---- Start 'Package\Sequence Container\Data Flow Task 2'
   LET dbt_vars_json VARCHAR := public.BuildDbtVarsJsonUDF('DemoPackage');
   LET full_args VARCHAR := 'build --target dev --vars ''' || dbt_vars_json || '''';
   EXECUTE DBT PROJECT public.Sequence_Container_Data_Flow_Task_2 ARGS=:full_args;
   ---- End block 'Package\Sequence Container'

   CALL public.UpdateControlVariable('User_CustomerName', 'DemoPackage', TO_VARIANT(:User_CustomerName));
END;

CREATE OR REPLACE TASK public.demopackage_sequence_container_2
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.demopackage_sequence_container
AS
BEGIN
   CALL public.SetRunContext();
   LET User_CustomerName VARCHAR := public.GetControlVariableUDF('User_CustomerName', 'DemoPackage') :: VARCHAR;
   LET Project_Schema VARCHAR := public.GetControlVariableUDF('Project_Schema', 'Package') :: VARCHAR;
   LET Project_Database VARCHAR := public.GetControlVariableUDF('Project_Database', 'Package') :: VARCHAR;
   LET Project_DimCustomerTable VARCHAR := public.GetControlVariableUDF('Project_DimCustomerTable', 'Package') :: VARCHAR;
   ---- Start block 'Package\Sequence Container 2'
   ---- Start 'Package\Sequence Container 2\Execute Process Task'
   !!!RESOLVE EWI!!! /*** SSC-EWI-SSIS0004 - SSIS CONTROL FLOW ELEMENT Microsoft.ExecuteProcess CANNOT BE CONVERTED TO SNOWFLAKE SCRIPTING. ***/!!!
   --<Executable ExecutableType="Microsoft.ExecuteProcess" refId="Package\Sequence Container 2\Execute Process Task" ThreadHint="0" LocaleID="-1" Description="Execute Process Task" DTSID="{EB5C4E2D-9AB2-4F5B-B465-A2D482C47647}" CreationName="Microsoft.ExecuteProcess" ObjectName="Execute Process Task" TaskContact="Execute Process Task;Microsoft Corporation; SQL Server 2022; © 2022 Microsoft Corporation; All Rights Reserved;http://www.microsoft.com/sql/support/default.asp;1">
   --  <EventHandlers />
   --</Executable>
   NULL;
   ---- End block 'Package\Sequence Container 2'

   CALL public.UpdateControlVariable('User_CustomerName', 'DemoPackage', TO_VARIANT(:User_CustomerName));
END;

