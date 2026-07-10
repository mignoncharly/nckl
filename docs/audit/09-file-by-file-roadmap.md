# 09 - File-by-File Roadmap

This roadmap lists files/directories that were inspected directly or whose role is clear from the repository structure. It does not claim every file needs modification.

| Path | Current purpose | Generic/client-specific | Planned modification | Reason | Security implications | Tests | Phase |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `README.md` | SAHA project overview | Client-specific | Replace with NCKL overview | Public repo docs must match NCKL | Avoid SAHA operational leakage | Docs review | A |
| `AGENTS.md` | SAHA onboarding/safety | Client-specific | Replace/update for NCKL while preserving SAHA isolation warning | Current content describes source project | Prevent wrong operational commands | Docs review | A |
| `.gitignore` | Ignore secrets/artifacts | Mostly generic with SAHA Redis name | Add/rename NCKL secret/runtime patterns | Avoid public leak | Critical | `git status --ignored` | A |
| `.env.example` | Env template | Client-specific | Replace `stl_*`, sender, phone with NCKL placeholders | Current values are SAHA/STL | Critical if copied to prod | Secret scan | A/B |
| `backend/requirements.txt` | Python deps | Generic | Reuse initially | Proven stack | Dependency audit needed | Backend tests | A/E |
| `backend/config/settings/base.py` | Core Django settings | Mixed | Replace STL defaults, add fail-fast production checks, configure logging names | Defaults reference STL | Secrets/DB/CORS risk | Django checks/tests | B/E |
| `backend/config/settings/production.py` | Production settings | Mixed | Require NCKL env, sender, CORS/hosts | Sender fallback is STL | Misrouting/leakage risk | Deploy check | B/G |
| `backend/config/settings/test.py` | Safe test settings | Generic | Reuse; maybe add NCKL media temp path | Uses in-memory DB/cache | Low | Backend tests | E |
| `backend/config/urls.py` | API root routing | Generic | Reuse | Clean route composition | Low | API tests | D |
| `backend/config/celery.py` | Celery app | Mostly generic | Rename app label from `stl` to `nckl` | Naming clarity | Low | Celery task tests | B |
| `backend/apps/accounts/*` | Auth/users/password reset | Generic with branded email dependencies | Reuse; review token auth and email copy | Mature auth flow | Token/security risk | Account tests | D/E |
| `backend/apps/customers/*` | Customer model/matching | Generic | Reuse; consider normalized phone index later | Single-client customer model works | PII handling | Customer tests | D/E |
| `backend/apps/services/*` | Service catalogue | Generic model, client seed data | Replace seed data and content | NCKL services unknown | Low | Service tests | C/D |
| `backend/apps/pricing/*` | Pricing rules | Generic model, client seed data | Replace prices; confirm currency/rules | NCKL prices unknown | Monetary accuracy | Pricing tests | C/D |
| `backend/apps/destinations/*` | Destination cities | Client default country | Replace default/seed if needed | `Cameroun` default | Content correctness | Destination/API tests | C/D/E |
| `backend/apps/schedules/*` | Pickup/loading dates | Client seed/default country | Replace seeds and perhaps defaults | SAHA regions/dates | Operational accuracy | Schedule tests | C/D |
| `backend/apps/logistics/models.py` | Transport requests/statuses | Mixed | Reuse with possible status rename | `arrived_cameroon` coupling | Migration risk | Request/status tests | D/E |
| `backend/apps/logistics/reference.py` | Reference generation | Mixed | Replace/configure prefix | `STL-` prefix | Enumeration/privacy | Collision tests | B/E |
| `backend/apps/logistics/views.py` | Public/customer/admin request API | Mostly generic | Reuse; add tracking throttle if needed | Good privacy scoping | PII exposure if changed | API permission tests | D/E |
| `backend/apps/logistics/retention.py` | Photo purge/anonymization | Generic | Reuse with NCKL retention settings | GDPR-relevant | Data deletion risk | Retention tests | E |
| `backend/apps/notifications/*` | Push/in-app/email notifications | Mixed | Replace brand/contact, generate NCKL VAPID, review failure logging | SAHA email templates | Secret/contact risk | Notification tests | B/C/D |
| `backend/apps/contact/*` | Contact form email | Mixed | Use NCKL recipient/sender/reply-to | Current subject is STL | Email spoof/delivery | Contact tests | C/E |
| `backend/apps/audit/*` | Audit logs | Generic | Reuse; add redaction/retention if needed | May log PII | Medium | Audit tests | E |
| `backend/apps/uploads/*` | Upload validation/storage | Generic | Add MIME/content validation | Extension-only check | File upload security | Upload tests | E |
| `backend/tests/*` | Backend tests | Mixed | Update expected prefixes/status labels/content | Tests encode STL/Cameroon | Regression coverage | Test suite | B-E |
| `frontend/package.json` | Frontend deps/scripts | Mixed | Rename package from `stl-frontend`; reuse deps | Naming contamination | Low | npm checks | B |
| `frontend/package-lock.json` | npm lock | Generic after name update | Update via npm only in implementation phase | Lock consistency | Dependency audit | npm checks | B |
| `frontend/next.config.js` | Headers/CSP/rewrites/images | Mixed | Replace SAHA CSP and configure NCKL image/API origins | API origin leak | High | Header/build checks | B/G |
| `frontend/tailwind.config.ts` | Theme tokens | Client-specific colors | Replace with NCKL brand after extraction | SAHA palette | Accessibility contrast | Visual checks | C/F |
| `frontend/src/styles/globals.css` | Shared styles | Mostly generic | Reuse with theme token changes | UI consistency | Low | Visual checks | C/F |
| `frontend/src/lib/i18n-config.ts` | FR/DE dictionary | Highly client-specific | Rewrite visible copy | SAHA/STL content | Legal/pricing risk | Search and UI review | C |
| `frontend/src/lib/constants.ts` | Contact and city constants | Client-specific | Replace/centralize | Phone/cities are SAHA | Contact misrouting | UI tests | B/C |
| `frontend/src/lib/auth.ts` | Token storage | Mixed | Rename token key; review storage model | `stl_admin_token`, localStorage risk | High | Auth tests | B/E |
| `frontend/src/lib/api.ts` | API client | Generic | Reuse; verify base URL | Local fallback okay for dev | Low | API tests | B |
| `frontend/src/lib/validators.ts` | Form schemas | Mixed | Adapt required fields/consent to NCKL | Workflow-dependent | Data quality | Form tests | D |
| `frontend/src/app/layout.tsx` | Root layout/metadata | Client-specific metadata | Replace title/description/theme color | SAHA SEO | Public misinformation | Metadata check | C |
| `frontend/src/app/page.tsx` | Homepage | Client-specific copy/layout data | Replace content while reusing sections | SAHA route/services | Public misinformation | Visual checks | C/F |
| `frontend/src/app/demande/page.tsx` | Request form | Mixed | Adapt fields/validation/copy | NCKL workflow unknown | PII/consent | Form/API tests | D |
| `frontend/src/app/suivi/page.tsx` | Tracking | Mixed | Update reference examples/statuses | STL reference | Privacy/UX | Tracking tests | D |
| `frontend/src/app/contact/page.tsx` | Contact page/form | Client-specific | Replace contact channels | SAHA email/phone | Misrouting | Contact tests | C |
| `frontend/src/app/privacy/page.tsx` | Privacy policy | Client-specific/legal | Replace with NCKL legal text | SAHA email/claims | Legal risk | Legal review | C |
| `frontend/src/app/admin/*` | Admin pages | Mostly generic with labels | Reuse; adapt statuses/content | Some STL labels | Permission relies on API | Admin tests | D/F |
| `frontend/src/components/layout/*` | Nav/footer/user chrome | Mixed | Replace brand/contact, keep structure | SAHA/STL names | Public misbrand | Responsive checks | C/F |
| `frontend/src/components/public/*` | Public cards/hero/FAQ/status | Mixed | Replace copy/assets/status labels | SAHA services/route | Public misinformation | Visual checks | C/D/F |
| `frontend/src/components/admin/*` | Admin UI | Mostly generic | Adapt labels/status/payment/workflow | STL labels in admin sidebar/login | Medium | Admin tests | D/F |
| `frontend/public/sw.js` | Service worker | Mixed | Rename cache namespace | `stl-v2` | Low | PWA test | B |
| `frontend/public/offline.html` | Offline page | Client-specific | Replace SAHA/STL copy | Public misbrand | Low | Offline check | C |
| `frontend/public/icons/*`, `frontend/src/app/icon.svg` | Icons/logos | Client-specific | Replace with NCKL assets | STL logo | Brand correctness | Asset check | C |
| `deploy/systemd/*` | SAHA systemd unit templates | Client-specific | Do not run; create `nckl-*` later | Collision with SAHA | Critical | Static review | G |
| `deploy/nginx/*` | SAHA Nginx templates | Client-specific | Do not run; create NCKL config later | Collision with SAHA | Critical | `nginx -t` later | G |
| `deploy/root_setup.sh` | SAHA provisioning | Client-specific | Do not run; rewrite/split later | Critical collision | Critical | Manual review | G |
| `scripts/backup_db.sh`, `scripts/restore_db.sh` | Docker/STL DB backup | Client-specific | Replace with no-Docker NCKL scripts | Data loss/leak | High | Restore test | G/H |
| `scripts/create_admin.py` | Hardcoded admin creation | Insecure/client-specific | Replace with env-driven bootstrap | Weak password/source email | High | Bootstrap test | G |
| `docker-compose*.yml`, `Makefile` | Docker local/dev helpers | Mixed/client-specific | Mark local-only or remove/rename | No-Docker principle | Medium | Docs review | A/B |
| `docs/nckl_*.jpeg` | Supplied NCKL images | NCKL material | Extract requirements when viewable | Currently unreadable in sandbox | Unknown | Manual/OCR validation | C |


