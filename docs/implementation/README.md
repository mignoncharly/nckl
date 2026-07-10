# NCKL Implementation Notes

## Implemented phases

- Phase 1: repository safety baseline, ignore rules, safe `.env.example`, staged safety script, and audit baseline committed.
- Phase 2/3: SAHA runtime coupling replaced with NCKL defaults and centralized frontend/backend configuration.
- Phase 4/5: route options, accepted item categories, drop-off locations, shipment schedules, and request workflow fields added with migrations and API serializers/views.
- Phase 6/7: NCKL public branding, route/location/schedule display, WhatsApp actions, and customer request form fields implemented.
- Phase 8/9/10: admin-protected APIs, upload content validation, NCKL email/push/contact copy, token/locale keys, CSP origin configuration, and FR/DE catalogs updated.
- Phase 11: backend tests and frontend production build run locally without production services.

## Main architectural decisions

- NCKL remains a single-client application, not a multi-tenant/white-label product.
- Business records that staff must maintain are database-managed: services, route options, accepted item categories, drop-off locations, and shipment schedules.
- Infrastructure-sensitive and globally branded values remain environment/config driven.
- Pricing stays empty/admin-managed because no confirmed NCKL prices were supplied.
- The conflicting transit-time claims are represented as configurable `transit_time_display` values on route records.

## Configuration locations

- Backend defaults: `backend/config/settings/base.py` and `.env.example`.
- Frontend public defaults: `frontend/src/lib/nckl-config.ts` and `frontend/src/lib/constants.ts`.
- Deployment templates: `deploy/nginx/nckl-*.conf`, `deploy/systemd/nckl-*.service`, `deploy/redis-nckl.conf.example`.
- Runtime reference prefix: `REQUEST_REFERENCE_PREFIX`, default `NCKL`.

## Required environment variables

See `.env.example`. Production must provide NCKL-owned values for `SECRET_KEY`, database credentials/URL, Redis URL/password, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `FRONTEND_URL`, `NEXT_PUBLIC_API_URL`, SMTP settings, VAPID keys, final support email, and final domains.

## Database migrations created

- `backend/apps/services/migrations/0002_accepteditemcategory_alter_servicetype_options_and_more.py`
- `backend/apps/schedules/migrations/0002_dropofflocation_shipmentschedule_and_more.py`
- `backend/apps/logistics/migrations/0006_transportrequest_accepted_item_and_more.py`

## Admin setup requirements

Create an NCKL-only admin account after the dedicated NCKL database exists. Use the admin APIs/Django admin to review services, route options, accepted item categories, drop-off locations, shipment schedules, and prices before production.

## Tests run

- `scripts/check-repo-safety.sh`
- `backend/.venv/bin/python backend/manage.py check --settings=config.settings.test`
- `backend/.venv/bin/python backend/manage.py makemigrations services schedules logistics --settings=config.settings.test`
- `backend/.venv/bin/python backend/manage.py test backend/tests --settings=config.settings.test`
- `backend/.venv/bin/python backend/manage.py compilemessages --settings=config.settings.test`
- `cd frontend && npm run build`

`npm run lint` was attempted but Next.js prompted to create an ESLint config, so it was not usable non-interactively in this checkout.

## Known unresolved client inputs

Final NCKL domain, final API domain, legal/privacy text, production email sender, final support email, final pricing, payment workflow, customs terms, final transit-time wording, final primary Cameroon contact number, exact ambiguous address spelling, whether July 2026 schedules are one-time or recurring, and final language scope.

## Deployment prerequisites

Dedicated NCKL database and role, dedicated Redis instance/password, dedicated `.env`, final domains and SSL certificates, final SMTP/VAPID credentials, reviewed Nginx/systemd templates, static/media/log/backup directories, admin account, and approval to run migrations against the NCKL database.

## Rollback considerations

Before deployment, take a NCKL-only database and media backup. Roll back by reverting the deployed Git revision, rebuilding the frontend, restarting only NCKL services, and restoring the NCKL database backup if migrations were applied. No SAHA rollback path is involved.
