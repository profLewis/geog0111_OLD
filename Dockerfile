FROM continuumio/miniconda3

LABEL maintainer="p.lewis@ucl.ac.uk"
LABEL coursename="GEOG0111"
LABEL department="Geography"
LABEL university="UCL"
LABEL version="1.0"

#
WORKDIR /home/user

# add notebooks to <WORKDIR>
ADD *.ipynb geog0111/
ADD images geog0111/
ADD data geog0111/

# Create the environment:
COPY environment.yml .
COPY postBuild .

# create env geog0111
RUN conda update -n base -c defaults conda
RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "geog0111", "/bin/bash", "-c"]
RUN conda install jupyter

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "geog0111", "/bin/bash"]
RUN postBuild

# The code to run when container is started:
ENTRYPOINT ["conda", "run", "-n", "geog0111", "jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
