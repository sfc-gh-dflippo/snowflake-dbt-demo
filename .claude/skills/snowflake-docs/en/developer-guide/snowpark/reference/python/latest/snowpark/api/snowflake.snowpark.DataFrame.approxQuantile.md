---
auto_generated: true
description: For a specified numeric column and a list of desired quantiles, returns
  an approximate value for the column at each of the desired quantiles. This function
  uses the t-Digest algorithm.
last_scraped: '2026-01-14T16:54:52.538736+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrame.approxQuantile
title: snowflake.snowpark.DataFrame.approxQuantile | Snowflake Documentation
---

1.44.0 (latest)1.43.01.42.01.41.01.40.01.39.11.39.01.38.01.37.01.35.01.34.01.33.01.32.01.31.01.30.01.29.11.29.01.28.01.27.01.26.01.25.01.24.01.23.01.22.11.21.11.21.01.20.01.19.01.18.01.17.01.16.01.15.01.14.01.13.01.12.11.12.01.11.11.10.01.9.01.8.01.7.01.6.11.5.01.4.01.3.01.2.01.1.0

1. [Overview](../../index.md)
2. [Snowpark Session](../session.md)
3. [Snowpark APIs](../index.md)

   * [Input/Output](../io.md)
   * [DataFrame](../dataframe.md)

     + [DataFrame](snowflake.snowpark.DataFrame.md)
     + [DataFrameNaFunctions](snowflake.snowpark.DataFrameNaFunctions.md)
     + [DataFrameStatFunctions](snowflake.snowpark.DataFrameStatFunctions.md)
     + [DataFrameAnalyticsFunctions](snowflake.snowpark.DataFrameAnalyticsFunctions.md)
     + [DataFrameAIFunctions](snowflake.snowpark.DataFrameAIFunctions.md)
     + [DataFrame.agg](snowflake.snowpark.DataFrame.agg.md)
     + [DataFrame.approxQuantile](snowflake.snowpark.DataFrame.approxQuantile.md)
     + [DataFrame.approx\_quantile](snowflake.snowpark.DataFrame.approx_quantile.md)
     + [DataFrame.cache\_result](snowflake.snowpark.DataFrame.cache_result.md)
     + [DataFrame.col](snowflake.snowpark.DataFrame.col.md)
     + [DataFrame.col\_ilike](snowflake.snowpark.DataFrame.col_ilike.md)
     + [DataFrame.collect](snowflake.snowpark.DataFrame.collect.md)
     + [DataFrame.collect\_nowait](snowflake.snowpark.DataFrame.collect_nowait.md)
     + [DataFrame.copy\_into\_table](snowflake.snowpark.DataFrame.copy_into_table.md)
     + [DataFrame.corr](snowflake.snowpark.DataFrame.corr.md)
     + [DataFrame.count](snowflake.snowpark.DataFrame.count.md)
     + [DataFrame.cov](snowflake.snowpark.DataFrame.cov.md)
     + [DataFrame.create\_or\_replace\_dynamic\_table](snowflake.snowpark.DataFrame.create_or_replace_dynamic_table.md)
     + [DataFrame.createOrReplaceTempView](snowflake.snowpark.DataFrame.createOrReplaceTempView.md)
     + [DataFrame.createOrReplaceView](snowflake.snowpark.DataFrame.createOrReplaceView.md)
     + [DataFrame.createTempView](snowflake.snowpark.DataFrame.createTempView.md)
     + [DataFrame.create\_or\_replace\_temp\_view](snowflake.snowpark.DataFrame.create_or_replace_temp_view.md)
     + [DataFrame.create\_or\_replace\_view](snowflake.snowpark.DataFrame.create_or_replace_view.md)
     + [DataFrame.create\_temp\_view](snowflake.snowpark.DataFrame.create_temp_view.md)
     + [DataFrame.crossJoin](snowflake.snowpark.DataFrame.crossJoin.md)
     + [DataFrame.cross\_join](snowflake.snowpark.DataFrame.cross_join.md)
     + [DataFrame.crosstab](snowflake.snowpark.DataFrame.crosstab.md)
     + [DataFrame.cube](snowflake.snowpark.DataFrame.cube.md)
     + [DataFrame.describe](snowflake.snowpark.DataFrame.describe.md)
     + [DataFrame.distinct](snowflake.snowpark.DataFrame.distinct.md)
     + [DataFrame.drop](snowflake.snowpark.DataFrame.drop.md)
     + [DataFrame.dropDuplicates](snowflake.snowpark.DataFrame.dropDuplicates.md)
     + [DataFrame.drop\_duplicates](snowflake.snowpark.DataFrame.drop_duplicates.md)
     + [DataFrame.dropna](snowflake.snowpark.DataFrame.dropna.md)
     + [DataFrame.except\_](snowflake.snowpark.DataFrame.except_.md)
     + [DataFrame.explain](snowflake.snowpark.DataFrame.explain.md)
     + [DataFrame.fillna](snowflake.snowpark.DataFrame.fillna.md)
     + [DataFrame.filter](snowflake.snowpark.DataFrame.filter.md)
     + [DataFrame.first](snowflake.snowpark.DataFrame.first.md)
     + [DataFrame.flatten](snowflake.snowpark.DataFrame.flatten.md)
     + [DataFrame.groupBy](snowflake.snowpark.DataFrame.groupBy.md)
     + [DataFrame.group\_by](snowflake.snowpark.DataFrame.group_by.md)
     + [DataFrame.group\_by\_grouping\_sets](snowflake.snowpark.DataFrame.group_by_grouping_sets.md)
     + [DataFrame.intersect](snowflake.snowpark.DataFrame.intersect.md)
     + [DataFrame.join](snowflake.snowpark.DataFrame.join.md)
     + [DataFrame.join\_table\_function](snowflake.snowpark.DataFrame.join_table_function.md)
     + [DataFrame.lateral\_join](snowflake.snowpark.DataFrame.lateral_join.md)
     + [DataFrame.limit](snowflake.snowpark.DataFrame.limit.md)
     + [DataFrame.minus](snowflake.snowpark.DataFrame.minus.md)
     + [DataFrame.natural\_join](snowflake.snowpark.DataFrame.natural_join.md)
     + [DataFrame.orderBy](snowflake.snowpark.DataFrame.orderBy.md)
     + [DataFrame.order\_by](snowflake.snowpark.DataFrame.order_by.md)
     + [DataFrame.pivot](snowflake.snowpark.DataFrame.pivot.md)
     + [DataFrame.print\_schema](snowflake.snowpark.DataFrame.print_schema.md)
     + [DataFrame.printSchema](snowflake.snowpark.DataFrame.printSchema.md)
     + [DataFrame.randomSplit](snowflake.snowpark.DataFrame.randomSplit.md)
     + [DataFrame.random\_split](snowflake.snowpark.DataFrame.random_split.md)
     + [DataFrame.rename](snowflake.snowpark.DataFrame.rename.md)
     + [DataFrame.replace](snowflake.snowpark.DataFrame.replace.md)
     + [DataFrame.rollup](snowflake.snowpark.DataFrame.rollup.md)
     + [DataFrame.sample](snowflake.snowpark.DataFrame.sample.md)
     + [DataFrame.sampleBy](snowflake.snowpark.DataFrame.sampleBy.md)
     + [DataFrame.sample\_by](snowflake.snowpark.DataFrame.sample_by.md)
     + [DataFrame.select](snowflake.snowpark.DataFrame.select.md)
     + [DataFrame.selectExpr](snowflake.snowpark.DataFrame.selectExpr.md)
     + [DataFrame.select\_expr](snowflake.snowpark.DataFrame.select_expr.md)
     + [DataFrame.show](snowflake.snowpark.DataFrame.show.md)
     + [DataFrame.sort](snowflake.snowpark.DataFrame.sort.md)
     + [DataFrame.subtract](snowflake.snowpark.DataFrame.subtract.md)
     + [DataFrame.take](snowflake.snowpark.DataFrame.take.md)
     + [DataFrame.toDF](snowflake.snowpark.DataFrame.toDF.md)
     + [DataFrame.toLocalIterator](snowflake.snowpark.DataFrame.toLocalIterator.md)
     + [DataFrame.toPandas](snowflake.snowpark.DataFrame.toPandas.md)
     + [DataFrame.to\_df](snowflake.snowpark.DataFrame.to_df.md)
     + [DataFrame.to\_local\_iterator](snowflake.snowpark.DataFrame.to_local_iterator.md)
     + [DataFrame.to\_pandas](snowflake.snowpark.DataFrame.to_pandas.md)
     + [DataFrame.to\_pandas\_batches](snowflake.snowpark.DataFrame.to_pandas_batches.md)
     + [DataFrame.to\_snowpark\_pandas](snowflake.snowpark.DataFrame.to_snowpark_pandas.md)
     + [DataFrame.union](snowflake.snowpark.DataFrame.union.md)
     + [DataFrame.unionAll](snowflake.snowpark.DataFrame.unionAll.md)
     + [DataFrame.unionAllByName](snowflake.snowpark.DataFrame.unionAllByName.md)
     + [DataFrame.unionByName](snowflake.snowpark.DataFrame.unionByName.md)
     + [DataFrame.union\_all](snowflake.snowpark.DataFrame.union_all.md)
     + [DataFrame.union\_all\_by\_name](snowflake.snowpark.DataFrame.union_all_by_name.md)
     + [DataFrame.union\_by\_name](snowflake.snowpark.DataFrame.union_by_name.md)
     + [DataFrame.unpivot](snowflake.snowpark.DataFrame.unpivot.md)
     + [DataFrame.where](snowflake.snowpark.DataFrame.where.md)
     + [DataFrame.withColumn](snowflake.snowpark.DataFrame.withColumn.md)
     + [DataFrame.withColumnRenamed](snowflake.snowpark.DataFrame.withColumnRenamed.md)
     + [DataFrame.with\_column](snowflake.snowpark.DataFrame.with_column.md)
     + [DataFrame.with\_column\_renamed](snowflake.snowpark.DataFrame.with_column_renamed.md)
     + [DataFrame.with\_columns](snowflake.snowpark.DataFrame.with_columns.md)
     + [DataFrameNaFunctions.drop](snowflake.snowpark.DataFrameNaFunctions.drop.md)
     + [DataFrameNaFunctions.fill](snowflake.snowpark.DataFrameNaFunctions.fill.md)
     + [DataFrameNaFunctions.replace](snowflake.snowpark.DataFrameNaFunctions.replace.md)
     + [DataFrameStatFunctions.approxQuantile](snowflake.snowpark.DataFrameStatFunctions.approxQuantile.md)
     + [DataFrameStatFunctions.approx\_quantile](snowflake.snowpark.DataFrameStatFunctions.approx_quantile.md)
     + [DataFrameStatFunctions.corr](snowflake.snowpark.DataFrameStatFunctions.corr.md)
     + [DataFrameStatFunctions.cov](snowflake.snowpark.DataFrameStatFunctions.cov.md)
     + [DataFrameStatFunctions.crosstab](snowflake.snowpark.DataFrameStatFunctions.crosstab.md)
     + [DataFrameStatFunctions.sampleBy](snowflake.snowpark.DataFrameStatFunctions.sampleBy.md)
     + [DataFrameStatFunctions.sample\_by](snowflake.snowpark.DataFrameStatFunctions.sample_by.md)
     + [DataFrameAnalyticsFunctions.moving\_agg](snowflake.snowpark.DataFrameAnalyticsFunctions.moving_agg.md)
     + [DataFrameAnalyticsFunctions.cumulative\_agg](snowflake.snowpark.DataFrameAnalyticsFunctions.cumulative_agg.md)
     + [DataFrameAnalyticsFunctions.compute\_lag](snowflake.snowpark.DataFrameAnalyticsFunctions.compute_lag.md)
     + [DataFrameAnalyticsFunctions.compute\_lead](snowflake.snowpark.DataFrameAnalyticsFunctions.compute_lead.md)
     + [DataFrameAnalyticsFunctions.time\_series\_agg](snowflake.snowpark.DataFrameAnalyticsFunctions.time_series_agg.md)
     + [DataFrameAIFunctions.agg](snowflake.snowpark.DataFrameAIFunctions.agg.md)
     + [DataFrameAIFunctions.classify](snowflake.snowpark.DataFrameAIFunctions.classify.md)
     + [DataFrameAIFunctions.complete](snowflake.snowpark.DataFrameAIFunctions.complete.md)
     + [DataFrameAIFunctions.count\_tokens](snowflake.snowpark.DataFrameAIFunctions.count_tokens.md)
     + [DataFrameAIFunctions.embed](snowflake.snowpark.DataFrameAIFunctions.embed.md)
     + [DataFrameAIFunctions.extract](snowflake.snowpark.DataFrameAIFunctions.extract.md)
     + [DataFrameAIFunctions.filter](snowflake.snowpark.DataFrameAIFunctions.filter.md)
     + [DataFrameAIFunctions.parse\_document](snowflake.snowpark.DataFrameAIFunctions.parse_document.md)
     + [DataFrameAIFunctions.sentiment](snowflake.snowpark.DataFrameAIFunctions.sentiment.md)
     + [DataFrameAIFunctions.similarity](snowflake.snowpark.DataFrameAIFunctions.similarity.md)
     + [DataFrameAIFunctions.split\_text\_markdown\_header](snowflake.snowpark.DataFrameAIFunctions.split_text_markdown_header.md)
     + [DataFrameAIFunctions.split\_text\_recursive\_character](snowflake.snowpark.DataFrameAIFunctions.split_text_recursive_character.md)
     + [DataFrameAIFunctions.summarize\_agg](snowflake.snowpark.DataFrameAIFunctions.summarize_agg.md)
     + [DataFrameAIFunctions.transcribe](snowflake.snowpark.DataFrameAIFunctions.transcribe.md)
     + [dataframe.map](snowflake.snowpark.dataframe.map.md)
     + [dataframe.map\_in\_pandas](snowflake.snowpark.dataframe.map_in_pandas.md)
     + [DataFrame.ai](snowflake.snowpark.DataFrame.ai.md)
     + [DataFrame.columns](snowflake.snowpark.DataFrame.columns.md)
     + [DataFrame.na](snowflake.snowpark.DataFrame.na.md)
     + [DataFrame.queries](snowflake.snowpark.DataFrame.queries.md)
     + [DataFrame.schema](snowflake.snowpark.DataFrame.schema.md)
     + [DataFrame.stat](snowflake.snowpark.DataFrame.stat.md)
     + [DataFrame.write](snowflake.snowpark.DataFrame.write.md)
     + [DataFrame.is\_cached](snowflake.snowpark.DataFrame.is_cached.md)
     + [DataFrame.session](snowflake.snowpark.DataFrame.session.md)
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
   * [StoredProcedureProfiler](../stored_procedure_profiler.md)
   * [User-Defined Functions](../udf.md)
   * [User-Defined Aggregate Functions](../udaf.md)
   * [User-Defined Table Functions](../udtf.md)
   * [Snowpark Secrets](../secrets.md)
   * [Observability](../observability.md)
   * [Files](../files.md)
   * [Catalog](../catalog.md)
   * [LINEAGE](../lineage.md)
   * [Context](../context.md)
   * [Exceptions](../exceptions.md)
   * [Testing](../testing.md)
