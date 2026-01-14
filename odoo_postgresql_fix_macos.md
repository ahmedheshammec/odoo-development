# Fixing PostgreSQL Connection Issues for Odoo 18 on macOS (Homebrew)

This document explains how we diagnosed and fixed a **PostgreSQL not running / socket error**
when starting **Odoo 18** on **macOS (Apple Silicon)** using **Homebrew PostgreSQL 17**.

---

## ❌ Original Error

When starting Odoo:

```text
psycopg2.OperationalError:
connection to server on socket "/tmp/.s.PGSQL.5432" failed:
No such file or directory
Is the server running locally and accepting connections on that socket?
```

This indicates that **PostgreSQL is not running**, or Odoo cannot reach it.

---

## Step 1 — Confirm PostgreSQL Is Not Running

```bash
ps aux | grep postgres
```

If you only see `grep` itself, PostgreSQL is **not running**.

---

## Step 2 — Identify a Stale `postmaster.pid`

Trying to start PostgreSQL may show:

```text
FATAL: lock file "postmaster.pid" already exists
HINT: Is another postmaster (PID XXX) running?
```

But checking the PID:

```bash
ps -p <PID> -o pid,command
```

Shows **not postgres** → this means PostgreSQL crashed earlier and left a **stale lock file**.

---

## Step 3 — Safely Remove the Stale Lock File

⚠️ Only do this if PostgreSQL is NOT running.

```bash
rm -f /opt/homebrew/var/postgresql@17/postmaster.pid
```

Verify:

```bash
ls /opt/homebrew/var/postgresql@17/postmaster.pid
# No such file or directory
```

---

## Step 4 — Start PostgreSQL Manually (Authoritative)

```bash
pg_ctl -D /opt/homebrew/var/postgresql@17 start
```

Expected successful output:

```text
database system is ready to accept connections
server started
```

This confirms:
- WAL recovery succeeded
- No corruption
- PostgreSQL is healthy

---

## Step 5 — Verify PostgreSQL Is Running

```bash
ps aux | grep '[p]ostgres'
```

You should see multiple processes:
- checkpointer
- walwriter
- autovacuum
- stats collector

---

## Step 6 — Test Connections

### Socket connection
```bash
psql postgres
```

### TCP connection (recommended for Odoo)
```bash
psql -h localhost -p 5432 postgres
```

Both must work.

---

## Step 7 — Create Odoo Database User

Inside psql:

```sql
CREATE ROLE odoo WITH LOGIN SUPERUSER PASSWORD 'odoo';
ALTER ROLE odoo CREATEDB;
```

Exit:

```sql
\q
```

---

## Step 8 — Fix Odoo Configuration (IMPORTANT)

Edit your Odoo config file (e.g. `LiveDB_Old.conf`):

```ini
[options]
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
```

### Why this matters
- Avoids Unix socket issues
- Forces TCP (`127.0.0.1:5432`)
- Works reliably on macOS + Homebrew

---

## Step 9 — Start Odoo

```bash
./odoo-bin -c LiveDB_Old.conf -d LiveDB_Old
```

Odoo should now start without database errors.

---

## Optional — Re-enable Homebrew Services

Once PostgreSQL is healthy:

```bash
brew services cleanup
brew services start postgresql@17
```

⚠️ If this still fails, it is safe to ignore.
Manual `pg_ctl start` is perfectly fine for development.

---

## Root Cause Summary

| Cause | Effect |
|-----|------|
| macOS sleep / crash | PostgreSQL killed |
| External drive usage | higher crash probability |
| Homebrew upgrades | service mismatch |
| Unclean shutdown | stale `postmaster.pid` |

---

## Final Sanity Checklist

```bash
ps aux | grep postgres
psql -h localhost -U odoo postgres
./odoo-bin -c LiveDB_Old.conf -d LiveDB_Old
```

If all succeed → system is healthy ✅

---

**Status:** ✅ Resolved  
**Environment:** macOS + Homebrew + PostgreSQL 17 + Odoo 18
