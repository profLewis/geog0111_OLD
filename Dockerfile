FROM continuumio/miniconda3

LABEL maintainer="p.lewis@ucl.ac.uk"
LABEL coursename="GEOG0111"
LABEL department="Geography"
LABEL university="UCL"
LABEL version="1.0"

#
WORKDIR /home/user

# add notebooks to <WORKDIR>
ADD *.ipynb geog0111
ADD images geog0111
ADD data geog0111

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
ENTRYPOINT [ "/usr/bin/tini", "--" ]
SHELL ["conda", "run", "-n", "geog0111", "/bin/bash", "-c"]
RUN /opt/conda/bin/jupyter notebook --notebook-dir=/home/user/geog0111 --ip=0.0.0.0 --port=8888 --no-browser  --allow-root

