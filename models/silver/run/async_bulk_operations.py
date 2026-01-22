import time
from typing import Optional

import snowflake.snowpark as snowpark
from joblib import Parallel, delayed


class BulkQueryWriter:
    def __init__(self, session: snowpark.Session):
        self.session = session
        self.register_bulk_thread_runner()

    def register_bulk_thread_runner(self):
        """
        Registers a temporary stored procedure 'BULK_THREAD_RUNNER' for parallel SQL execution.

        The procedure distributes SQL statements across threads, executes each thread's subset, and returns results as a DataFrame.

        Notes:
            - Temporary, replaces any existing procedure with the same name.
            - Uses 'snowflake-snowpark-python' package.
            - Exceptions during execution are ignored.
        """

        def bulk_thread_runner(
            session: snowpark.Session,
            sql_statements_query: str,
            thread_number: int,
            total_number_of_threads: int,
        ) -> Optional[snowpark.DataFrame]:
            session.query_tag = f"Thread {thread_number} of {total_number_of_threads}"
            all_results = []
            sql_statements = (
                session.sql(sql_statements_query).to_pandas().iloc[:, 0].sort_values()
            )
            for index, sql_statement in enumerate(sql_statements):
                if thread_number == (index % total_number_of_threads):
                    try:
                        results = session.sql(sql_statement).collect()
                        if results:
                            all_results.extend(results)
                    except Exception:
                        pass
            if all_results:
                return session.createDataFrame(data=all_results)

        self.session.sproc.register(
            func=bulk_thread_runner,
            name="BULK_THREAD_RUNNER",
            is_permanent=False,
            replace=True,
            stage_location=None,
            packages=["snowflake-snowpark-python"],
            execute_as="CALLER",
            comment="Temporary stored procedure for running multiple queries in parallel.",
        )

    def run(
        self,
        sql_statements_query: str,
        output_table_name: str,
        write_mode: str = "overwrite",
        table_type: str = "transient",
        commit_interval: int = 100000,
        parallel_query_limit: int = 8,
    ) -> str:
        """
        Executes a set of SQL statements in parallel and writes their results to a Snowflake table.

        Depending on the number of SQL statements, this method either:
            - Uses joblib for local parallel execution if the number of statements is small.
            - Uses the registered Snowflake stored procedure for distributed parallel execution if the number is large.

        Args:
            sql_statements_query (str): SQL query that returns the list of SQL statements to execute.
            output_table_name (str): Name of the output table to write results to.
            write_mode (str): Write mode for the output table ("overwrite" or "append").
            table_type (str): Type of the output table ("transient" or "temporary").
            commit_interval (int): Number of records to accumulate before writing to the table.
            parallel_query_limit (int): Number of parallel jobs/threads to use.

        Returns:
            str: Summary message with the number of records written.
        """
        all_results = []
        num_results_found = 0

        def get_query_result(session: snowpark.Session, sql_statement: str):
            """
            Executes a single SQL statement and yields its results.

            Args:
                session (snowpark.Session): Snowpark session.
                sql_statement (str): SQL statement to execute.

            Yields:
                Rows from the executed SQL statement.
            """
            try:
                results = session.sql(sql_statement).collect()
                if results:
                    yield from results
            except Exception:
                # Ignore exceptions for individual statements
                pass

        # Retrieve all SQL statements to execute
        all_sql_statements = [
            row[0] for row in self.session.sql(sql_statements_query).collect() if row
        ]

        if all_sql_statements:
            # Use joblib for local parallel execution if the number of statements is small
            if len(all_sql_statements) < (parallel_query_limit * 5):
                res = Parallel(
                    n_jobs=-1, require="sharedmem", return_as="generator_unordered"
                )(
                    delayed(get_query_result)(self.session, sql_statement)
                    for sql_statement in all_sql_statements
                )
                for query_results in res:
                    if query_results:
                        all_results.extend(query_results)
                        if len(all_results) >= commit_interval:
                            num_results_found += len(all_results)
                            self.session.createDataFrame(
                                data=all_results
                            ).write.save_as_table(
                                table_name=output_table_name,
                                mode=write_mode,
                                table_type=table_type,
                            )
                            all_results = []
                            write_mode = "append"
                # Write any remaining results
                if all_results:
                    num_results_found += len(all_results)
                    self.session.createDataFrame(data=all_results).write.save_as_table(
                        table_name=output_table_name,
                        mode=write_mode,
                        table_type=table_type,
                    )
            else:
                # Use the registered stored procedure for distributed parallel execution
                running_processes = []
                for thread_number in range(parallel_query_limit):
                    async_job = self.session.sql(
                        "CALL bulk_thread_runner(?, ?, ?)",
                        [sql_statements_query, thread_number, parallel_query_limit],
                    ).collect_nowait()
                    running_processes.append(async_job)
                # Monitor and collect results from async jobs
                while running_processes:
                    for index, async_job in enumerate(running_processes):
                        if async_job.is_done():
                            running_processes.pop(index)
                            try:
                                results = async_job.result()
                                if results:
                                    all_results.extend(results)
                            except Exception:
                                # Ignore exceptions for individual jobs
                                pass
                            if len(all_results) >= commit_interval:
                                num_results_found += len(all_results)
                                self.session.createDataFrame(
                                    data=all_results
                                ).write.save_as_table(
                                    table_name=output_table_name,
                                    mode=write_mode,
                                    table_type=table_type,
                                )
                                all_results = []
                                write_mode = "append"
                    if running_processes:
                        time.sleep(0)  # Yield control to avoid busy waiting
                # Write any remaining results
                if all_results:
                    num_results_found += len(all_results)
                    self.session.createDataFrame(data=all_results).write.save_as_table(
                        table_name=output_table_name,
                        mode=write_mode,
                        table_type=table_type,
                    )
        return f"Number of records written: {num_results_found}"


def model(dbt, session):
    """
    DBT model entry point. Configures the model and runs the async bulk query writer.
    """
    dbt.config(
        materialized="table",
        packages=["snowflake-snowpark-python", "joblib"],
        python_version="3.11",
    )

    sql_statements_query = """
        select 'select '||seq4()||' as row_num' FROM TABLE(GENERATOR(ROWCOUNT => 10))
    """

    writer = BulkQueryWriter(session=session)

    writer.run(
        sql_statements_query=sql_statements_query,
        output_table_name="temp_output_table",
        write_mode="overwrite",
        table_type="temporary",
        commit_interval=100000,
        parallel_query_limit=8,
    )

    return session.table("temp_output_table")
