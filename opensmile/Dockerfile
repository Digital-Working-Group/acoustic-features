FROM ubuntu:24.04

# Install Python 3.10 and pip
RUN apt-get update && \ 
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.9 python3.9-venv python3.9-dev && \
    python3.9 -m ensurepip && \
    python3.9 -m pip install --upgrade pip 

RUN rm /usr/bin/python3 && \
    ln -s python3.9 /usr/bin/python3
# RUN python3 -m venv /opt/venv
# ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /scripts
COPY python39_requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt