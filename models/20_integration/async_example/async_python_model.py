import snowflake.snowpark as snowpark
import time


def async_bulk_query_writer(session: snowpark.Session, sql_statements,
        output_table_name, write_mode, table_type, commit_interval, parallel_query_limit):
    all_results = []
    num_results_found = 0

    running_processes = []

    # Submit each statement as an asyncronous job
    for sql_statement in sql_statements:

        # If we are at the query limit we need to see if a job has completed
        # We won't leave this loop until we are below the query limit
        while len(running_processes) == parallel_query_limit:
            for index, async_job in enumerate(running_processes):
                if async_job.is_done():
                    # Remove the process from our list of running processes
                    running_processes.pop(index)
                    try:
                        # Get results from a completed async job
                        results = async_job.result()
                        if results:
                            all_results.extend(results)
                    except:
                        raise

                    # If we reach the commit interval, write the output
                    if len(all_results) >= commit_interval:
                        num_results_found += len(all_results)
                        session.createDataFrame(data=all_results).write.save_as_table(
                            table_name=output_table_name, mode=write_mode, table_type=table_type)
                        all_results = []
                        write_mode = "append"

            # Sleep if we still haven't completed a job
            if len(running_processes) == parallel_query_limit:
                time.sleep(0.1)

        # Submit the additional async query to running processes
        async_job = session.sql(sql_statement).collect_nowait()
        running_processes.append(async_job)

    # Wait for the final processes to end
    while len(running_processes) > 0:
        for index, async_job in enumerate(running_processes):
            if async_job.is_done():
                # Remove the process from our list of running processes
                running_processes.pop(index)
                try:
                    # Get results from a completed async job
                    results = async_job.result()
                    if results:
                        all_results.extend(results)
                except:
                    raise

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

    return f"Number of records written: {num_results_found}"


def model(dbt, session: snowpark.Session):
    dbt.config(materialized="table")
    upload_cache_size = 100000
    sql_statements = [ f"select {x} as row_num" for x in range(10) ]
    async_bulk_query_writer(session, sql_statements, "MY_TEMP", "overwrite", "temporary", upload_cache_size, 10)

    return session.table("MY_TEMP")
