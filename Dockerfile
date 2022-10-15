FROM continuumio/miniconda3:4.12.0

# Clone repo and install dependencies
COPY . /skypilot-tutorial

WORKDIR /skypilot-tutorial

# Install tutorial dependencies
RUN pip install -r requirements.txt

# Install SkyPilot + dependencies
RUN conda install -c conda-forge google-cloud-sdk && \
    apt update -y && \
    apt install rsync nano -y && \
    pip install skypilot[aws,gcp] && \
    rm -rf /var/lib/apt/lists/*

# Copy credentials
COPY src/.aws /root/.aws
COPY src/.config/gcloud /root/.config/gcloud

CMD jupyter lab --no-browser --ip "*" --allow-root --notebook-dir=/skypilot-tutorial --NotebookApp.token='' --NotebookApp.password=''
