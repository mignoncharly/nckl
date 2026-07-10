# 08 - Phased Implementation Plan

## Phase A - Repository and Safety Baseline

Objective: make the NCKL checkout safe to work in before application changes.

Tasks:

- Verify `.gitignore` protects `.env`, `.env.*`, backups, media, logs, staticfiles, `.next`, `node_modules`, secret files, and Redis runtime files.
- Inventory ignored local artifacts and decide whether to remove them from the NCKL workspace after explicit approval.
- Replace `.env.example` with NCKL-safe placeholders only.
- Add audit docs and NCKL onboarding docs.
- Add secret scanning where practical.

Likely files: `.gitignore`, `.env.example`, docs under `docs/`, CI config.

Dependencies: owner approval for cleanup of local ignored artifacts.

Risks: accidental staging of secrets/backups/media in a public repo.

Verification commands:

- `git status --short --ignored`
- `git ls-files`
- `rg -n "saha|SAHA|stl|STL|docufisc|gestionatech|/home/mignon/saha" .`
- staged secret scan before commit

Acceptance criteria:

- No secret/runtime/data artifacts staged.
- NCKL docs clearly warn against SAHA collisions.
- `.env.example` contains no real secret and no SAHA identity.

Suggested commits: one documentation/safety baseline commit.

Rollback: docs/config-template-only changes can be reverted without runtime impact.

## Phase B - Decouple Source-Client Configuration

Objective: remove SAHA/STL coupling from config and runtime names.

Tasks:

- Centralize brand/contact values in frontend config and backend settings.
- Replace `STL` token/cache/log/reference names with NCKL or config-driven names.
- Remove SAHA API domain from CSP.
- Replace deployment templates with disabled/reviewed NCKL templates.
- Add guard checks that NCKL env cannot point to SAHA domains/databases.

Likely files: `backend/config/settings/*`, `backend/config/celery.py`, `frontend/next.config.js`, `frontend/src/lib/constants.ts`, `frontend/src/lib/auth.ts`, `frontend/public/sw.js`, deployment templates.

Dependencies: NCKL domain/API domain/ports may remain placeholders until infra phase.

Risks: breaking auth token persistence, PWA caches, or API calls if names are changed without migration path.

Verification commands:

- `rg -n "saha|SAHA|stl|STL|api-saha|saha-stl|gestionatech|docufisc|/home/mignon/saha"`
- Backend tests with `DJANGO_SETTINGS_MODULE=config.settings.test`
- Frontend type/lint/build in safe context

Acceptance criteria:

- No active config points to SAHA.
- Remaining legacy references are only documented historical references or tests intentionally updated.

Suggested commits: backend config, frontend config, deploy templates as separate commits.

Rollback: revert individual commit; no production NCKL deployment exists yet.

## Phase C - NCKL Requirements and Branding

Objective: replace public identity and content with verified NCKL information.

Tasks:

- Extract requirements from images or owner-supplied text.
- Add NCKL logo/favicon/PWA assets.
- Implement theme tokens and typography choices.
- Replace metadata, nav/footer, hero, services, FAQ, contact, privacy/legal pages.
- Update FR/DE translations or adjust language scope if owner changes it.

Likely files: `frontend/src/app/*`, `frontend/src/components/layout/*`, `frontend/src/components/public/*`, `frontend/src/lib/i18n-config.ts`, `frontend/tailwind.config.ts`, `frontend/public/*`.

Dependencies: confirmed NCKL brand, content, legal, contact, services, prices.

Risks: publishing unverified legal/pricing claims.

Verification commands:

- `rg -n "SAHA|STL|Cameroun|Cameroon|gestionatech|docufisc"`
- `cd frontend && npm run lint`
- `cd frontend && npm run build` in safe NCKL context

Acceptance criteria:

- All visible public/admin copy is NCKL-aligned and bilingual if FR/DE remain.
- No placeholders or fake content.

Suggested commits: assets/theme, public copy, legal/contact, i18n.

Rollback: revert content commit(s).

## Phase D - Business Workflows

Objective: align customer/admin logistics workflows with NCKL requirements.

Tasks:

