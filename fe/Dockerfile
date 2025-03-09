FROM python:3.10-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake git \
    libboost-all-dev \
    libeigen3-dev \
    libfreeimage-dev \
    libgoogle-glog-dev \
    libgflags-dev \
    libsqlite3-dev \
    libglew-dev \
    qtbase5-dev qtdeclarative5-dev \
    libcgal-dev \
    liblapack-dev \
    liblz4-dev \
    libhdf5-dev \
    libopenblas-dev \
    libtbb-dev \
    libsuitesparse-dev \
    libmetis-dev \
    libceres-dev \
    libflann-dev

# Clone COLMAP repository into a dedicated source directory
RUN git clone --depth=1 https://github.com/colmap/colmap.git /opt/colmap

# Build COLMAP with optimized settings
RUN mkdir /opt/colmap/build && cd /opt/colmap/build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DCUDA_ENABLED=OFF -DGUI_ENABLED=OFF && \
    make -j$(nproc) && make install

# --- Final Stage ---
FROM python:3.10-slim

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-dri libx11-6 libxext6 libsm6

# Copy COLMAP binaries and only necessary libraries
COPY --from=builder /usr/local/bin/colmap /usr/local/bin/colmap
COPY --from=builder /usr/local/lib/libcolmap.so* /usr/local/lib/
COPY --from=builder /usr/local/lib/libmetis.so* /usr/local/lib/

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
