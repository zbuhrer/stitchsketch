# --- Builder Stage ---
FROM python:3.10-alpine as builder

# Install build dependencies
RUN apk update && apk add --no-cache \
    build-base cmake git \
    boost-dev \
    eigen-dev freeimage-dev \
    glog-dev gflags-dev sqlite-dev glew-dev qt5-qtbase-dev qt5-qtdeclarative-dev \
    cgal-dev \
    lapack-dev \
    lz4-dev \
    hdf5-dev \
    openblas-dev \
    tbb-dev \
    suitesparse-dev

# Build and install FLANN
RUN git clone --depth=1 https://github.com/flann-lib/flann.git && \
    cd flann && \
    mkdir build && cd build && \
    cmake .. -DBUILD_PYTHON_BINDINGS=OFF -DBUILD_MATLAB_BINDINGS=OFF -DBUILD_EXAMPLES=OFF -DBUILD_TESTS=OFF -DBUILD_DOC=OFF && \
    make -j$(nproc) && \
    make install && \
    cd ../.. && \
    rm -rf flann

# Build and install METIS 
RUN wget http://glaros.dtc.umn.edu/gkhome/fetch/sw/metis/metis-5.1.0.tar.gz && \
    tar -xzf metis-5.1.0.tar.gz && \
    cd metis-5.1.0 && \
    make config shared=1 && \
    make install && \
    cd .. && \
    rm -rf metis-5.1.0*

# Build and install Ceres
RUN git clone --depth=1 https://github.com/ceres-solver/ceres-solver.git && \
    cd ceres-solver && \
    mkdir build && cd build && \
    cmake .. -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF && \
    make -j$(nproc) && \
    make install && \
    cd ../.. && \
    rm -rf ceres-solver

# Clone COLMAP repository into a dedicated source directory
RUN git clone --depth=1 https://github.com/colmap/colmap.git /opt/colmap

# Build COLMAP with optimized settings
RUN mkdir /opt/colmap/build && cd /opt/colmap/build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DCUDA_ENABLED=OFF -DGUI_ENABLED=OFF && \
    make -j$(nproc) && make install

# --- Final Stage ---
FROM python:3.10-alpine

# Install minimal runtime dependencies
RUN apk update && apk add --no-cache \
    mesa-gl libx11 libxext libsm

# Copy COLMAP binaries and only necessary libraries
COPY --from=builder /usr/local/bin/colmap /usr/local/bin/colmap
COPY --from=builder /usr/local/lib/libcolmap.so* /usr/local/lib/

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies efficiently
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