- Confirm guest vs account flows.
- Adapt request fields, required documents/photos, validation, consent text.
- Adapt tracking/detail visibility.
- Adapt status lifecycle and admin workflow.
- Adapt notification copy and triggers.
- Confirm payment handling.

Likely files: `backend/apps/logistics/*`, `backend/apps/pricing/*`, `backend/apps/schedules/*`, `frontend/src/app/demande/page.tsx`, `frontend/src/app/suivi/page.tsx`, admin components.

Dependencies: confirmed NCKL workflow requirements.

Risks: schema/status migrations if status values change.

Verification commands:

- Backend request/status/customer tests.
- Frontend form validation checks.
- API contract review.

Acceptance criteria:

- Customer and admin journeys match confirmed NCKL process.
- Permissions remain intact.

Suggested commits: request form/API, status model/UI, admin workflow, notification workflow.

Rollback: revert workflow commits before deployment; use DB backups after deployment.

## Phase E - Backend and Database Hardening

Objective: strengthen persistence, validation, permissions, and auditability.

Tasks:

- Apply necessary schema migrations.
- Add indexes/constraints.
- Add upload MIME/content validation.
- Add tracking throttle.
- Add redaction rules for audit logs.
- Add env validation/fail-fast checks.
- Add tests for permissions, uploads, retention, status, and privacy.

Likely files: backend models/migrations/serializers/views/settings/tests.

Dependencies: schema decisions and NCKL requirements.

Risks: migrations must never run against SAHA.

Verification commands:

- `DJANGO_SETTINGS_MODULE=config.settings.test python manage.py test`
- `python manage.py check --deploy --settings=config.settings.production` with safe env later

Acceptance criteria:

- Tests pass.
- Upload and permission regressions covered.
- Migrations reviewed.

Suggested commits: migrations, validation, permissions, tests.

Rollback: DB backup restore plus code rollback after deployment.

## Phase F - Frontend Quality

Objective: polish responsive, accessible, and operational UI.

Tasks:

- Verify mobile nav, bottom CTA, account/admin layouts.
- Ensure loading/empty/error/success states.
- Review keyboard/focus behavior.
- Optimize images/assets.
- Remove hardcoded backend exposure.
- Verify NCKL visual consistency.

Likely files: frontend app/components/styles.

Dependencies: final content/assets.

Risks: responsive regressions.

Verification commands:

- `npm run lint`
- `npm run build`
- Manual browser checks or Playwright later in isolated NCKL server context

Acceptance criteria:

- No overlap/truncation on mobile/desktop.
- Core flows usable and accessible.

Suggested commits: UI polish and state handling.

Rollback: revert UI commit(s).

## Phase G - Infrastructure Preparation

Objective: prepare NCKL-only runtime without touching SAHA.

Tasks:

- Create NCKL database/role/password.
- Create NCKL `.env`.
- Create NCKL systemd units.
- Create NCKL Nginx server blocks after domain confirmation.
- Configure NCKL static/media/log/backup dirs.
- Configure NCKL SMTP/VAPID.
- Add health checks and backup/restore scripts.

Likely files: `deploy/systemd/nckl-*`, `deploy/nginx/<nckl-domain>`, scripts, deployment docs.

Dependencies: domain, ports, secrets, SMTP.

Risks: port/service collisions.

Verification commands:

- `systemctl cat nckl-api` later
- `nginx -t` later
- port checks before activation

Acceptance criteria:

- No NCKL unit references `/home/mignon/saha`, `saha-*`, SAHA domains, or SAHA DB.

Suggested commits: infra templates/docs only; server activation separate and approved.

Rollback: disable NCKL units and remove NCKL Nginx symlinks only, not SAHA.

## Phase H - Testing and Acceptance

Objective: prove NCKL app behavior and isolation.

Tasks:

- Run backend unit/integration tests.
- Run frontend lint/build/type checks.
- Add permission/API/form/upload/security regression tests.
- Test backup and restore into a disposable DB.
- Complete owner acceptance checklist.

Dependencies: complete implementation and safe test environment.

Risks: tests accidentally configured with production env.

Verification commands:

- `DJANGO_SETTINGS_MODULE=config.settings.test python manage.py test`
- `cd frontend && npm run lint`
- `cd frontend && npm run build`
- Secret/source-client search

