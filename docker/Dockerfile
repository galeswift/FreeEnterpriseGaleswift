FROM python:3.8-slim

WORKDIR /app

# System deps for compiling Floating IPS
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy local source (ie: whatever branch you have synched locally)
COPY . .

# Patch hardcoded MongoDB host to use the Docker service name instead of localhost
RUN sed -i 's|mongodb://127.0.0.1:27017|mongodb://mongo:27017|g' /app/FreeEnt/server/server.py

# Patch CherryPy to bind on all interfaces so Docker port forwarding can reach it
RUN sed -i "s/cherrypy.config.update({'server.socket_port' : config.port})/cherrypy.config.update({'server.socket_port': config.port, 'server.socket_host': '0.0.0.0'})/g" /app/FreeEnt/server/website.py

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set up fe.pth so `python -m FreeEnt` can find the module
RUN echo "/app" > $(python -c "import site; print(site.getsitepackages()[0])")/fe.pth

# Build Floating IPS (headless) and place it where FreeEnt expects it
RUN wget -q https://github.com/Alcaro/Flips/archive/refs/heads/master.tar.gz -O flips.tar.gz && \
    tar xf flips.tar.gz && \
    cd Flips-master && \
    TARGET=cli make && \
    mkdir -p /app/FreeEnt/server/bin && \
    cp flips /app/FreeEnt/server/bin/flips-linux && \
    chmod +x /app/FreeEnt/server/bin/flips-linux && \
    cd .. && rm -rf Flips-master flips.tar.gz

# Fix CRLF line endings from Windows checkout before running shell scripts
RUN find /app -name "*.sh" -exec sed -i 's/\r$//' {} +

# Compile the randomizer spec files (required before server can run)
RUN cd /app/FreeEnt && bash compile_all_specs.sh

# ROM is mounted at runtime — not baked into the image
CMD ["python", "-m", "FreeEnt", "/rom/ff4.smc", "server"]
