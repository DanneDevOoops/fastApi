# FastAPI Environment Setup Guide

This project supports **two seamless development modes**: Docker-based and local database.

---

## 🚀 Quick Start

### Mode 1: Docker (Recommended for CI/CD & team collaboration)

All services (FastAPI, Postgres, MongoDB) run in Docker containers with **isolated volumes**.

```bash
cd /Users/daniel/PycharmProjects/fastApi-v1

# Start all services
docker compose --env-file .env.docker up -d

# View logs
docker compose logs -f fastapi_server

# Stop services
docker compose --env-file .env.docker down
```

**Environment file:** `.env.docker`  
**Database:** Docker Postgres at `postgres_db:5432` (container DNS)  
**Volume:** `.docker/postgres-data` (isolated, won't affect local Postgres)  

---

### Mode 2: Local Database (Recommended for local development)

FastAPI + MongoDB run in Docker; **Postgres runs on your host machine**.

**Prerequisites:**
- Local Postgres server running on `127.0.0.1:5432`
- Same credentials configured in local Postgres:
  ```sql
  CREATE ROLE fastapi_app_user_001 WITH LOGIN PASSWORD 'rO2ry5dafKdgRTnamN4CYSZx8lqmpfM50GZMGWLP';
  CREATE DATABASE fastapi_project_db_v1 OWNER fastapi_app_user_001;
  ```

**Start:**
```bash
cd /Users/daniel/PycharmProjects/fastApi-v1

# Start FastAPI + MongoDB only (skips postgres_db container)
docker compose --env-file .env.localdb -f docker-compose.yml -f docker-compose.localdb.yml up -d

# View logs
docker compose -f docker-compose.yml -f docker-compose.localdb.yml logs -f fastapi_server

# Stop
docker compose -f docker-compose.yml -f docker-compose.localdb.yml down
```

**Environment file:** `.env.localdb`  
**Database:** Local Postgres at `127.0.0.1:5432`  
**MongoDB:** Docker container (shared with Mode 1)  

---

## 📋 Environment Files

| File | Mode | Postgres Host | MongoDB Host | Data Directory |
|------|------|---------------|--------------|-----------------|
| `.env.docker` | Docker | `postgres_db` (Docker) | `mongo_db` (Docker) | `.docker/postgres-data` |
| `.env.localdb` | Local | `127.0.0.1` (Host) | `mongo_db` (Docker) | Local system Postgres |
| `.env` | Template | `postgres_db` (Docker) | `mongo_db` (Docker) | `.docker/postgres-data` |

---

## 🗂️ Docker Compose Files

- **`docker-compose.yml`** — Main compose file (used by both modes)
- **`docker-compose.localdb.yml`** — Override file (used only in local mode)
  - Removes `postgres_db` from `fastapi_server` dependencies
  - Allows FastAPI to connect to local Postgres

---

## 🔧 Switching Between Modes

### From Docker → Local

```bash
# Stop Docker services
docker compose --env-file .env.docker down

# Ensure local Postgres is running and has the required role/database
psql -U postgres -c "CREATE ROLE fastapi_app_user_001 WITH LOGIN PASSWORD 'rO2ry5dafKdgRTnamN4CYSZx8lqmpfM50GZMGWLP';"
psql -U postgres -c "CREATE DATABASE fastapi_project_db_v1 OWNER fastapi_app_user_001;"

# Start in local mode
docker compose --env-file .env.localdb -f docker-compose.yml -f docker-compose.localdb.yml up -d
```

### From Local → Docker

```bash
# Stop local mode services
docker compose -f docker-compose.yml -f docker-compose.localdb.yml down

# Start Docker mode (auto-initializes Postgres with correct user/password)
docker compose --env-file .env.docker up -d
```

---

## 🧪 Verify Connectivity

### Docker Mode

```bash
# Test Postgres connection
docker compose --env-file .env.docker exec postgres_db psql -U fastapi_app_user_001 -d fastapi_project_db_v1 -c "SELECT NOW();"

# Test FastAPI
curl http://localhost:1337/health
```

### Local Mode

```bash
# Test local Postgres
psql -h 127.0.0.1 -U fastapi_app_user_001 -d fastapi_project_db_v1 -c "SELECT NOW();"

# Test FastAPI
curl http://localhost:1337/health
```

---

## 📌 Important Notes

1. **Data Isolation:** Docker mode uses `.docker/postgres-data` — it won't affect your local Postgres installation.
2. **Backup:** The original corrupted volume is backed up at `/Users/daniel/Library/Application Support/Postgres/var-16.backup`.
3. **Credentials:** Both modes use identical credentials for seamless switching.
4. **MongoDB:** Both modes use the same Docker MongoDB container (isolated volume: `.docker/mongo-data`).

---

## 🆘 Troubleshooting

### Postgres connection fails in Docker mode

```bash
# Check container status
docker compose ps

# View Postgres logs
docker compose logs postgres_db | tail -100

# Verify user exists
docker compose exec postgres_db psql -U postgres -d postgres -c "\du"
```

### Postgres connection fails in Local mode

```bash
# Check local Postgres is running
psql -U postgres -d postgres -c "SELECT NOW();"

# Verify role exists
psql -U postgres -d postgres -c "\du"

# Check .env.localdb has correct PG_DB_HOST=127.0.0.1
cat .env.localdb | grep PG_DB_HOST
```

### Reset everything (clean slate)

```bash
# Stop all containers
docker compose --env-file .env.docker down

# Remove Docker volumes
docker volume rm fastapi-v1_postgres_data fastapi-v1_mongo_db_data

# Restart
docker compose --env-file .env.docker up -d
```

---

## 📚 References

- Docker Compose docs: https://docs.docker.com/compose/
- PostgreSQL docs: https://www.postgresql.org/docs/
- FastAPI docs: https://fastapi.tiangolo.com/

