# 06 - Isolation and Deployment Architecture

## Target Isolation Strategy

Status: recommendation.

NCKL must run as a separate single-client application using the existing proven architecture, not as a skin over SAHA. The architecture should keep Django/DRF, Next.js, PostgreSQL, Redis, Celery, Nginx, and systemd, but every runtime resource must be NCKL-owned.

## Required Dedicated Resources

| Resource | NCKL convention | Collision prevention |
| --- | --- | --- |
| Project directory | `/home/mignon/nckl` | Never use `/home/mignon/saha` paths. |
| Git repository | `github.com/mignoncharly/nckl` | Verify remote before push. |
| Backend venv | `/home/mignon/nckl/backend/.venv` | Separate Python packages and executables. |
| Frontend build | `/home/mignon/nckl/frontend/.next` | Build from NCKL source only. |
| API service | `nckl-api.service` | Separate systemd unit from `saha-api`. |
| Frontend service | `nckl-frontend.service` | Separate unit from `saha-frontend`. |
| Worker/beat | `nckl-worker.service`, `nckl-beat.service` | Separate Celery processes and queues/broker DB. |
| Redis | `nckl-redis.service` or shared Redis with separate DB/password only if explicitly approved | Prefer dedicated port/config/path. |
| API bind | TBD, not `127.0.0.1:8030` unless confirmed unused and not colliding | Pick after checking active ports. |
| Frontend bind | TBD, not `127.0.0.1:3030` unless confirmed unused and not colliding | Pick after checking active ports. |
| Database | `nckl_db` | Separate DB from `saha_db`/`stl_db`. |
| DB role | `nckl_user` | Separate role/password from SAHA. |
| Env files | `/home/mignon/nckl/.env`, possibly service env files | Never reuse SAHA `.env`. |
| Static files | `/home/mignon/nckl/backend/staticfiles` or dedicated `/var/www/nckl/static` | Nginx alias only to NCKL path. |
| Media/uploads | `/home/mignon/nckl/backend/media` or dedicated `/var/www/nckl/media` | Empty start; no copied SAHA media. |
| Logs | dedicated NCKL log path, e.g. `/home/mignon/nckl/backend/logs/nckl.log` or `/var/log/nckl/` | No `/var/log/nginx/saha-*` logs. |
| Backups | dedicated NCKL backup dir, e.g. `/home/mignon/nckl/backups` with restricted permissions | No SAHA backup reuse. |
| Nginx server blocks | `nckl-frontend` and `nckl-api` filenames after domain confirmed | No SAHA domains or aliases. |
| SSL cert | NCKL domain certificate | Do not renew/alter SAHA certs. |
| SMTP sender | NCKL verified sender | No `info@gestionatech.de` or SAHA identity. |
| VAPID keys | NCKL generated keys | No copied private keys. |
| Admin account | NCKL owner-approved admin email/password | No copied admin account. |

## Current Deployment Files Are Unsafe As-Is

Status: verified fact.

| File | Unsafe SAHA coupling |
| --- | --- |
| `deploy/systemd/saha-api.service` | Unit name, description, path `/home/mignon/saha`, bind `127.0.0.1:8030` |
| `deploy/systemd/saha-frontend.service` | Path `/home/mignon/saha/frontend`, port `3030` |
| `deploy/systemd/saha-worker.service` | Depends on `saha-redis`, path `/home/mignon/saha` |
| `deploy/systemd/saha-beat.service` | Depends on `saha-redis`, path `/home/mignon/saha` |
| `deploy/systemd/saha-redis.service` | Uses `/home/mignon/saha/deploy/redis-saha.conf` |
| `deploy/nginx/saha-stl.docufisc.de` | SAHA frontend domain and logs |
| `deploy/nginx/api-saha.docufisc.de` | SAHA API domain, media/static aliases, port `8030` |
| `deploy/root_setup.sh` | Creates/starts SAHA DB, Redis, services, Nginx, admin |

Do not run these files for NCKL.

## Proposed Request Flow

Status: recommendation.

1. Browser requests confirmed NCKL frontend domain.
2. Nginx NCKL frontend server block proxies to `nckl-frontend` on a dedicated localhost port.
3. Next.js renders public/admin routes and calls the NCKL API base URL.
4. Browser/API calls go to confirmed NCKL API domain.
5. Nginx NCKL API server block proxies to `nckl-api` Gunicorn on a dedicated localhost port.
6. Django connects only to `nckl_db` with `nckl_user`.
7. Django uses NCKL Redis broker/cache only.
8. Uploads/static files are served from NCKL storage paths only.
9. Celery worker/beat use NCKL settings, NCKL queue/broker, and NCKL SMTP/VAPID keys.
10. Backups dump only `nckl_db` into NCKL backup paths.

## Configuration Values Not To Choose Yet

Unknown.

Do not decide final values without owner confirmation:

| Value | Reason |
| --- | --- |
| Public frontend domain | Not supplied |
| Public API domain | Not supplied |
| Final ports | Must check live services and avoid SAHA |
| DB password | Must be generated securely and not committed |
| Django `SECRET_KEY` | Must be generated securely and not committed |
| Redis password | Must be generated securely and not committed |
| SMTP credentials | Must be NCKL-owned |
| VAPID keys | Must be generated for NCKL |
| Admin email/password | Owner decision |

## Collision Prevention Checklist

Recommendation.

- Search for `saha`, `SAHA`, `stl`, `STL`, `docufisc`, `gestionatech`, `/home/mignon/saha`, `saha_db`, `saha_user`, `stl_db`, `stl_user`, `8030`, `3030`, and `6383` before deployment.
- Verify `git remote -v` points to `mignoncharly/nckl`.
- Verify `DATABASE_URL` points to `nckl_db`.
- Verify all systemd unit names begin with `nckl-`.
- Verify all Nginx aliases begin with NCKL paths.
- Verify no NCKL service references `saha-redis`.
- Verify NCKL media/static/log paths are empty or NCKL-owned before launch.
- Verify NCKL frontend `NEXT_PUBLIC_API_URL` is not a SAHA URL.

