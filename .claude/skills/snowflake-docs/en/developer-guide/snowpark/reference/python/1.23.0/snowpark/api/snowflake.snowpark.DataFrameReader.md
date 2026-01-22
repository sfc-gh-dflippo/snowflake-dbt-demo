---
auto_generated: true
description: 'Bases: object'
last_scraped: '2026-01-14T16:54:46.115581+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrameReader
title: snowflake.snowpark.DataFrameReader | Snowflake Documentation
---

1.44.0 (latest)1.43.01.42.01.41.01.40.01.39.11.39.01.38.01.37.01.35.01.34.01.33.01.32.01.31.01.30.01.29.11.29.01.28.01.27.01.26.01.25.01.24.01.23.01.22.11.21.11.21.01.20.01.19.01.18.01.17.01.16.01.15.01.14.01.13.01.12.11.12.01.11.11.10.01.9.01.8.01.7.01.6.11.5.01.4.01.3.01.2.01.1.0

1. [Overview](../../index.md)
2. [Snowpark Session](../session.md)
3. [Snowpark APIs](../index.md)

   * [Input/Output](../io.md)

     + [DataFrameReader](snowflake.snowpark.DataFrameReader.md)
     + [DataFrameWriter](snowflake.snowpark.DataFrameWriter.md)
     + [FileOperation](snowflake.snowpark.FileOperation.md)
     + [PutResult](snowflake.snowpark.PutResult.md)
     + [GetResult](snowflake.snowpark.GetResult.md)
     + [DataFrameReader.avro](snowflake.snowpark.DataFrameReader.avro.md)
     + [DataFrameReader.csv](snowflake.snowpark.DataFrameReader.csv.md)
     + [DataFrameReader.json](snowflake.snowpark.DataFrameReader.json.md)
     + [DataFrameReader.option](snowflake.snowpark.DataFrameReader.option.md)
     + [DataFrameReader.options](snowflake.snowpark.DataFrameReader.options.md)
     + [DataFrameReader.orc](snowflake.snowpark.DataFrameReader.orc.md)
     + [DataFrameReader.parquet](snowflake.snowpark.DataFrameReader.parquet.md)
     + [DataFrameReader.schema](snowflake.snowpark.DataFrameReader.schema.md)
     + [DataFrameReader.table](snowflake.snowpark.DataFrameReader.table.md)
     + [DataFrameReader.with\_metadata](snowflake.snowpark.DataFrameReader.with_metadata.md)
     + [DataFrameReader.xml](snowflake.snowpark.DataFrameReader.xml.md)
     + [DataFrameWriter.copy\_into\_location](snowflake.snowpark.DataFrameWriter.copy_into_location.md)
     + [DataFrameWriter.mode](snowflake.snowpark.DataFrameWriter.mode.md)
     + [DataFrameWriter.saveAsTable](snowflake.snowpark.DataFrameWriter.saveAsTable.md)
     + [DataFrameWriter.save\_as\_table](snowflake.snowpark.DataFrameWriter.save_as_table.md)
     + [DataFrameWriter.csv](snowflake.snowpark.DataFrameWriter.csv.md)
     + [DataFrameWriter.json](snowflake.snowpark.DataFrameWriter.json.md)
     + [DataFrameWriter.parquet](snowflake.snowpark.DataFrameWriter.parquet.md)
     + [FileOperation.get](snowflake.snowpark.FileOperation.get.md)
     + [FileOperation.get\_stream](snowflake.snowpark.FileOperation.get_stream.md)
     + [FileOperation.put](snowflake.snowpark.FileOperation.put.md)
     + [FileOperation.put\_stream](snowflake.snowpark.FileOperation.put_stream.md)
     + [PutResult.count](snowflake.snowpark.PutResult.count.md)
     + [PutResult.index](snowflake.snowpark.PutResult.index.md)
     + [GetResult.count](snowflake.snowpark.GetResult.count.md)
     + [GetResult.index](snowflake.snowpark.GetResult.index.md)
     + [PutResult.message](snowflake.snowpark.PutResult.message.md)
     + [PutResult.source](snowflake.snowpark.PutResult.source.md)
     + [PutResult.source\_compression](snowflake.snowpark.PutResult.source_compression.md)
     + [PutResult.source\_size](snowflake.snowpark.PutResult.source_size.md)
     + [PutResult.status](snowflake.snowpark.PutResult.status.md)
     + [PutResult.target](snowflake.snowpark.PutResult.target.md)
     + [PutResult.target\_compression](snowflake.snowpark.PutResult.target_compression.md)
     + [PutResult.target\_size](snowflake.snowpark.PutResult.target_size.md)
     + [GetResult.file](snowflake.snowpark.GetResult.file.md)
     + [GetResult.message](snowflake.snowpark.GetResult.message.md)
     + [GetResult.size](snowflake.snowpark.GetResult.size.md)
     + [GetResult.status](snowflake.snowpark.GetResult.status.md)
   * [DataFrame](../dataframe.md)
   * [Column](../column.md)
   * [Data Types](../types.md)
   * [Row](../row.md)
   * [Functions](../functions.md)
   * [Window](../window.md)
   * [Grouping](../grouping.md)
   * [Table Function](../table_function.md)
   * [Table](../table.md)
   * [AsyncJob](../async_job.md)
   * [Stored Procedures](../stored_procedures.md)
   * [User-Defined Functions](../udf.md)
   * [User-Defined Aggregate Functions](../udaf.md)
   * [User-Defined Table Functions](../udtf.md)
   * [Observability](../observability.md)
   * [Files](../files.md)
   * [LINEAGE](../lineage.md)
   * [Context](../context.md)
   * [Exceptions](../exceptions.md)
   * [Testing](../testing.md)
