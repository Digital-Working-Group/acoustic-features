FROM continuumio/miniconda3
RUN conda create -y -n env python=3.9.6
RUN echo "source activate env" > ~/.bashrc
ENV PATH /opt/conda/envs/env/bin:$PATH
WORKDIR /scripts
COPY python3-9-6_requirements.txt .
RUN pip install --no-cache-dir -r python3-9-6_requirements.txt
