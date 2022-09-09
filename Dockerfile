FROM continuumio/miniconda3:4.12.0

# Clone repo and install dependencies
RUN git clone https://github.com/skypilot-org/skypilot-tutorial.git && \
    cd skypilot-tutorial && \
    pip install -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

CMD jupyter lab --no-browser --ip "*" --allow-root --notebook-dir=/skypilot-tutorial --NotebookApp.token='' --NotebookApp.password=''