4. [Snowpark pandas API](../../modin/index.md)

[Developer](../../../../../../../developer.md)[Snowpark API](../../../../../index.md)[Python](../../../../../python/index.md)[Python API Reference](../../index.md)[Snowpark APIs](../index.md)[Input/Output](../io.md)DataFrameReader

You are viewing documentation about an older version (1.23.0).  [View latest version](../../../1.44.0/index.md)

# snowflake.snowpark.DataFrameReader[¶](#snowflake-snowpark-dataframereader "Permalink to this heading")

*class* snowflake.snowpark.DataFrameReader(*session: [Session](snowflake.snowpark.Session.html#snowflake.snowpark.Session "snowflake.snowpark.session.Session")*)[[source]](https://github.com/snowflakedb/snowpark-python/blob/v1.23.0/src/snowflake/snowpark/dataframe_reader.py#L62-L763)[¶](#snowflake.snowpark.DataFrameReader "Permalink to this definition")
:   Bases: `object`

    Provides methods to load data in various supported formats from a Snowflake
    stage to a [`DataFrame`](snowflake.snowpark.DataFrame.html#snowflake.snowpark.DataFrame "snowflake.snowpark.DataFrame"). The paths provided to the DataFrameReader must refer
    to Snowflake stages.

    To use this object:

    1. Access an instance of a [`DataFrameReader`](#snowflake.snowpark.DataFrameReader "snowflake.snowpark.DataFrameReader") by using the
    [`Session.read`](snowflake.snowpark.Session.read.html#snowflake.snowpark.Session.read "snowflake.snowpark.Session.read") property.

    2. Specify any [format-specific options](https://docs.snowflake.com/en/sql-reference/sql/create-file-format.html#format-type-options-formattypeoptions) and [copy options](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table.html#copy-options-copyoptions)
    by calling the [`option()`](snowflake.snowpark.DataFrameReader.option.html#snowflake.snowpark.DataFrameReader.option "snowflake.snowpark.DataFrameReader.option") or [`options()`](snowflake.snowpark.DataFrameReader.options.html#snowflake.snowpark.DataFrameReader.options "snowflake.snowpark.DataFrameReader.options") method. These methods return a
    DataFrameReader that is configured with these options. (Note that although
    specifying copy options can make error handling more robust during the reading
    process, it may have an effect on performance.)

    3. Specify the schema of the data that you plan to load by constructing a
    [`types.StructType`](snowflake.snowpark.types.StructType.html#snowflake.snowpark.types.StructType "snowflake.snowpark.types.StructType") object and passing it to the [`schema()`](snowflake.snowpark.DataFrameReader.schema.html#snowflake.snowpark.DataFrameReader.schema "snowflake.snowpark.DataFrameReader.schema") method if the file format is CSV. Other file
    formats such as JSON, XML, Parquet, ORC, and AVRO don’t accept a schema.
    This method returns a [`DataFrameReader`](#snowflake.snowpark.DataFrameReader "snowflake.snowpark.DataFrameReader") that is configured to read data that uses the specified schema.
    Currently, inferring schema is also supported for CSV and JSON formats as a preview feature open to all accounts.

    4. Specify the format of the data by calling the method named after the format
    (e.g. [`csv()`](snowflake.snowpark.DataFrameReader.csv.html#snowflake.snowpark.DataFrameReader.csv "snowflake.snowpark.DataFrameReader.csv"), [`json()`](snowflake.snowpark.DataFrameReader.json.html#snowflake.snowpark.DataFrameReader.json "snowflake.snowpark.DataFrameReader.json"), etc.). These methods return a [`DataFrame`](snowflake.snowpark.DataFrame.html#snowflake.snowpark.DataFrame "snowflake.snowpark.DataFrame")
    that is configured to load data in the specified format.

    5. Call a [`DataFrame`](snowflake.snowpark.DataFrame.html#snowflake.snowpark.DataFrame "snowflake.snowpark.DataFrame") method that performs an action (e.g.
    [`DataFrame.collect()`](snowflake.snowpark.DataFrame.collect.html#snowflake.snowpark.DataFrame.collect "snowflake.snowpark.DataFrame.collect")) to load the data from the file.

    The following examples demonstrate how to use a DataFrameReader.
    :   ```
        >>> # Create a temp stage to run the example code.
        >>> _ = session.sql("CREATE or REPLACE temp STAGE mystage").collect()
        ```

        Copy

    Example 1:
    :   Loading the first two columns of a CSV file and skipping the first header line:

        ```
        >>> from snowflake.snowpark.types import StructType, StructField, IntegerType, StringType, FloatType
        >>> _ = session.file.put("tests/resources/testCSV.csv", "@mystage", auto_compress=False)
        >>> # Define the schema for the data in the CSV file.
        >>> user_schema = StructType([StructField("a", IntegerType()), StructField("b", StringType()), StructField("c", FloatType())])
        >>> # Create a DataFrame that is configured to load data from the CSV file.
        >>> df = session.read.options({"field_delimiter": ",", "skip_header": 1}).schema(user_schema).csv("@mystage/testCSV.csv")
        >>> # Load the data into the DataFrame and return an array of rows containing the results.
        >>> df.collect()
        [Row(A=2, B='two', C=2.2)]
        ```

        Copy

    Example 2:
    :   Loading a gzip compressed json file:

        ```
        >>> _ = session.file.put("tests/resources/testJson.json", "@mystage", auto_compress=True)
        >>> # Create a DataFrame that is configured to load data from the gzipped JSON file.
        >>> json_df = session.read.option("compression", "gzip").json("@mystage/testJson.json.gz")
        >>> # Load the data into the DataFrame and return an array of rows containing the results.
        >>> json_df.show()
        -----------------------
        |"$1"                 |
        -----------------------
        |{                    |
        |  "color": "Red",    |
        |  "fruit": "Apple",  |
        |  "size": "Large"    |
        |}                    |
        -----------------------
        ```

        Copy

    In addition, if you want to load only a subset of files from the stage, you can use the
    [pattern](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table.html#loading-using-pattern-matching)
    option to specify a regular expression that matches the files that you want to load.

    Example 3:
    :   Loading only the CSV files from a stage location:

        ```
        >>> from snowflake.snowpark.types import StructType, StructField, IntegerType, StringType
        >>> from snowflake.snowpark.functions import col
        >>> _ = session.file.put("tests/resources/*.csv", "@mystage", auto_compress=False)
        >>> # Define the schema for the data in the CSV files.
        >>> user_schema = StructType([StructField("a", IntegerType()), StructField("b", StringType()), StructField("c", FloatType())])
        >>> # Create a DataFrame that is configured to load data from the CSV files in the stage.
        >>> csv_df = session.read.option("pattern", ".*V[.]csv").schema(user_schema).csv("@mystage").sort(col("a"))
        >>> # Load the data into the DataFrame and return an array of rows containing the results.
        >>> csv_df.collect()
        [Row(A=1, B='one', C=1.2), Row(A=2, B='two', C=2.2), Row(A=3, B='three', C=3.3), Row(A=4, B='four', C=4.4)]
        ```

        Copy

    To load Parquet, ORC and AVRO files, no schema is accepted because the schema will be automatically inferred.
    Inferring the schema can be disabled by setting option “infer\_schema” to `False`. Then you can use `$1` to access
    the column data as an OBJECT.

    Example 4:
    :   Loading a Parquet file with inferring the schema.
        :   ```
            >>> from snowflake.snowpark.functions import col
            >>> _ = session.file.put("tests/resources/test.parquet", "@mystage", auto_compress=False)
            >>> # Create a DataFrame that uses a DataFrameReader to load data from a file in a stage.
            >>> df = session.read.parquet("@mystage/test.parquet").where(col('"num"') == 2)
            >>> # Load the data into the DataFrame and return an array of rows containing the results.
            >>> df.collect()
            [Row(str='str2', num=2)]
            ```

            Copy

    Example 5:
    :   Loading an ORC file and infer the schema:
        :   ```
            >>> from snowflake.snowpark.functions import col
            >>> _ = session.file.put("tests/resources/test.orc", "@mystage", auto_compress=False)
            >>> # Create a DataFrame that uses a DataFrameReader to load data from a file in a stage.
            >>> df = session.read.orc("@mystage/test.orc").where(col('"num"') == 2)
            >>> # Load the data into the DataFrame and return an array of rows containing the results.
            >>> df.collect()
            [Row(str='str2', num=2)]
            ```

            Copy

    Example 6:
    :   Loading an AVRO file and infer the schema:
        :   ```
            >>> from snowflake.snowpark.functions import col
            >>> _ = session.file.put("tests/resources/test.avro", "@mystage", auto_compress=False)
            >>> # Create a DataFrame that uses a DataFrameReader to load data from a file in a stage.
            >>> df = session.read.avro("@mystage/test.avro").where(col('"num"') == 2)
            >>> # Load the data into the DataFrame and return an array of rows containing the results.
            >>> df.collect()
            [Row(str='str2', num=2)]
            ```

            Copy

    Example 7:
    :   Loading a Parquet file without inferring the schema:
        :   ```
            >>> from snowflake.snowpark.functions import col
            >>> _ = session.file.put("tests/resources/test.parquet", "@mystage", auto_compress=False)
            >>> # Create a DataFrame that uses a DataFrameReader to load data from a file in a stage.
            >>> df = session.read.option("infer_schema", False).parquet("@mystage/test.parquet").where(col('$1')["num"] == 2)
            >>> # Load the data into the DataFrame and return an array of rows containing the results.
            >>> df.show()
            -------------------
            |"$1"             |
            -------------------
            |{                |
            |  "num": 2,      |
            |  "str": "str2"  |
            |}                |
            -------------------
            ```

            Copy

    Loading JSON and XML files doesn’t support schema either. You also need to use `$1` to access the column data as an OBJECT.

    Example 8:
    :   Loading a JSON file:
        :   ```
            >>> from snowflake.snowpark.functions import col, lit
            >>> _ = session.file.put("tests/resources/testJson.json", "@mystage", auto_compress=False)
            >>> # Create a DataFrame that uses a DataFrameReader to load data from a file in a stage.
            >>> df = session.read.json("@mystage/testJson.json").where(col("$1")["fruit"] == lit("Apple"))
            >>> # Load the data into the DataFrame and return an array of rows containing the results.
            >>> df.show()
            -----------------------
            |"$1"                 |
            -----------------------
            |{                    |
            |  "color": "Red",    |
            |  "fruit": "Apple",  |
            |  "size": "Large"    |
            |}                    |
            |{                    |
            |  "color": "Red",    |
            |  "fruit": "Apple",  |
            |  "size": "Large"    |
            |}                    |
            -----------------------
            ```

            Copy

    Example 9:
    :   Loading an XML file:
        :   ```
            >>> _ = session.file.put("tests/resources/test.xml", "@mystage", auto_compress=False)
            >>> # Create a DataFrame that uses a DataFrameReader to load data from a file in a stage.
            >>> df = session.read.xml("@mystage/test.xml")
            >>> # Load the data into the DataFrame and return an array of rows containing the results.
            >>> df.show()
            ---------------------
            |"$1"               |
            ---------------------
            |<test>             |
            |  <num>1</num>     |
            |  <str>str1</str>  |
            |</test>            |
            |<test>             |
            |  <num>2</num>     |
            |  <str>str2</str>  |
            |</test>            |
            ---------------------
            ```

            Copy

    Example 10:
    :   Loading a CSV file with an already existing FILE\_FORMAT:
        :   ```
            >>> from snowflake.snowpark.types import StructType, StructField, IntegerType, StringType
            >>> _ = session.sql("create file format if not exists csv_format type=csv skip_header=1 null_if='none';").collect()
            >>> _ = session.file.put("tests/resources/testCSVspecialFormat.csv", "@mystage", auto_compress=False)
            >>> # Define the schema for the data in the CSV files.
            >>> schema = StructType([StructField("ID", IntegerType()),StructField("USERNAME", StringType()),StructField("FIRSTNAME", StringType()),StructField("LASTNAME", StringType())])
            >>> # Create a DataFrame that is configured to load data from the CSV files in the stage.
            >>> df = session.read.schema(schema).option("format_name", "csv_format").csv("@mystage/testCSVspecialFormat.csv")
            >>> # Load the data into the DataFrame and return an array of rows containing the results.
            >>> df.collect()
            [Row(ID=0, USERNAME='admin', FIRSTNAME=None, LASTNAME=None), Row(ID=1, USERNAME='test_user', FIRSTNAME='test', LASTNAME='user')]
            ```

            Copy

    Example 11:
    :   Querying metadata for staged files:
        :   ```
            >>> from snowflake.snowpark.column import METADATA_FILENAME, METADATA_FILE_ROW_NUMBER
            >>> df = session.read.with_metadata(METADATA_FILENAME, METADATA_FILE_ROW_NUMBER.as_("ROW NUMBER")).schema(user_schema).csv("@mystage/testCSV.csv")
            >>> # Load the data into the DataFrame and return an array of rows containing the results.
            >>> df.show()
            --------------------------------------------------------
            |"METADATA$FILENAME"  |"ROW NUMBER"  |"A"  |"B"  |"C"  |
            --------------------------------------------------------
            |testCSV.csv          |1             |1    |one  |1.2  |
            |testCSV.csv          |2             |2    |two  |2.2  |
            --------------------------------------------------------
            ```

            Copy

    Example 12:
    :   Inferring schema for csv and json files (Preview Feature - Open):
        :   ```
            >>> # Read a csv file without a header
            >>> df = session.read.option("INFER_SCHEMA", True).csv("@mystage/testCSV.csv")
            >>> df.show()
            ----------------------
            |"c1"  |"c2"  |"c3"  |
            ----------------------
            |1     |one   |1.2   |
            |2     |two   |2.2   |
            ----------------------
            ```

            Copy

            ```
            >>> # Read a csv file with header and parse the header
            >>> _ = session.file.put("tests/resources/testCSVheader.csv", "@mystage", auto_compress=False)
            >>> df = session.read.option("INFER_SCHEMA", True).option("PARSE_HEADER", True).csv("@mystage/testCSVheader.csv")
            >>> df.show()
            ----------------------------
            |"id"  |"name"  |"rating"  |
            ----------------------------
            |1     |one     |1.2       |
            |2     |two     |2.2       |
            ----------------------------
            ```

            Copy

            ```
            >>> df = session.read.option("INFER_SCHEMA", True).json("@mystage/testJson.json")
            >>> df.show()
            ------------------------------
            |"color"  |"fruit"  |"size"  |
            ------------------------------
            |Red      |Apple    |Large   |
            |Red      |Apple    |Large   |
            ------------------------------
            ```

            Copy

    Methods

    |  |  |
    | --- | --- |
    | [`avro`](snowflake.snowpark.DataFrameReader.avro.html#snowflake.snowpark.DataFrameReader.avro "snowflake.snowpark.DataFrameReader.avro")(path) | Specify the path of the AVRO file(s) to load. |
    | [`csv`](snowflake.snowpark.DataFrameReader.csv.html#snowflake.snowpark.DataFrameReader.csv "snowflake.snowpark.DataFrameReader.csv")(path) | Specify the path of the CSV file(s) to load. |
    | [`json`](snowflake.snowpark.DataFrameReader.json.html#snowflake.snowpark.DataFrameReader.json "snowflake.snowpark.DataFrameReader.json")(path) | Specify the path of the JSON file(s) to load. |
    | [`option`](snowflake.snowpark.DataFrameReader.option.html#snowflake.snowpark.DataFrameReader.option "snowflake.snowpark.DataFrameReader.option")(key, value) | Sets the specified option in the DataFrameReader. |
    | [`options`](snowflake.snowpark.DataFrameReader.options.html#snowflake.snowpark.DataFrameReader.options "snowflake.snowpark.DataFrameReader.options")(configs) | Sets multiple specified options in the DataFrameReader. |
    | [`orc`](snowflake.snowpark.DataFrameReader.orc.html#snowflake.snowpark.DataFrameReader.orc "snowflake.snowpark.DataFrameReader.orc")(path) | Specify the path of the ORC file(s) to load. |
    | [`parquet`](snowflake.snowpark.DataFrameReader.parquet.html#snowflake.snowpark.DataFrameReader.parquet "snowflake.snowpark.DataFrameReader.parquet")(path) | Specify the path of the PARQUET file(s) to load. |
    | [`schema`](snowflake.snowpark.DataFrameReader.schema.html#snowflake.snowpark.DataFrameReader.schema "snowflake.snowpark.DataFrameReader.schema")(schema) | Define the schema for CSV files that you want to read. |
    | [`table`](snowflake.snowpark.DataFrameReader.table.html#snowflake.snowpark.DataFrameReader.table "snowflake.snowpark.DataFrameReader.table")(name) | Returns a Table that points to the specified table. |
    | [`with_metadata`](snowflake.snowpark.DataFrameReader.with_metadata.html#snowflake.snowpark.DataFrameReader.with_metadata "snowflake.snowpark.DataFrameReader.with_metadata")(\*metadata\_cols) | Define the metadata columns that need to be selected from stage files. |
    | [`xml`](snowflake.snowpark.DataFrameReader.xml.html#snowflake.snowpark.DataFrameReader.xml "snowflake.snowpark.DataFrameReader.xml")(path) | Specify the path of the XML file(s) to load. |

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.