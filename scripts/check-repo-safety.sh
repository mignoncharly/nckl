#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

fail=0

tracked_sensitive=$(git ls-files | grep -E '(^|/)(\.env|\.env\..+|.*\.sql|.*\.dump|.*\.backup|.*\.bak|.*\.pem|.*\.key|.*\.p12|.*\.pfx)$|(^|/)(backups|backend/media|backend/logs|backend/test_media|deploy/redis-data)(/|$)' | grep -v -E '(^|/)\.env\.example$' || true)
if [[ -n "$tracked_sensitive" ]]; then
  echo "Tracked sensitive/runtime files detected:" >&2
  echo "$tracked_sensitive" >&2
  fail=1
fi

staged_files=$(git diff --cached --name-only)
if [[ -n "$staged_files" ]]; then
  staged_sensitive=$(echo "$staged_files" | grep -E '(^|/)(\.env|\.env\..+|.*\.sql|.*\.dump|.*\.backup|.*\.bak|.*\.pem|.*\.key|.*\.p12|.*\.pfx|docs/nckl_.*\.jpeg)$|(^|/)(backups|backend/media|backend/logs|backend/test_media|deploy/redis-data)(/|$)' | grep -v -E '(^|/)\.env\.example$' || true)
  if [[ -n "$staged_sensitive" ]]; then
    echo "Staged private/runtime files detected:" >&2
    echo "$staged_sensitive" >&2
    fail=1
  fi

  diff_targets=$(echo "$staged_files" | grep -v -E '(^|/)(\.env\.example|scripts/check-repo-safety\.sh|backend/config/settings/base\.py|frontend/package-lock\.json|docs/audit/.*|docs/implementation/.*)$' || true)
  staged_secret_hits=""
  if [[ -n "$diff_targets" ]]; then
    # shellcheck disable=SC2086 # repository paths do not contain spaces.
    staged_secret_hits=$(git diff --cached -U0 -- $diff_targets | grep -E '^[+][^+].*(SECRET_KEY|PASSWORD|PRIVATE_KEY|DATABASE_URL|EMAIL_HOST_PASSWORD|VAPID_PRIVATE_KEY|BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY|saha-stl\.docufisc\.de|api-saha\.docufisc\.de|/home/mignon/saha|saha_db|saha_user|stl_db|stl_user)' || true)
  fi
  if [[ -n "$staged_secret_hits" ]]; then
    echo "Potential secret or SAHA production value in staged diff:" >&2
    echo "$staged_secret_hits" >&2
    fail=1
  fi
fi

if [[ "$fail" -ne 0 ]]; then
  exit 1
fi

echo "Repository safety check passed."
