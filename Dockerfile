FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "geog0111", "/bin/bash", "-c"]

# Make sure the environment is activated:
RUN echo "Make sure gdal is installed:"
RUN python -c "import gdal"

# The code to run when container is started:
COPY run.py .
ENTRYPOINT ["conda", "run", "-n", "geog0111", "python", "run.py"]
