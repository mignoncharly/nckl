# 11 - Risk Register

| ID | Risk | Severity | Likelihood | Evidence | Mitigation | Owner decision needed |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | SAHA secrets copied into public NCKL repo | Critical | Medium | Ignored `.env`, `.secrets.json`, Redis config exist | Never stage; secret scanning; rotate NCKL secrets | Whether to purge local ignored artifacts |
| R2 | SAHA customer data or uploads copied into NCKL | Critical | Medium | Ignored backups and media files exist | Start NCKL DB/media empty; never stage backups/media | Confirm artifact origin/removal |
| R3 | NCKL deployment collides with SAHA services | Critical | Medium | Current systemd/Nginx/root setup use SAHA names/ports/paths | Rewrite NCKL infra with `nckl-*`, new ports | Final ports/domains |
| R4 | NCKL frontend/API points to SAHA API/domain | High | High | CSP and docs reference SAHA domains | Search and replace active config; env guard | Final API domain |
| R5 | Public site shows SAHA/STL branding | High | High | Many frontend/i18n/email references | Centralized branding replacement | NCKL brand assets/content |
| R6 | Wrong services/prices published | High | High | SAHA seed data and copy are present | Use only verified NCKL requirements | Confirm prices/services |
| R7 | Legal/privacy content is incorrect | High | Medium | Current privacy references SAHA email/claims | Owner/legal review before launch | Legal text |
| R8 | Auth token theft via XSS/localStorage | High | Medium | Token stored in `localStorage` | Harden CSP; consider cookie auth; audit UI | Auth strategy |
| R9 | File upload accepts disguised malicious images | Medium | Medium | Extension/size validation only | Add MIME/Pillow verification | Allowed file types |
| R10 | Reference codes are enumerable and client-specific | Medium | Medium | `STL-YYYY-NNNNNN` | NCKL prefix/randomization/throttle | Tracking policy |
| R11 | Tracking endpoint brute force | Medium | Low/Medium | Anonymous GET by reference code | Add throttle; keep minimal serializer | Tracking policy |
| R12 | Email failures are hidden | Medium | Medium | Contact form uses `fail_silently=True` | Log/store contact messages or failures | Ops expectations |
| R13 | Audit logs store too much PII | Medium | Unknown | Generic JSON audit metadata | Redact and define retention | Retention/legal |
| R14 | Build artifact leaks source path | Low | High | `frontend/tsconfig.tsbuildinfo` tracked with SAHA paths | Stop tracking | None |
| R15 | Docker files confuse operators | Medium | Medium | Docker compose and Makefile present | Mark local-only/remove from NCKL prod docs | Keep local Docker? |
| R16 | Image requirements cannot be extracted in current tool environment | Medium | High | Viewer/OCR blocked | Provide text or approved extraction path | Yes |

