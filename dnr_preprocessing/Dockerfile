FROM ubuntu
MAINTAINER Yohannes Gultom modified by DNR Team

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    wget \
    ca-certificates \
    time \
    libglib2.0-0 \
  && rm -rf /var/lib/apt/lists/*

RUN curl -qsSLkO \
    https://repo.continuum.io/miniconda/Miniconda-latest-Linux-`uname -p`.sh \
  && bash Miniconda-latest-Linux-`uname -p`.sh -b \
  && rm Miniconda-latest-Linux-`uname -p`.sh

ENV PATH=/root/miniconda2/bin:$PATH

RUN conda install -y \
    h5py \
    scipy \
    opencv \
    pytables \
  && conda clean --yes --tarballs --packages --source-cache \
  && pip install --upgrade pip \
  && pip install --upgrade -I setuptools \
  && pip install --upgrade pydicom \
  && pip install pandas \
&& pip install git+git://github.com/fchollet/keras.git
	
RUN wget http://www.imagemagick.org/download/ImageMagick-7.0.4-0.tar.gz \
  && tar xzvf ImageMagick-7.0.4-0.tar.gz \
  && cd ImageMagick-7.0.4-0 \
  && ./configure --prefix=/opt/imagemagick-6.8 && make

WORKDIR /
COPY generate_image_labels.py .
COPY subfoldering.py .
COPY preprocess.sh .

RUN chmod 777 generate_image_labels.py
RUN chmod 777 subfoldering.py
RUN chmod 777 preprocess.sh
