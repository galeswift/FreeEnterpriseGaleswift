# Getting started #
1. Install docker for windows: <code>https://docs.docker.com/desktop/setup/install/windows-install/</code>
2. Make a folder called 'rom'
3. Place your copy of the <code>ff4.smc</code> ROM into that folder
4. Open a command prompt into the root FreeEnterprise folder (one level up from where the docker folder is)
5. Run the container with the following command:
<code>docker compose -f docker/docker-compose.local.yml up --build</code>
6. Open a browser to <code>http://localhost:8080</code> (after a few minutes, or you can check the logs to see when the server gets up)

# Updating the build #
If you want to update the site after building, run the following
<code>docker compose -f docker/docker-compose.local.yml up --build -d</code>