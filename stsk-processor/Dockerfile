FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    cmake \
    build-essential \
    ninja-build \
    libboost-program-options-dev \
    libboost-filesystem-dev \
    libboost-graph-dev \
    libboost-system-dev \
    libboost-test-dev \
    libeigen3-dev \
    libsuitesparse-dev \
    libfreeimage-dev \
    libgoogle-glog-dev \
    libgflags-dev \
    libglew-dev \
    qtbase5-dev \
    libqt5opengl5-dev \
    libcgal-dev \
    libcgal-qt5-dev \
    libflann-dev \
    libatlas-base-dev \
    libsuitesparse-dev \
    python3 \
    python3-pip \
    libsqlite3-dev \
    libceres-dev \ 
    libmetis-dev \
    libmariadbclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Set MYSQLCLIENT_CFLAGS and MYSQLCLIENT_LDFLAGS
RUN echo "export MYSQLCLIENT_CFLAGS=`mysql_config --cflags`" >> /etc/profile.d/mysqlclient.sh && \
    echo "export MYSQLCLIENT_LDFLAGS=`mysql_config --libs`" >> /etc/profile.d/mysqlclient.sh

# Clone and build COLMAP
RUN git clone https://github.com/colmap/colmap.git
WORKDIR /colmap
RUN mkdir build \
    && cd build \
    && cmake .. -GNinja \
    && ninja -j2 \
    && ninja install

WORKDIR /app

COPY requirements.txt .
RUN . /etc/profile.d/mysqlclient.sh && pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