4. [Snowpark pandas API](../../modin/index.md)

[Developer](../../../../../../../developer.md)[Snowpark API](../../../../../index.md)[Python](../../../../../python/index.md)[Python API Reference](../../index.md)[Snowpark APIs](../index.md)[DataFrame](../dataframe.md)DataFrame.approxQuantile

# snowflake.snowpark.DataFrame.approxQuantile[¶](#snowflake-snowpark-dataframe-approxquantile "Permalink to this heading")

DataFrame.approxQuantile(*col: Union[[Column](snowflake.snowpark.Column.html#snowflake.snowpark.Column "snowflake.snowpark.column.Column"), str, Iterable[Union[[Column](snowflake.snowpark.Column.html#snowflake.snowpark.Column "snowflake.snowpark.column.Column"), str]]]*, *percentile: Iterable[float]*, *\**, *statement\_params: Optional[Dict[str, str]] = None*) → Union[List[float], List[List[float]]][[source]](https://github.com/snowflakedb/snowpark-python/blob/v1.44.0/src/snowflake/snowpark/dataframe_stat_functions.py#L63-L177)[¶](#snowflake.snowpark.DataFrame.approxQuantile "Permalink to this definition")
:   For a specified numeric column and a list of desired quantiles, returns an approximate value for the column at each of the desired quantiles.
    This function uses the t-Digest algorithm.

    Examples:

    ```
    >>> df = session.create_dataframe([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], schema=["a"])
    >>> df.stat.approx_quantile("a", [0, 0.1, 0.4, 0.6, 1])  

    >>> df2 = session.create_dataframe([[0.1, 0.5], [0.2, 0.6], [0.3, 0.7]], schema=["a", "b"])
    >>> df2.stat.approx_quantile(["a", "b"], [0, 0.1, 0.6])
    ```

    Copy

    Parameters:
    :   * **col** – The name of the numeric column.
        * **percentile** – A list of float values greater than or equal to 0.0 and less than 1.0.
        * **statement\_params** – Dictionary of statement level parameters to be set while executing this action.

    Returns:
    :   A list of approximate percentile values if `col` is a single column name, or a matrix
        with the dimensions `(len(col) * len(percentile)` containing the
        approximate percentile values if `col` is a list of column names.

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.