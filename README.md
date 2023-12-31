# airflow-devcontainer

## Build devcontainer

Build the devcontainer by running `ctrl+shif+p` in Visual Studio Code, and then select `Dev Containers: Rebuild Container Without Cache`.

## Setup Airflow

Run `make airflow-setup` for configuring the Airflow and initializing its database.

## Start Airflow Scheduler

Open another terminal in Visual Studio Code and run `make airflow-start-scheduler`.

## Start Airflow Webserver

Open another terminal in Visual Studio Code and run `make airflow-start-webserver`.

## Execute DAG

Open `http://localhost:8080/login` with your browser. Log in with username `admin` and password `admin`. Navigate to `DAGs` and select `tampere_last_1h_temperature_dag` from the list. Trigger the `Tampere last 1h temperatures DAG`.

Then look for a png image from the `/workspaces/airflow-devcontainer`. The png image should contain temperature observations from Finnish Meteorological Institute's [Tampere Härmälä observation site](https://en.ilmatieteenlaitos.fi/local-weather/tampere?station=101124) of the last hour (UTC). The data is requested by using the [fmiopendata](https://github.com/pnuu/fmiopendata) library. More information from [https://en.ilmatieteenlaitos.fi/open-data-manual-accessing-data](https://en.ilmatieteenlaitos.fi/open-data-manual-accessing-data).

![airflow example DAG](/screenshot/airflow-example-dag.png "Airflow example DAG")