Acceptance criteria:

- All tests/checks pass.
- Owner approves content and workflows.
- No SAHA references in active runtime/config.

Suggested commits: final test fixes and acceptance docs.

Rollback: code revert before deployment.

## Phase I - Controlled Deployment

Objective: deploy NCKL without affecting SAHA.

Tasks:

- Predeployment backup of NCKL DB if it exists.
- Pull/build NCKL source.
- Install Python/Node dependencies in NCKL paths.
- Run NCKL migrations only.
- Collect static.
- Start/enable NCKL units.
- Activate NCKL Nginx config.
- Issue NCKL SSL certificate.
- Run smoke tests against NCKL domains.
- Monitor logs.
- Document rollback.

Dependencies: explicit approval, domain DNS, secrets, infra templates reviewed.

Risks: service collision if names/ports are wrong.

Verification commands:

- NCKL-only `systemctl status nckl-*`
- NCKL-only `journalctl -u nckl-*`
- NCKL URL smoke tests
- `rg` search for source-client values

Acceptance criteria:

- NCKL live on NCKL domain.
- SAHA services/domains remain untouched.
- Rollback tested/documented.

Suggested commits: deployment docs/templates before activation; no commit required for server secret files.

Rollback: stop NCKL services, restore NCKL DB backup, revert NCKL Nginx symlink, leave SAHA untouched.


## Image-Driven Refinements Added After Image Review

Status: recommendation based on Images 1-7.

### Phase C Additions - NCKL Requirements and Branding

Additional tasks:

- Replace SAHA visual identity with NCKL's dark navy, silver/white, red, and yellow/gold visual system.
- Replace logo/icon assets with the NCKL wordmark and swoosh once source assets are available.
- Add English and French content from the flyers; decide whether German remains required.
- Add TikTok handle `@nckllogisticsservices` to social/contact configuration if approved.
- Replace public route copy with Germany/Cameroon/Europe messaging only after transit-time conflicts are resolved.

Additional dependencies:

- Confirm final language scope: English/French, French/German, or English/French/German.
- Confirm exact primary phone numbers and final Berlin/Douala address spellings.

### Phase D Additions - Business Workflows

Additional tasks:

- Add route-direction support: Germany/Europe -> Cameroon, Cameroon -> Germany/Europe, and shopping-assistance workflows.
- Add accepted-item categories: dry foodstuff, frozen food, clothes, jewelries/bijoux, bags, shoes, cosmetics, hair extensions, dry herbs, documents, phones without battery, small household equipment.
- Add route/item conditions: phones without battery, phones Germany->Cameroon only if confirmed, small household equipment maximum 31 kg.
- Add shopping assistance from Europe workflow: product details/link, budget, quantity, purchase approval, payment status, doorstep delivery address in Cameroon.
- Add or configure drop-off locations for Bamenda, Douala/Bonaberi, Berlin, and Leipzig.
- Extend schedule data to represent drop-off deadline, departure date, arrival date, route direction, origin/drop-off location, and destination.

Additional risks:

- Transit-time claims conflict across images.
- No pricing is visible; pricing must remain owner-confirmed/admin-managed.
- Dates shown are campaign-specific July 2026 dates and should not become stale hardcoded homepage content.

### Phase E Additions - Backend and Database Hardening

Additional tasks:

- Decide whether drop-off locations need a new model or can be represented through existing schedules initially.
- Decide whether accepted items and route-specific item conditions need models, enum/config, or admin-managed content.
- Add validation tests for item/route constraints if they become enforced rules.
- Add tests for shopping-assistance request fields if implemented.

### Phase F Additions - Frontend Quality

Additional tasks:

- Build a service/route selector that does not overload the old one-way SAHA flow.
- Surface item-condition warnings clearly before submission.
- Provide readable location cards for multiple contacts and opening hours.
- Avoid flyer-style visual clutter while preserving NCKL brand colors and cues.

### Phase H Acceptance Additions

Additional acceptance criteria:

- Image-derived services and conditions are represented without inventing prices or legal claims.
- Drop-off location details match confirmed owner-approved text.
- Conflicting contacts/transit times have explicit owner decisions before launch.
