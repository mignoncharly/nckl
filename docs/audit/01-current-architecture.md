# 01 - Current Architecture

## Inspection Basis

Status: verified fact.

This audit inspected the `/home/mignon/nckl` checkout only. Commands used included `rg --files`, `find`, `git status`, `git ls-files`, `git log`, targeted `sed`, targeted `rg -n`, and read-only file listing. No server, migration, deployment, commit, push, package install, email, notification, or external production request was run.

Image limitation: `docs/nckl_1.jpeg` through `docs/nckl_7.jpeg` exist as untracked files, but the sandbox blocked direct image/OCR processing. NCKL-specific content from those images is therefore not verified in this document.

## Top-Level Layout

Status: verified fact.

| Path | Purpose | Notes |
| --- | --- | --- |
| `backend/` | Django/DRF API, domain apps, migrations, tests, locale files | Contains ignored runtime artifacts: `.venv/`, `media/`, `staticfiles/`, `logs/`, `test_media/`. |
| `frontend/` | Next.js App Router frontend | Contains tracked `package.json`, `package-lock.json`, `tsconfig.tsbuildinfo`; ignored `.next/`, `node_modules/`, `.env.production`. |
| `deploy/` | Production-style Nginx, systemd, Redis, root setup templates | Still SAHA-specific and unsafe for NCKL as-is. |
| `nginx/` | Docker-oriented Nginx sample config | Not aligned with the requested no-Docker production target. |
| `scripts/` | Backup/restore/admin/VAPID helper scripts | Several scripts are Docker or SAHA/STL-specific. |
| `docs/` | Existing SAHA project documentation and supplied NCKL JPEGs | Existing docs mostly describe SAHA. |
| `.github/workflows/` | CI workflow directory | Present; workflow details were not deeply audited in this initial pass. |
| `backups/` | Ignored database backup artifacts | Contains SQL backups and copied secret/runtime backup files; must never be committed. |

## Stack

Status: verified fact.

Backend:

| Item | Finding | Evidence |
| --- | --- | --- |
| Framework | Django 5.2.15 + Django REST Framework 3.16.1 | `backend/requirements.txt` |
| Language | Python | Django project under `backend/` |
| ORM | Django ORM | `models.py` files in `backend/apps/*` |
| Database | PostgreSQL in normal/runtime settings; SQLite in test settings | `backend/config/settings/base.py:83`, `backend/config/settings/test.py` |
| Cache/queue | Redis URL used for Django cache and Celery broker | `backend/config/settings/base.py` |
| Background jobs | Celery 5.6.3, django-celery-results, django-celery-beat | `backend/requirements.txt`, `backend/config/celery.py` |
| Web server | Gunicorn for WSGI in systemd service templates | `deploy/systemd/saha-api.service` |
| i18n | Django gettext, `fr` and `de` locales | `backend/locale/*`, `LANGUAGES` in settings |

Frontend:

| Item | Finding | Evidence |
| --- | --- | --- |
| Framework | Next.js 14.2.5 App Router | `frontend/package.json`, `frontend/src/app/` |
| Language | TypeScript + React 18 | `frontend/package.json`, `.tsx` files |
| Styling | Tailwind CSS 3.4.1 | `frontend/tailwind.config.ts`, `frontend/src/styles/globals.css` |
| Forms | `react-hook-form` + `zod` | `frontend/package.json`, `frontend/src/lib/validators.ts` |
| UI helpers | `lucide-react`, `recharts`, `sonner`, `qrcode` | `frontend/package.json` |
| PWA | Service worker, manifest route, icons, offline page | `frontend/public/sw.js`, `frontend/src/app/manifest.webmanifest/route.ts` |

Package managers:

| Area | Package manager | Lock file |
| --- | --- | --- |
| Backend | `pip` requirements | `backend/requirements.txt`; no Python lock file found |
| Frontend | npm | `frontend/package-lock.json` |

## Backend Application Structure

Status: verified fact.

The Django URL root is `backend/config/urls.py`. API routes are mounted below `/api/`, while Django admin remains `/admin/`.

Domain apps under `backend/apps/`:

| App | Current responsibility |
| --- | --- |
| `accounts` | Email-based custom user, DRF token login/register, email verification, password reset |
| `customers` | Customer records and phone-based matching |
| `services` | Transport service types and admin CRUD |
| `pricing` | Public price list, estimate endpoint, admin price CRUD |
| `logistics` | Transport requests, references, statuses, comments, customer request views, admin request management, CSV export, retention |
| `schedules` | Pickup regions/schedules, loading dates, admin import/export |
| `destinations` | Destination city catalogue |
| `notifications` | Web push subscriptions, notification logs, in-app notifications, email tasks |
| `contact` | Public contact form and email dispatch |
| `audit` | Audit log model, middleware, signals/services, admin list |
| `admin_api` | Admin dashboard aggregation and route composition |
| `core` | Shared pagination, permissions, throttles, exceptions, middleware, i18n helpers |
| `uploads` | Upload storage/validation helpers |

## Frontend Application Structure

Status: verified fact.

