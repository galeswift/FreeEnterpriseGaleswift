# Builds the Free Enterprise server. Used by docker/docker-compose.local.yml for local runs, and by
# Coolify for ff4fe.galeswift.com (build context: the repo root).
FROM python:3.8.20-slim-bookworm

WORKDIR /app

# System deps for compiling Floating IPS; wget is also what Coolify's health check uses
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies, pinned to the versions the old droplet ran
COPY requirements.txt docker/constraints.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt -c constraints.txt

# Set up fe.pth so `python -m FreeEnt` can find the module
RUN echo "/app" > $(python -c "import site; print(site.getsitepackages()[0])")/fe.pth

# Build Floating IPS (headless) from a pinned commit and place it where FreeEnt expects it
ARG FLIPS_COMMIT=ff216a75df0987047a67d7923567dc4482ce07ac
RUN wget -q https://github.com/Alcaro/Flips/archive/${FLIPS_COMMIT}.tar.gz -O flips.tar.gz && \
    tar xf flips.tar.gz && \
    cd Flips-${FLIPS_COMMIT} && \
    TARGET=cli make && \
    mkdir -p /opt/flips && \
    cp flips /opt/flips/flips-linux && \
    cd .. && rm -rf Flips-${FLIPS_COMMIT} flips.tar.gz

# Copy local source (ie: whatever branch you have synched locally)
COPY . .
RUN mkdir -p FreeEnt/server/bin && cp /opt/flips/flips-linux FreeEnt/server/bin/flips-linux

# Fix CRLF line endings from Windows checkout before running shell scripts
RUN find /app -name "*.sh" -exec sed -i 's/\r$//' {} +

# Compile the randomizer spec files (required before server can run)
RUN cd /app/FreeEnt && bash compile_all_specs.sh

# Run as an unprivileged user. It owns /app (for the generator's cache in FreeEnt/server/_build),
# but not the ROM or anything mounted in from the host, so those stay read-only.
RUN useradd --create-home --uid 1000 fe && chown -R fe:fe /app
USER fe

# Listen on all interfaces so the proxy can reach the server. MongoDB comes from FE_MONGO_URL.
ENV FE_LISTEN_HOST=0.0.0.0
EXPOSE 8080

# ROM is mounted at runtime — not baked into the image
CMD ["python", "-m", "FreeEnt", "/rom/ff4.smc", "server"]
