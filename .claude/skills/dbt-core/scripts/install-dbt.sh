#!/bin/sh
# Install the dbt Fusion engine (dbt 2.0) standalone binary on macOS/Linux, then show the version.

curl -fsSL https://public.cdn.getdbt.com/fs/install/install.sh | sh -s -- --update
dbt --version
