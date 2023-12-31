include make.properties

.DEFAULT_GOAL := help
.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[34m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Airflow

airflow-setup: ## Airflow Setup
	AIRFLOW_HOME="${AIRFLOW_HOME}" DAG_FOLDER="${DAG_FOLDER}" TZ="${TZ}" airflow db migrate &&\
	AIRFLOW_HOME="${AIRFLOW_HOME}" TZ="${TZ}" airflow users  create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin &&\
	sed -i '/^dags_folder.*/c\dags_folder = ${DAG_FOLDER}' "${AIRFLOW_HOME}/airflow.cfg" && \
	sed -i '/^load_examples.*/c\load_examples = False' "${AIRFLOW_HOME}/airflow.cfg"

airflow-start-scheduler: ## Airflow Start Scheduler
	AIRFLOW_HOME="${AIRFLOW_HOME}" TZ="${TZ}" TEMPERATURE_DAG_CONFIG="${TEMPERATURE_DAG_CONFIG}" airflow scheduler

airflow-start-webserver: ## Airflow Start Webserver
	AIRFLOW_HOME="${AIRFLOW_HOME}" TZ="${TZ}" TEMPERATURE_DAG_CONFIG="${TEMPERATURE_DAG_CONFIG}" airflow webserver