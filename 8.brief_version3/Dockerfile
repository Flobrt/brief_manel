FROM apache/airflow:2.7.3

USER airflow
RUN pip install --no-cache-dir soda-core soda-core-postgres
USER airflow

# CMD airflow connections add 'my_prod_db' --conn-json '{"conn_type": "my-conn-type", "login": "my-login", "password": "my-password", "host": "my-host", "port": 1234, "schema": "my-schema", "extra": {"param1": "val1", "param2": "val2"}}'