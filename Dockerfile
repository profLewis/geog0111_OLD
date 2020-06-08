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
RUN conda env create -f environment.yml
RUN conda activate geog0111 
RUN conda install jupyter
RUN /bin/bash postBuild

# Make RUN commands use the new environment:
ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD = ["/bin/bash","-c"]

