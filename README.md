# NCKL Logistics Services Platform

Independent NCKL logistics web application based on the proven Django/DRF and Next.js logistics stack.

## Safety

This repository is for NCKL only. It must not reuse SAHA production databases, Redis instances, services, domains, media, logs, backups, SMTP credentials, or deployment paths. Requirement images under `docs/nckl_*.jpeg` are local input material and are ignored unless explicitly approved for commit.

## Stack

- Backend: Django 4.2, Django REST Framework, PostgreSQL, Redis, Celery, Gunicorn.
- Frontend: Next.js 14 App Router, React, TypeScript, Tailwind CSS.
- Runtime templates: NCKL-prefixed systemd, Nginx, Redis, and backup configuration under `deploy/`.

## Configuration

Copy `.env.example` to `.env` and provide NCKL-owned values before running any production process. Unknown business values such as final domain, pricing, legal text, payment terms, and SMTP credentials are intentionally not hardcoded.

## Documentation

Audit and implementation documentation lives in `docs/audit/` and `docs/implementation/`.
