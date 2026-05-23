# Quick Start Cheat Sheet

## 🎯 TL;DR - One-Liner Commands

### Docker Mode (Recommended for CI/CD)
```bash
make docker-mode      # ✅ Start everything
make docker-logs      # 📊 View logs
make docker-mode-stop # 🛑 Stop everything
```

### Local DB Mode (Recommended for local development)
```bash
make local-db-mode      # ✅ Start everything (needs local Postgres)
make local-db-logs      # 📊 View logs
make local-db-mode-stop # 🛑 Stop everything
```

---

## 🔍 Verify Everything Works

### Docker Mode
```bash
# Check FastAPI is running
curl http://localhost:1337/health

# Check Postgres connection
docker compose exec postgres_db psql -U fastapi_app_user_001 -d fastapi_project_db_v1 -c "SELECT NOW();"

# Check MongoDB
docker compose exec mongo_db mongosh --eval "db.adminCommand('ping')"
```

### Local DB Mode
```bash
# Check FastAPI is running
curl http://localhost:1337/health

# Check local Postgres (must be running)
psql -h 127.0.0.1 -U fastapi_app_user_001 -d fastapi_project_db_v1 -c "SELECT NOW();"

# Check MongoDB
docker compose exec mongo_db mongosh --eval "db.adminCommand('ping')"
```

---

## 🔄 Switching Between Modes

### From Docker → Local
```bash
make docker-mode-stop       # Stop Docker services
# Ensure local Postgres has the user/database (see ENVIRONMENT_SETUP.md)
make local-db-mode          # Start Local DB mode
```

### From Local → Docker
```bash
make local-db-mode-stop     # Stop Local DB mode
make docker-mode            # Start Docker mode (auto-init Postgres)
```

---

## 📂 Files Overview

### Environment Files
- `.env` — Template (use for reference)
- `.env.docker` — Docker mode (all services in containers)
- `.env.localdb` — Local mode (local Postgres + Docker MongoDB)

### Compose Files
- `docker-compose.yml` — Main (used by both modes)
- `docker-compose.localdb.yml` — Override for local mode (skips postgres_db dependency)

### Documentation
- `ENVIRONMENT_SETUP.md` — Full setup guide with troubleshooting
- `QUICK_START.md` — This file!

### Data Directories
- `.docker/postgres-data` — Docker Postgres volume (isolated)
- `.docker/mongo-data` — Docker MongoDB volume (isolated)
- Local system Postgres — Used in local mode (separate from Docker)

---

## 🆘 Quick Troubleshooting

| Issue | Docker Mode | Local Mode |
|-------|-------------|-----------|
| Postgres won't connect | `docker compose logs postgres_db \| tail -50` | `psql -h 127.0.0.1 -U postgres -d postgres -c "\du"` |
| FastAPI crash loop | `docker compose logs fastapi_server` | Same as Docker |
| MongoDB not responding | `docker compose logs mongo_db` | Same as Docker |
| Reset everything | `make docker-mode-stop && docker volume rm fastapi-v1_postgres_data` | `make local-db-mode-stop` |

---

## 📋 Environment Variables

Both `.env.docker` and `.env.localdb` use the same database credentials for seamless switching:
- **Username:** `fastapi_app_user_001`
- **Password:** `rO2ry5dafKdgRTnamN4CYSZx8lqmpfM50GZMGWLP`
- **Database:** `fastapi_project_db_v1`
- **Port:** `5432`

The only difference is the **host**:
- Docker mode: `postgres_db` (container DNS)
- Local mode: `127.0.0.1` (host machine)

---

## 🚀 Your Setup is Ready!

✅ Docker volumes are isolated (won't interfere with local Postgres)  
✅ Seamless mode switching with one command  
✅ Easy-to-use `make` commands  
✅ Documentation included  

**Next steps:**
1. Run `make docker-mode` to verify Docker mode works ✓ (already tested!)
2. Set up your local Postgres and run `make local-db-mode` when ready
3. See `ENVIRONMENT_SETUP.md` for detailed instructions

