docker build --tag=custom-dbt .
docker run -it --network=host --name custom-dbt --rm --env-file ../.env custom-dbt:latest build
