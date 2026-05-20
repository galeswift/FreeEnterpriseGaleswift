# Step 1 — Test Locally

Before deploying to a real server, test the build on your own machine using Docker Desktop. This confirms everything works without needing a server, a domain, or SSL.

**What you need:**
- ⚠️ A legally obtained FF4 US v1.1 headerless ROM file (`ff4.smc`)

---

**1. Install Docker Desktop:** Download from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/) and install it. Once installed, make sure it's running (you should see the Docker whale icon in your system tray).

**2. Download the config files:** Clone or download this repository onto your machine. Open a terminal in the `docker/` folder containing `Dockerfile`, `docker-compose.local.yml`, etc.

If you have git installed:
```bash
git clone <your-repo-url>
cd <repo-name>/docker
```

Otherwise download the ZIP from GitHub, extract it, and open a terminal in the `docker/` folder.

**3. Add your ROM file:** Create a `rom` folder inside the `docker/` folder, then copy your ROM into it with the exact filename `ff4.smc`. 📋 The filename must be exactly `ff4.smc` — the server won't start if it's named anything else.

On Windows you can do this in File Explorer — create a folder named `rom` inside the `docker/` folder and drag your ROM file in, renaming it to `ff4.smc` if needed.

Your folder should look like this:
```
docker/
├── Dockerfile
├── Caddyfile
├── docker-compose.yml
├── docker-compose.local.yml
└── rom/
    └── ff4.smc
```

**4. Start the containers:**
```bash
docker compose -f docker-compose.local.yml up
```

⏳ The first run takes several minutes while Docker builds the image — this is normal, don't close the terminal. Once you see log output from FreeEnt, visit `http://localhost:8080`. If the randomizer loads, the setup is working. Press `Ctrl+C` to stop.

---

If the local test passes, continue to [Step 2 — Deploy on a Server](Step2.md).
