---
auto_generated: true
description: Executes internally a COPY INTO <location> to unload data from a DataFrame
  into one or more CSV files in a stage or external stage.
last_scraped: '2026-01-14T16:54:47.280481+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrameWriter.csv
title: snowflake.snowpark.DataFrameWriter.csv | Snowflake Documentation
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

[Developer](../../../../../../../developer.md)[Snowpark API](../../../../../index.md)[Python](../../../../../python/index.md)[Python API Reference](../../index.md)[Snowpark APIs](../index.md)[Input/Output](../io.md)DataFrameWriter.csv

You are viewing documentation about an older version (1.23.0).  [View latest version](../../../1.44.0/index.md)

# snowflake.snowpark.DataFrameWriter.csv[¶](#snowflake-snowpark-dataframewriter-csv "Permalink to this heading")

DataFrameWriter.csv(*location: str*, *\**, *partition\_by: Optional[Union[[Column](snowflake.snowpark.Column.html#snowflake.snowpark.Column "snowflake.snowpark.column.Column"), str]] = None*, *format\_type\_options: Optional[Dict[str, str]] = None*, *header: bool = False*, *statement\_params: Optional[Dict[str, str]] = None*, *block: bool = True*, *\*\*copy\_options: Optional[str]*) → Union[List[[Row](snowflake.snowpark.Row.html#snowflake.snowpark.Row "snowflake.snowpark.row.Row")], [AsyncJob](snowflake.snowpark.AsyncJob.html#snowflake.snowpark.AsyncJob "snowflake.snowpark.async_job.AsyncJob")][[source]](https://github.com/snowflakedb/snowpark-python/blob/v1.23.0/src/snowflake/snowpark/dataframe_writer.py#L420-L464)[¶](#snowflake.snowpark.DataFrameWriter.csv "Permalink to this definition")
:   Executes internally a [COPY INTO <location>](https://docs.snowflake.com/en/sql-reference/sql/copy-into-location.html) to unload data from a `DataFrame` into one or more CSV files in a stage or external stage.

    Parameters:
    :   * **location** – The destination stage location.
        * **partition\_by** – Specifies an expression used to partition the unloaded table rows into separate files. It can be a [`Column`](snowflake.snowpark.Column.html#snowflake.snowpark.Column "snowflake.snowpark.Column"), a column name, or a SQL expression.
        * **format\_type\_options** – Depending on the `file_format_type` specified, you can include more format specific options. Use the options documented in the [Format Type Options](https://docs.snowflake.com/en/sql-reference/sql/copy-into-location.html#format-type-options-formattypeoptions).
        * **header** – Specifies whether to include the table column headings in the output files.
        * **statement\_params** – Dictionary of statement level parameters to be set while executing this action.
        * **copy\_options** – The kwargs that are used to specify the copy options. Use the options documented in the [Copy Options](https://docs.snowflake.com/en/sql-reference/sql/copy-into-location.html#copy-options-copyoptions).
        * **block** – A bool value indicating whether this function will wait until the result is available.
          When it is `False`, this function executes the underlying queries of the dataframe
          asynchronously and returns an [`AsyncJob`](snowflake.snowpark.AsyncJob.html#snowflake.snowpark.AsyncJob "snowflake.snowpark.AsyncJob").

    Returns:
    :   A list of [`Row`](snowflake.snowpark.Row.html#snowflake.snowpark.Row "snowflake.snowpark.Row") objects containing unloading results.

    Example:

    ```
    >>> # save this dataframe to a csv file on the session stage
    >>> df = session.create_dataframe([["John", "Berry"], ["Rick", "Berry"], ["Anthony", "Davis"]], schema = ["FIRST_NAME", "LAST_NAME"])
    >>> remote_file_path = f"{session.get_session_stage()}/names.csv"
    >>> copy_result = df.write.csv(remote_file_path, overwrite=True, single=True)
    >>> copy_result[0].rows_unloaded
    3
    ```

    Copy

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.