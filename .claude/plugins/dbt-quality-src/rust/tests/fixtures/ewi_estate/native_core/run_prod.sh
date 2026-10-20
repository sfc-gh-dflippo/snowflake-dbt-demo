#!/bin/bash
# OPS004: automation uses dbt run + dbt test separately
dbt run --target prod
dbt test --target prod
