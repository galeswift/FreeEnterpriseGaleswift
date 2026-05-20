FROM python:3.8-slim

WORKDIR /app

# System deps: git to clone repo, gcc/make to compile Floating IPS
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    g++ \
    make \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Clone FreeEnterprise4
RUN git clone --branch main --depth 1 \
    https://github.com/HungryTenor/FreeEnterprise4.git .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set up fe.pth so `python -m FreeEnt` can find the module
RUN echo "/app" > $(python -c "import site; print(site.getsitepackages()[0])")/fe.pth

# Build Floating IPS (headless) and place it where FreeEnt expects it
RUN wget -q https://github.com/Alcaro/Flips/archive/refs/heads/master.tar.gz -O flips.tar.gz && \
    tar xf flips.tar.gz && \
    cd Flips-master && \
    make NOGUI=1 && \
    mkdir -p /app/FreeEnt/server/bin && \
    cp flips /app/FreeEnt/server/bin/flips-linux && \
    chmod +x /app/FreeEnt/server/bin/flips-linux && \
    cd .. && rm -rf Flips-master flips.tar.gz

# Compile the randomizer spec files (required before server can run)
RUN cd /app/FreeEnt && bash compile_all_specs.sh

# ROM is mounted at runtime — not baked into the image
ENTRYPOINT ["python", "-m", "FreeEnt", "/rom/ff4.smc", "server"]
