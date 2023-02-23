FROM mambaorg/micromamba:latest
LABEL image.name="jodyphelan/simple-rif-rf"

# This needs to be set for the PATH variable to be set correctly
ARG MAMBA_DOCKERFILE_ACTIVATE=1

# Install our software
RUN micromamba install -y -n base -c bioconda -c conda-forge \
    scikit-learn=1.2.1 \
    bcftools=1.16 \
    tqdm && \
    micromamba clean --all --yes

# create a directory for the internal data used by the container
USER root
RUN mkdir /internal_data /data

# copy the model, data files, and scripts
COPY model.pkl /internal_data/model.pkl
COPY predict.py /internal_data

# set `/data` as working directory so that the output is written to the
# mount point when run with `docker run -v $PWD:/data ... -o output.csv`
WORKDIR /data

ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "python", "/internal_data/predict.py", "--model", "/internal_data/model.pkl"]
