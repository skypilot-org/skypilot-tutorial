FROM continuumio/miniconda3:4.12.0

WORKDIR /skypilot-tutorial

ADD ./requirements.txt /skypilot-tutorial/requirements.txt

# Install tutorial dependencies
RUN pip install -r requirements.txt

# Install SkyPilot + dependencies
RUN conda install -c conda-forge google-cloud-sdk && \
    apt update -y && \
    apt install rsync nano -y && \
    pip install skypilot[aws,gcp] && \
    rm -rf /var/lib/apt/lists/*

# Copy credentials.
# UPDATE - no longer required. Instead mount the .aws and .config dirs to /credentials and it will be copied over.
# COPY src/.aws /root/.aws
# COPY src/.config/gcloud /root/.config/gcloud

# Exclude usage logging message
RUN mkdir -p /root/.sky && touch /root/.sky/privacy_policy

# Add files which may change frequently
COPY . /skypilot-tutorial

# Set bash as default shell
ENV SHELL /bin/bash

CMD ["/bin/bash", "-c", "cp -a /credentials/. /root/;sky show-gpus;jupyter lab --no-browser --ip '*' --allow-root --notebook-dir=/skypilot-tutorial --NotebookApp.token='SkyCamp2022'"]
