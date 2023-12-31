from __future__ import annotations
from textwrap import dedent
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from json import dumps, loads
from fmiopendata.wfs import download_stored_query
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
import os
import pandas as pd
import pendulum

with DAG(
    'tampere_last_1h_temperature_dag',
    default_args={"retries": 2},
    description='Tampere last 1h temperatures DAG',
    schedule=None,
    start_date=pendulum.datetime(2023, 12, 31, tz="UTC"),
    catchup=False,
    tags=['tampere', 'temperature'],
) as dag:
    dag.doc_md = __doc__

    def read_config():
        config_filepath = os.environ['TEMPERATURE_DAG_CONFIG']
        config = None
        with open(config_filepath, 'r', encoding='utf-8') as f:
            config = loads(f.read())
        Variable.set('config', dumps(config))

    def get_observations(cfg, start_time, end_time):
        bounding_box = cfg['bounding_box']
        observation_site = cfg['observation_site']

        observations = download_stored_query(
            'fmi::observations::weather::multipointcoverage',
            args=[
                f'bbox={bounding_box}',
                f'starttime={start_time}',
                f'endtime={end_time}'
            ]
        )

        data = observations.data

        observations_dict = {
            'timestamp': [],
            'temperature': []
        }

        for timestamp, observation in data.items():
            observation_temperature = observation[observation_site]['Air temperature']['value']
            observations_dict['timestamp'].append(timestamp)
            observations_dict['temperature'].append(float(observation_temperature))

        dataframe = pd.DataFrame(observations_dict)
        return dataframe

    def plot_observations():
        end_time = dt.datetime.utcnow()
        start_time = end_time - dt.timedelta(hours=1)
        start_time_with_z = f'{start_time.isoformat(timespec="seconds")}Z'
        end_time_with_z = f'{end_time.isoformat(timespec="seconds")}Z'

        config = loads(Variable.get('config'))
        observation_site = config['observation_site']
        plot_directory = config['plot_directory']

        dataframe = get_observations(config, start_time_with_z, end_time_with_z)
        format = mdates.DateFormatter('%H:%M')
        ax = plt.axes()
        ax.xaxis.set_major_formatter(format)
        plt.plot(
            dataframe['timestamp'],
            dataframe['temperature'],
            color='blue',
            marker='o',
            linestyle='solid',
            linewidth=2,
            markersize=12
        )
        plt.legend([u'\u2103'])
        plt.title(f'{observation_site} Air Temperature {end_time_with_z}')
        endtime_for_filename = end_time.strftime('%m%d%Y-%H%M%S')
        filepath = f'{plot_directory}/plot_last_1h_temperature-{endtime_for_filename}.png'
        plt.savefig(filepath)

    read_config_task = PythonOperator(
        task_id='read_config',
        python_callable=read_config,
    )
    read_config_task.doc_md = dedent(
        """\
        #### Read Configuration task
        Read the content of the config.json.
        """
    )

    plot_observations_task = PythonOperator(
        task_id='plot_observations',
        python_callable=plot_observations,
    )
    plot_observations_task.doc_md = dedent(
        """\
        #### Plot observations task
        Plot observations from FMI.
        """
    )

    read_config_task >> plot_observations_task
