---
description: SQL Server
source_url: https://docs.snowflake.com/en/migrations/snowconvert-docs/translation-references/transact/transact-built-in-procedures
title: SnowConvert AI - SQL Server-Azure Synapse - Built-in procedures | Snowflake
---

## SP_ADDEXTENDEDPROPERTY_UDP[¶](#sp-addextendedproperty-udp)

Applies to

- SQL Server

### Description[¶](#description)

Adds a new extended property to a database object.

#### SQLServer syntax[¶](#sqlserver-syntax)

```
 sp_addextendedproperty
    [ @name = ] N'name'
    [ , [ @value = ] value ]
    [ , [ @level0type = ] 'level0type' ]
    [ , [ @level0name = ] N'level0name' ]
    [ , [ @level1type = ] 'level1type' ]
    [ , [ @level1name = ] N'level1name' ]
    [ , [ @level2type = ] 'level2type' ]
    [ , [ @level2name = ] N'level2name' ]
[ ; ]
```

Copy

### Custom UDP[¶](#custom-udp)

Keeps the same parameters as the original procedure

#### UDP[¶](#udp)

```
 -- <copyright file="SP_ADDEXTENDEDPROPERTY_UDP.sql" company="Snowflake Inc">
--        Copyright (c) 2019-2023 Snowflake Inc. All rights reserved.
-- </copyright>

-- =======================================================================================================
-- Description: The sp_addextendedproperty provides an equivalent functionality for adding extended
--              properties in Snowflake. This version is only supporting 'MS_Description' property to
--              add comments at schema/table/view/procedure/function level.
--              Comments on columns are only supported for tables.
--              If the name of the object includes double quotes, they need to be added as part of the
--              parameter values, for example level1name='"My_Col"'.

-- Parameters:
--   name:       Name of the extended property. 'MS_Description' is the only supported in this version.
--   value:      Value of the extended property. Cannot be null for 'MS_Description' property.
--   level0type: Type of level 0 object. SCHEMA is the only supported value in this version.
--   level0name: Value associated to the level 0 object.
--   level1type: Type of level 1 object. TABLE/VIEW/PROCEDURE/FUNCTION are the only supported values in this
--               version.
--   level1name: Value associated to the level 1 object.
--   level2type: Type of level 2 object. COLUMN is the only supported value in this version.
--   level2name: Value associated to the level 2 object.

-- Return:      This procedure returns a message with the result of the execution. If an exception occurs,
--              the exception is raised.
-- =======================================================================================================

CREATE OR REPLACE PROCEDURE SP_ADDEXTENDEDPROPERTY_UDP(
    name varchar,
    value varchar,
    level0type varchar DEFAULT '',
    level0name varchar DEFAULT '',
    level1type varchar DEFAULT '',
    level1name varchar DEFAULT '',
    level2type varchar DEFAULT '',
    level2name varchar DEFAULT '')

RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
   DECLARE  stmt VARCHAR;
            str_result VARCHAR;
BEGIN
    IF(lower(name) = 'ms_description') THEN --Comments on
        IF (value IS NOT NULL) THEN

            --Comment on table column
            IF(lower(level0type) = 'schema' and lower(level1type) = 'table' and lower(level2type) = 'column') THEN
                stmt := 'COMMENT ON COLUMN ' || level0name || '.' || level1name || '.' || level2name || ' IS ''' || value || ''';';

            --Comment on table/view/procedure/function
            ELSEIF(lower(level0type) = 'schema' and lower(level1type) in ('table', 'view', 'procedure', 'function') and level2type IS NULL) THEN
                stmt := 'COMMENT ON ' || upper(level1type) || ' ' || level0name || '.' || level1name || ' IS ''' || value || ''';';

            --Comment on schema
            ELSEIF(lower(level0type) = 'schema' and level1type IS NULL) THEN
                stmt := 'COMMENT ON ' || upper(level0type) || ' ' || level0name || ' IS ''' || value || ''';';

ELSE
                str_result := 'ERROR: COMMENT ON level0type: ' || level0type || ' | level1type: ' || nvl(level1type,'') || ' | level2type: ' || nvl(level2type,'') || ' is not supported yet.';
END IF;

            IF(stmt IS NOT NULL) THEN
                EXECUTE IMMEDIATE :stmt;
                str_result := name || ' extended property was successfully created.';
END IF;
ELSE
            str_result := 'ERROR: NULL value for COMMENT ON is not supported.';
END IF;
ELSE
        str_result := 'ERROR: ' || name || ' extended property is not supported yet.';
END IF;
RETURN str_result;
END;
```

Copy

##### SQL Server[¶](#sql-server)

```
 EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Technical identifier.' , @level0type=N'SCHEMA',@level0name=N'Monitoring', @level1type=N'TABLE',@level1name=N'tProcessingIssue', @level2type=N'COLUMN',@level2name=N'ID'
```

Copy

##### Snowflake[¶](#snowflake)

```
 CALL SP_ADDEXTENDEDPROPERTY_UDP('MS_Description', 'Technical identifier.', 'SCHEMA', 'Monitoring', 'TABLE', 'tProcessingIssue', 'COLUMN', 'ID');
```

Copy
