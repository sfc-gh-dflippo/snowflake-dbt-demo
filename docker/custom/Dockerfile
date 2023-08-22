ARG DBT_VERSION=1.6.0
FROM ghcr.io/dbt-labs/dbt-snowflake:${DBT_VERSION}

ENTRYPOINT ["/entrypoint.sh"]
CMD ["build"]

ENV GIT_REPO_URL="https://github.com/sfc-gh-dflippo/snowflake-dbt-demo.git"
ENV GIT_BRANCH="main"
ENV DBT_PROFILES_DIR=./docker

COPY --chmod=777 ./entrypoint.sh /entrypoint.sh
RUN git clone --quiet -b $GIT_BRANCH $GIT_REPO_URL /usr/app/dbt
