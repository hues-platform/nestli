FROM python:3.8-slim-buster

ARG ENERGYPLUS_VERSION=9.3.0
ARG ENERGYPLUS_TAG=v9.3.0
ARG ENERGYPLUS_SHA=baff08990c
ARG ENERGYPLUS_INSTALL_VERSION=9-3-0
ARG ENERGYPLUS_INSTALL_SYMLINK_VERSION=9-3
ENV ENERGYPLUS_VERSION=$ENERGYPLUS_VERSION
ENV ENERGYPLUS_TAG=v$ENERGYPLUS_VERSION
ENV ENERGYPLUS_SHA=$ENERGYPLUS_SHA

ENV ENERGYPLUS_INSTALL_VERSION=$ENERGYPLUS_INSTALL_VERSION


# INSTALL EnergyPlus
# Downloading from Github
ENV ENERGYPLUS_DOWNLOAD_BASE_URL https://github.com/NREL/EnergyPlus/releases/download/$ENERGYPLUS_TAG
ENV ENERGYPLUS_DOWNLOAD_FILENAME EnergyPlus-$ENERGYPLUS_VERSION-$ENERGYPLUS_SHA-Linux-x86_64.sh
ENV ENERGYPLUS_DOWNLOAD_URL $ENERGYPLUS_DOWNLOAD_BASE_URL/$ENERGYPLUS_DOWNLOAD_FILENAME

# System deps:
# Collapse the update of packages, download and installation into one command
# to make the container smaller & remove a bunch of the auxiliary apps/files
# that are not needed in the container
RUN apt-get update && apt-get install -y ca-certificates curl git \
    && curl -SLO $ENERGYPLUS_DOWNLOAD_URL \
    && chmod +x $ENERGYPLUS_DOWNLOAD_FILENAME \
    && echo "y\r" | ./$ENERGYPLUS_DOWNLOAD_FILENAME \
    && rm $ENERGYPLUS_DOWNLOAD_FILENAME \
    && cd /usr/local/EnergyPlus-$ENERGYPLUS_INSTALL_VERSION \
    && rm -rf DataSets Documentation ExampleFiles WeatherData MacroDataSets PostProcess/convertESOMTRpgm \
    PostProcess/EP-Compare PreProcess/FMUParser PreProcess/ParametricPreProcessor PreProcess/IDFVersionUpdater \
	  && ln -s /usr/local/EnergyPlus-$ENERGYPLUS_INSTALL_VERSION /usr/local/EnergyPlus-$ENERGYPLUS_INSTALL_SYMLINK_VERSION
RUN apt-get remove --purge -y curl ca-certificates \
    && apt-get autoremove -y --purge \
	  # Remove the broken symlinks
	  && cd /usr/local/bin \
	  && find -L . -type l -delete \
	  && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/local/dtpy
ENV TEMP=/tmp/

COPY . . 

RUN pip install -r requirements.txt

CMD ["python3", "mosaik_umar_simulation.py"]

