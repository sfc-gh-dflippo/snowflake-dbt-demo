from joblib import Parallel, delayed
import snowflake.snowpark as snowpark


def async_bulk_query_writer(session: snowpark.Session, sql_statements, output_table_name, write_mode, table_type, commit_interval):
    all_results = []
    num_results_found = 0

    # Function to execute a SQL and wait for the results
    get_query_result = lambda sql_statement: session.sql(sql_statement).collect()

    # Split up the work by the number of CPU processors
    res = Parallel(n_jobs=-1, return_as="generator")(
        delayed(get_query_result)(sql_statement) for sql_statement in sql_statements
    )

    # The generator will stream results to our all_results cache to minimize memory usage
    for query_results in res:
        all_results.extend( query_results )

        # If we reach the commit interval, write the output
        if len(all_results) >= commit_interval:
            num_results_found += len(all_results)
            session.createDataFrame(data=all_results).write.save_as_table(
                table_name=output_table_name, mode=write_mode, table_type=table_type)
            all_results = []
            write_mode = "append"

    # Write all the final results
    if len(all_results) > 0:
        num_results_found += len(all_results)
        session.createDataFrame(data=all_results).write.save_as_table(
            table_name=output_table_name, mode=write_mode, table_type=table_type)


def model(dbt, session: snowpark.Session):
    dbt.config(materialized="table", packages = ["joblib"])
    upload_cache_size = 100000
    sql_statements = []
    for x in range(10):
        sql_statements.append(f"select {x} as row_num")

    async_bulk_query_writer(session, sql_statements, "my_temp", "overwrite", "temporary", upload_cache_size)

    return session.table("my_temp")