The frontend uses Next.js App Router under `frontend/src/app/`. Public French slugs include `/services`, `/tarifs`, `/suivi`, `/demande`, `/calendrier`, `/compte`, `/contact`, `/faq`, and `/privacy`. Admin routes live under `/admin`.

Supporting directories:

| Path | Purpose |
| --- | --- |
| `frontend/src/components/layout` | Navbar, mobile drawer, footer, user menu, bottom CTA |
| `frontend/src/components/public` | Marketing/public workflow cards, hero, FAQ, schedule, price, status timeline |
| `frontend/src/components/admin` | Admin shell, sidebar, request table/detail, editors, charts, audit log, notification composer |
| `frontend/src/components/ui` | Loading, empty, error, section, form field, password input, status badge |
| `frontend/src/lib` | API client, auth token helpers, i18n, validators, constants, PWA, WhatsApp |
| `frontend/src/hooks` | Auth, install prompt, push notifications, unread count |
| `frontend/src/types` | API/request/pricing/schedule TypeScript types |

## Authentication and Authorization

Status: verified fact.

Backend:

| Topic | Finding | Evidence |
| --- | --- | --- |
| User model | Custom `accounts.User` extends `AbstractUser`, removes username, uses unique email | `backend/apps/accounts/models.py` |
| Roles | `role` choices: `admin`, `staff`, `customer` | `backend/apps/accounts/models.py` |
| Auth method | DRF token auth plus session auth | `REST_FRAMEWORK` in `backend/config/settings/base.py` |
| Login/register | `/api/auth/login/`, `/api/auth/register/` issue tokens | `backend/apps/accounts/views.py` |
| Admin permission | `IsStaffOrAdmin` checks authenticated role in `admin` or `staff` | `backend/apps/core/permissions.py` |
| Customer ownership | Customer request detail/history/comments filter by authenticated user's `customer_profile` | `backend/apps/logistics/views.py` |

Frontend:

| Topic | Finding | Evidence |
| --- | --- | --- |
| Token storage | Auth token stored in browser `localStorage` key `stl_admin_token` | `frontend/src/lib/auth.ts:5` |
| Auth provider | `AuthProvider` wraps the app and fetches `/auth/me/` when token exists | `frontend/src/hooks/useAuth.tsx` |
| Admin routing | Admin pages use frontend auth state and backend protected routes | `frontend/src/app/admin/*`, `frontend/src/components/admin/*` |

Security recommendation: token storage should be revisited before NCKL launch. `localStorage` works but increases impact of XSS. If keeping DRF token auth, harden CSP and frontend injection surfaces; if switching to cookies, design CSRF/session behavior explicitly.

## API Architecture

Status: verified fact.

The backend is a REST API. Public endpoints are mostly list/create/detail views. Admin endpoints are grouped under `/api/admin/` and use role checks.

Public API examples:

| Endpoint | Purpose |
| --- | --- |
| `GET /api/services/` | Active service types |
| `GET /api/prices/` | Active/current prices |
| `GET /api/prices/estimate/` | Price estimate |
| `GET /api/pickup-schedules/` | Active pickup schedules |
| `GET /api/loading-dates/` | Active loading dates |
| `GET /api/destination-cities/` | Active destinations |
| `POST /api/transport-requests/` | Create public transport request with optional photos |
| `GET /api/transport-requests/<reference>/` | Anonymous minimal tracking projection |
| `POST /api/contact/` | Contact form email |
| `POST /api/notifications/subscribe/` | Web-push subscription |

Admin API examples:

| Endpoint group | Purpose |
| --- | --- |
| `/api/admin/dashboard/` | Counts, charts, notification failure stats |
| `/api/admin/requests/` | Request list/detail/status/comments/bulk/export/retention |
| `/api/admin/services/` | Service catalogue CRUD |
| `/api/admin/prices/` | Price rule CRUD |
| `/api/admin/pickup-schedules/` | Schedule CRUD and CSV import/export |
| `/api/admin/loading-dates/` | Loading date CRUD |
| `/api/admin/broadcast/` | Push/in-app broadcast |
| `/api/admin/audit/` | Audit log list |

## Data Model

Status: verified fact.

Core models:

| Model | Key fields |
| --- | --- |
| `accounts.User` | `email`, `role`, `email_verified`, verification token fields |
| `customers.Customer` | optional `user`, name, phone, WhatsApp, email, preferred language |
| `services.ServiceType` | name, description, icon, active, sort order |
| `destinations.DestinationCity` | name, country defaulting to `Cameroun`, active |
| `pricing.PriceRule` | service, label, decimal price, currency, unit, active, validity window |
| `schedules.PickupRegion` | name, country defaulting to `Allemagne`, comma-separated cities |
| `schedules.PickupSchedule` | region, date range, cities override, notes, active |
| `schedules.LoadingDate` | unique date, title, description, active |
| `logistics.TransportRequest` | reference, customer, service, pickup/destination, status, price/payment fields, notes |
| `logistics.TransportRequestPhoto` | request-linked image under `request_photos/` |
| `logistics.RequestStatusEvent` | status history with actor/note |
| `logistics.RequestComment` | internal/customer comments |
| `notifications.PushSubscription` | endpoint, keys, optional customer/region/language |
| `notifications.NotificationLog` | broadcast/status notification summary |
| `notifications.CustomerNotification` | in-app customer notification history |
| `notifications.NotificationPreference` | customer language/regions/status/pickup preferences |
| `audit.AuditLog` | actor/action/entity/metadata timestamp |

