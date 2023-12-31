ARG     PYTHON_TAG
FROM    python:${PYTHON_TAG}

ARG     DOCKER_GROUP_ID
ARG     USER="dev"
ARG     KUBECTL_VERSION="v1.27.1"
ARG     HELM_VERSION="v3.12.3"
ARG     APACHE_AIRFLOW_VERSION="2.7.3"
ARG     KUBERNETES_VERSION="28.1.0"
ARG     VIRTUALENV_VERSION="20.25.0"
ARG     PANDAS_VERSION="2.1.4"
ARG     FMI_OPEN_DATA_VERSION="0.4.3"
ARG     MATPLOTLIB_VERSION="3.8.2"
ARG     NUMPY_VERSION="1.26.2"

RUN     apk add build-base \
                curl \
                doas \
                docker \
                gcc \
                git \
                linux-headers \
                make \
                py3-pybind11-dev \
                openssh \
                re2-dev \
                s2geometry-dev \
                shadow \
                sqlite \
                sqlite-dev \
                vim && \
        adduser -D ${USER} && \
        addgroup ${USER} docker && \
        groupmod --gid ${DOCKER_GROUP_ID} docker && \
        git config --global core.editor "vim" && \
        curl -LO https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl && \
        chmod +x kubectl && \
        mv kubectl /usr/local/bin/kubectl && \
        curl -LO https://get.helm.sh/helm-${HELM_VERSION}-linux-amd64.tar.gz && \
        tar -zxvf helm-${HELM_VERSION}-linux-amd64.tar.gz && \
        mv linux-amd64/helm /usr/local/bin/helm && \
        pip install apache-airflow==${APACHE_AIRFLOW_VERSION} \
                    kubernetes==${KUBERNETES_VERSION} \
                    virtualenv==${VIRTUALENV_VERSION} \
                    pandas==${PANDAS_VERSION} \
                    fmiopendata==${FMI_OPEN_DATA_VERSION} \
                    matplotlib==${MATPLOTLIB_VERSION} \
                    numpy==${NUMPY_VERSION}
