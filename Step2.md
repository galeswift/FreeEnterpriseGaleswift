# Step 2 — Deploy on a Server

> Complete [Step 1 — Test Locally](Step1.md) before continuing. This confirms the build works before you touch a real server.

This guide deploys the FF4FE randomizer server to a Linux VM with a public domain and HTTPS. Docker handles Python, MongoDB, and SSL automatically.

**Overview:**
1. Prepare the server (install Docker + open firewall)
2. Get the files ready (download config, add ROM, set domain)
3. Launch

---

**What you need:**
- A Linux server with a public IP (DigitalOcean, Linode, AWS, etc.)
- A domain name with a subdomain pointed at your server (e.g. `ff4fe.yourdomain.com`)
- A legally obtained FF4 US v1.1 headerless ROM file (`ff4.smc`)

> 💡 **Tip:** If you already have a website/domain, you can skip straight to Step 1.

## Setting Up a Domain Name

A domain name is required for the live server — SSL certificates (HTTPS) are tied to a domain, and Caddy won't start without one.

### Registering a Domain

If you don't already have a domain, register one through any registrar:
- **Namecheap** — cheap, straightforward
- **Cloudflare** — sells domains at cost, good DNS tooling
- **Google Domains (now Squarespace)** — simple interface

A `.com` domain costs ~$10-15/year. Alternatively, if you already own a domain (e.g. `yourdomain.com`), you can create a free subdomain for this server without buying anything new.

### Pointing Your Domain at the Server

Once you have a domain and a server IP address, create a DNS **A record**:

| Type | Name | Value | TTL |
|---|---|---|---|
| A | `ff4fe` | `your.server.ip` | 3600 |

This makes `ff4fe.yourdomain.com` resolve to your server. Where to add this depends on your registrar — look for "DNS Management" or "DNS Records" in their control panel.

**DNS propagation** takes anywhere from a few minutes to 48 hours, though usually under 30 minutes. You can check if it's ready with:

```bash
nslookup ff4fe.yourdomain.com
```

It should return your server's IP. ⚠️ Don't start the server until this resolves correctly — Caddy needs to reach Let's Encrypt to issue the certificate, and Let's Encrypt will check that the domain points to your server.

---

## Step 1 — Prepare the Server

SSH into your server and install Docker:

```bash
curl -fsSL https://get.docker.com | sh
```

Verify it worked:

```bash
docker --version
docker compose version
```

Then open the firewall ports Caddy needs for SSL, and keep SSH open so you don't lock yourself out:

```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
sudo ufw status
```

You should see ports 22, 80, and 443 listed as `ALLOW`.

---

## Step 2 — Get the Files Ready

Clone the repository onto your server:

```bash
git clone <your-repo-url> ff4fe-server
cd ff4fe-server/docker
```

Add your ROM file:

```bash
mkdir rom
cp /path/to/your/rom.smc rom/ff4.smc
```

Edit `Caddyfile` and replace `ff4fe.yourdomain.com` with your actual domain:

```bash
nano Caddyfile
```

Save and close (`Ctrl+X`, then `Y`, then `Enter`).

Your folder should look like this:

```
ff4fe-server/
└── docker/
    ├── Dockerfile
    ├── Caddyfile
    ├── docker-compose.yml
    └── rom/
        └── ff4.smc
```

---

## Step 3 — Launch

```bash
docker compose up -d
```

⏳ The first run takes several minutes — Docker is building the FreeEnt image, which includes cloning the repository, installing Python packages, compiling Floating IPS, and compiling the randomizer specs. Subsequent starts are instant.

Watch the build progress:

```bash
docker compose logs -f
```

Once you see `freeent` logging activity and `caddy` reports that it obtained a certificate, your server is live. Visit `https://ff4fe.yourdomain.com` to confirm.

---

## Updating FreeEnt

When a new version of the FreeEnt code is released, rebuild the image:

```bash
docker compose pull                           # update Caddy and MongoDB images
docker compose build --no-cache freeent      # rebuild FreeEnt from latest code
docker compose up -d                          # restart with new image
```

---

## Useful Commands

```bash
# Check status of all services
docker compose ps

# View live logs
docker compose logs -f

# View logs for one service only
docker compose logs -f freeent

# Restart a single service
docker compose restart freeent

# Stop everything
docker compose down

# Stop everything and delete all data (including MongoDB)
docker compose down -v
```

---

## Troubleshooting

**Site returns "Bad Gateway"**
The FreeEnt container isn't running or hasn't finished starting. Check logs:
```bash
docker compose logs freeent
```
Common cause: the ROM file is missing or named incorrectly. Confirm `rom/ff4.smc` exists.

**SSL certificate not issued / site shows certificate warning**
Caddy couldn't reach Let's Encrypt. Make sure:
- Your domain's DNS points to this server's IP
- Ports 80 and 443 are open (`sudo ufw status`)
- You waited a minute after `docker compose up` for the cert to be issued

**Build fails during `compile_all_specs.sh`**
Check the full error output with `docker compose logs freeent`. If it's a missing dependency, open a GitHub issue on the FreeEnt repo.

**MongoDB connection errors in FreeEnt logs**
The `mongo` container may still be starting when `freeent` starts. This usually resolves on its own within 30 seconds. If it persists:
```bash
docker compose restart freeent
```