Evidence-based inference: the database is a single-client operational schema, not tenant-aware. NCKL should use its own database and seed data rather than sharing or migrating SAHA production data.

## File and Document Handling

Status: verified fact.

Transport request photos are accepted through multipart form upload. Validation checks file extension and size, with allowed extensions `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp` and a 5 MB memory limit (`backend/apps/uploads/validators.py`, `backend/config/settings/base.py:181`).

Media storage defaults to `MEDIA_ROOT = BASE_DIR / 'media'` unless overridden (`backend/config/settings/base.py:141`). Production Nginx config currently aliases `/media/` to `/home/mignon/saha/backend/media/`, which is unsafe for NCKL as-is.

PDF generation: unknown/not found. Searches for common PDF libraries and PDF-related application code did not identify a PDF generation feature in the application source. CSV export/import exists for admin requests and pickup schedules.

## Email, Push, and Background Work

Status: verified fact.

| Mechanism | Finding |
| --- | --- |
| Email | Django email backend; production SMTP settings in `backend/config/settings/production.py`; default sender still `STL <info@gestionatech.de>`. |
| Async email | Celery tasks send verification and password reset emails. |
| Contact form | Calls `send_mail(..., fail_silently=True)` to `settings.DEFAULT_FROM_EMAIL`. |
| Web push | `pywebpush` via VAPID settings; browser subscription endpoints in `/api/notifications/`. |
| Scheduled jobs | Celery beat runs daily data retention task at 03:30 Europe/Paris. |
| In-app notifications | `CustomerNotification` and read/unread endpoints. |

## Internationalization

Status: verified fact.

Backend supports French and German via Django gettext. Frontend supports `fr` and `de` through `frontend/src/lib/i18n-config.ts`, `i18n.tsx`, and `i18n-server.ts`. French appears to be the source/default language.

Risk: the translation dictionary contains many SAHA/STL strings and Cameroon/Europe routes. NCKL content must be replaced in both French and German.

## Logging and Error Handling

Status: verified fact.

Backend logging writes console and rotating file handlers to `backend/logs/stl.log` by default (`backend/config/settings/base.py:194-213`). This log filename and local artifact are source-client coupled and potentially sensitive.

DRF uses a custom exception handler that appends `status_code` to error responses (`backend/apps/core/exceptions.py`). Frontend API errors are parsed in `frontend/src/lib/api.ts`.

## Tests

Status: verified fact.

Backend tests exist in `backend/tests/`: accounts, audit, comments, customer matching/detail, i18n, notifications, payment, pricing, schedules, services, status history, and transport requests.

Frontend test framework was not found. Frontend verification is currently lint/type/build-oriented.

No tests were run during this initial planning pass.

## Build and Deployment

Status: verified fact.

Frontend:

| Command | Purpose |
| --- | --- |
| `npm run build` | Production Next build |
| `npm run start` | Production Next start |
| `npm run lint` | Next lint |

Backend:

| Runtime | Purpose |
| --- | --- |
| `gunicorn config.wsgi:application` | Production API runtime in systemd template |
| Celery worker/beat | Async and scheduled work |

Deployment files are present but still SAHA-specific:

| Path | Issue |
| --- | --- |
| `deploy/systemd/saha-*.service` | Names, paths, ports, dependencies all SAHA-specific |
| `deploy/nginx/saha-stl.docufisc.de` | SAHA frontend domain and port `3030` |
| `deploy/nginx/api-saha.docufisc.de` | SAHA API domain, path aliases, port `8030` |
| `deploy/root_setup.sh` | Creates `saha_db`, `saha_user`, SAHA services, SAHA domains |
| `deploy/redis-saha.conf.example` and ignored `deploy/redis-saha.conf` | SAHA Redis naming, paths, port `6383` |
| `docker-compose*.yml` and `Makefile` | Docker-based local commands, contrary to target NCKL no-Docker production principle |

## Browser Request Flow

Status: evidence-based inference based on current configs.

Current SAHA-style flow:

1. Browser requests the frontend domain from Nginx.
2. Nginx proxies frontend traffic to Next.js on `127.0.0.1:3030`.
3. Next.js renders pages, fetching public data using `NEXT_PUBLIC_API_URL` or rewrite behavior.
4. Browser and server-side frontend requests call backend API endpoints under `/api/`.
5. API Nginx server block proxies to Gunicorn/Django on `127.0.0.1:8030`.
6. Django uses PostgreSQL through `DATABASE_URL`, Redis for cache/Celery broker, and filesystem media/static paths.
7. Celery worker handles email and push tasks; Celery beat schedules data retention.
8. SMTP and web-push services are external integrations.

NCKL target flow should preserve this shape but with dedicated domains, ports, service names, database, Redis instance, media/static roots, logs, secrets, and backup jobs.