## Image-Driven Roadmap Additions

| Path | Current purpose | New image-driven requirement | Planned modification | Reason | Phase |
| --- | --- | --- | --- | --- | --- |
| `frontend/src/lib/i18n-config.ts` | FR/DE text dictionary | Flyers contain English and French public copy | Decide language model; add English if required; replace SAHA text with NCKL copy | Current app does not support English despite English NCKL materials | C |
| `frontend/src/app/page.tsx` | Homepage | NCKL should present Germany/Cameroon/Europe routes, shopping assistance, and WhatsApp-first CTA | Replace SAHA sections with NCKL route/service summary | Image 1, 6, 7 content | C/F |
| `frontend/src/app/services/page.tsx` | Public services | NCKL services include bidirectional shipping and shopping assistance | Replace service intro and cards; possibly include accepted item conditions | Images 1, 2, 4, 6, 7 | C/D |
| `frontend/src/app/calendrier/page.tsx` | Schedule display | NCKL schedule needs drop-off deadlines, departure, arrival, route/location | Extend display after backend model/content decision | Images 2 and 4 | D/F |
| `frontend/src/app/contact/page.tsx` | Contact page | Multiple NCKL drop-off locations and contacts | Add location cards or consume admin-managed locations | Images 3, 5, 7 | C/D |
| `frontend/src/app/demande/page.tsx` | Request form | Route direction, item categories, conditional rules, shopping-assistance fields | Add route/service-specific form sections | Images 1, 6, 7 | D |
| `backend/apps/logistics/models.py` | Transport request | Needs route direction and possibly purchase-assistance fields | Add fields only after workflow decision | Images 1, 6, 7 | D/E |
| `backend/apps/services/seed_data.py` | SAHA service seed | NCKL service catalogue differs | Replace with NCKL services after owner confirmation | Image-derived service list | C/D |
| `backend/apps/schedules/models.py` | Pickup/loading dates | Needs drop-off deadline, departure, arrival, route/location | Extend or add schedule model | Images 2, 4 | D/E |
| `backend/apps/destinations/models.py` | Destination cities | NCKL has broad Europe/Cameroon routes, not just Cameroon cities | Generalize destination/route data | Images 1, 2, 4, 7 | D/E |
| `backend/apps/contact/*` or new `locations` app | Contact form only | Drop-off locations should be structured/admin-managed | Add model/API/admin UI if approved | Images 3, 5, 7 | D/E |
| `frontend/src/components/public/*` | Public cards/hero/status UI | NCKL route and item-condition cards | Reuse components but replace copy/content | Image-driven public content | C/F |
| `backend/apps/pricing/*` | Price rules | No prices visible in images | Keep admin-managed; do not seed fake prices | Avoid invented business data | C/D |

## Implementation update - 2026-07-10

Implemented NCKL runtime decoupling, centralized configuration, configurable routes/items/locations/schedules, customer request workflow fields, admin-protected APIs, upload validation, NCKL branding/content updates, deployment templates, and local regression checks. See `docs/implementation/README.md` for current implementation status.
