 Phase 0: Production-Safe Setup

  Goal: make changes without touching live services.

  - Create a clean branch from main or rebase current work onto main.
  - Do all testing in a staging/local clone, not /home/mignon/saha.
  - Confirm backup/rollback path before any backend deploy:
      - DB backup.
      - Current commit SHA.
      - systemd restart commands documented.

  - Add a short docs/release-checklist.md.

  Exit criteria: repeatable safe workflow exists before code changes.

  Phase 1: Repository Hygiene And Secrets

  Highest priority.

  - Remove from Git tracking:
      - deploy/.secrets.json
      - deploy/redis-data/dump.rdb
      - deploy/redis-data/redis-saha.pid

  - Add .gitignore rules for:
      - deploy/.secrets.json
      - deploy/redis-data/
      - local runtime/cache/backup artifacts.

  - Add deploy/.secrets.example.json.
  - Rotate any secrets that may have existed in tracked files.
  - Decide whether history cleanup is needed. If secrets were pushed to GitHub, rotation is mandatory even if history cleanup is
    done.

  Exit criteria: no secrets/runtime artifacts tracked; credentials rotated.

  Phase 2: Public Privacy Fix

  Goal: public tracking should not leak private/admin data.

  Backend:

  - Add PublicTransportRequestTrackingSerializer.
  - Include only:
      - reference_code
      - status
      - translated status label if useful
      - pickup_city
      - destination city name
      - service type name
      - created date
      - preferred pickup date if acceptable

  - Exclude:
      - customer phone/email
      - full pickup address
      - internal notes
      - prices
      - photos/media URLs

  - Keep full serializer for admin and authenticated customer detail.

  Frontend:

  - Update /suivi types/components to consume public tracking shape.
  - Add authenticated customer detail endpoint/page later if customers need private full details.

  Tests:

  - Assert anonymous tracking response does not include customer.email, phone, internal_notes, estimated_price, final_price, or
    photos.

  Exit criteria: guest tracking is minimal and tested.

  Phase 3: Admin API/UI Completion

  Goal: make admin controls actually persist what the UI shows.

  Pickup schedules:

  - Create an admin serializer that accepts:
      - region or region_name
      - cities
      - start_date
      - end_date
      - notes
      - active

  - Decide behavior for region creation:
      - Conservative option: accept region_name, create/update PickupRegion.

  - Update admin schedule endpoints to use admin serializer.
  - Remove window.location.reload() after CSV import; refresh state.

  Pricing:

  - Add active, valid_from, valid_until to admin serializer.
  - Keep public price list filtered to active/current rules.
  - Make the UI active checkbox real.
  - Optionally expose validity dates in admin UI.

  Loading dates:

  - Add active to admin serializer.
  - Add active toggle in UI or remove inactive concept from model/admin if not needed.

  Services:

  - Backend admin endpoints exist, but admin nav has no service catalog editor.
  - Add simple admin service editor for name, description, icon, active, sort_order.

  Tests:

  - Admin create/update schedule.
  - Admin active/inactive pricing.
  - Public endpoints exclude inactive records.
  - Admin service CRUD.

  Exit criteria: no admin field is fake/read-only by accident.

  Phase 4: Auth And Public Endpoint Hardening

  Goal: reduce abuse risk without changing the whole auth system.

  Backend:

  - Add throttles for:
      - password reset request
      - password reset confirm
      - email verification
      - resend verification
      - push subscription

  - Apply validate_password(new_password, user) during password reset confirm.
  - Normalize email lookup during password reset with email__iexact.
  - Consider invalidating auth token after password reset.
  - Keep generic password reset response to avoid account enumeration.

  Frontend:

  - Show validator errors from reset-confirm instead of generic error only.
  - Keep current localStorage token short-term, but document migration to HttpOnly cookies.

  Security headers:

  - Add frontend/Nginx headers:
      - CSP, ideally report-only first
      - Referrer-Policy
      - Permissions-Policy
      - frame-ancestors 'none'
      - HSTS at TLS layer

  Exit criteria: high-abuse endpoints throttled; reset password respects Django validators.

  Phase 5: Backend Reliability And Audit

  Reference codes:

  - Replace “latest + 1” race-prone generation with:
      - retry-on-IntegrityError, or
      - small yearly counter table, or
      - DB sequence-backed reference.

  - Keep existing format: STL-YYYY-000001.

  Customer matching:

  - Normalize phone numbers before matching.
  - For authenticated users, attach requests to their Customer profile first.
  - For anonymous users, avoid overwriting existing customer identity too aggressively.

  Audit:

  - Wire actor attribution for admin mutations.
  - Record:
      - actor
      - action
      - entity
      - entity id
      - before/after status or changed fields
      - metadata

  - Add admin audit log page later.

  Notifications:

  - Replace print() in web push with logger.
  - Mark expired/invalid push subscriptions inactive.
  - Upsert push subscriptions by endpoint.
  - Add unsubscribe/deactivate-device flow.

  Exit criteria: request IDs are race-safe; audit records identify actors; notification failures are operationally useful.

  Phase 6: Dependency And Platform Upgrades

  Do after functional fixes, not mixed into them.

  Backend:

  - Django 4.2 is now unsupported according to the official Django download page: extended support ended April 7, 2026. Plan
    upgrade to Django 5.2 LTS first, not straight to 6.x unless there is a separate compatibility budget. Django 5.2 LTS is listed
    as supported until April 2028.

  - Upgrade path:
      - bump Django to latest 5.2.x
      - upgrade DRF, django-filter, django-cors-headers, Celery, Redis client, gunicorn
      - run deprecation checks
      - run migrations check
      - run full backend tests

  - Keep Python version compatibility verified before bumping Django.

  Frontend:

  - First patch within current Next 14 line if security patches exist.
  - Then plan major Next upgrade separately.
  - Next 14 was released October 26, 2023, so treat it as aging stack, but do not combine a major Next migration with privacy/admin
    fixes.

  Exit criteria: supported Django LTS, dependency locks updated, tests/build green.

  Sources: Django supported versions page: https://www.djangoproject.com/download/ and Next 14 release page:
  https://nextjs.org/blog/next-14

  Phase 7: Documentation And Contracts

  Fill the empty docs.

  - docs/security.md
      - auth model
      - data exposure rules
      - media handling
      - secrets policy
      - production-safe commands
      - incident/rollback basics

  - docs/api-contract.md
      - public endpoints
      - admin endpoints
      - auth requirements
      - request/response shapes
      - status transitions

  - docs/mvp-roadmap.md
      - completed MVP
      - fixes required before growth
      - next features

  - Update docs/deployment.md
      - systemd production path first
      - Docker Compose clearly labeled local/dev only

  - Update README.md to warn production checkout is systemd-managed.

  Exit criteria: docs no longer contradict production reality.

  Phase 8: Testing And CI

  Add practical checks.

  Backend:

  - Run Django test suite in isolated env.
  - Add tests for every fix above.
  - Add a permission smoke test for all /api/admin/ endpoints.

  Frontend:

  - Add tsc --noEmit script.
  - Keep npm run lint.
  - Add minimal Playwright only for high-value flows:
      - request submit
      - tracking
      - admin login guard
      - admin schedule create/edit

  - Add i18n missing-key check.

  CI:

  - Backend tests.
  - Frontend lint/typecheck.
  - Secret scanning.
  - No tracked runtime artifacts.

  Exit criteria: regressions are caught before production.

  Phase 9: Feature Roadmap After Fixes

  Only after hardening/completion.

  Recommended order:

  1. Authenticated customer request detail page.
  2. Status-change history per request.
  3. Admin audit log UI.
  4. Payment status fields without online payment.
  5. Request message thread or internal/customer comments.
  6. CSV import preview before applying.
  7. Operational dashboard for failed notifications/emails.
  8. Data retention workflow for photos and PII.
  9. Filter-aware CSV exports.
  10. Admin service catalog editor if not already done in Phase 3.

  Deployment Plan Per Phase

  For backend changes:

  - Build/test in staging.
  - Review migrations before applying.
  - Backup DB.
  - Deploy code.
  - Run migrations only if required.
  - Restart:
      - saha-api for API changes.
      - saha-worker and saha-beat if task code changes.

  For frontend changes:

  - npm run build in safe deployment flow.
  - Restart saha-frontend.

  For secrets:

  - Rotate first.
  - Deploy new env/secrets.
  - Restart affected services.
  - Confirm logs.

  Best First Batch

  I would start with these three PRs:

  1. Repo hygiene and secret/runtime artifact cleanup.
  2. Public tracking serializer privacy fix.
  3. Admin schedule/pricing/loading active serializer fixes.

  Those deliver the most risk reduction with the least architectural churn.