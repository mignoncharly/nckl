#!/usr/bin/env bash
# NCKL production deployment. Run manually with:
#   sudo bash /home/mignon/nckl/deploy/root_setup.sh
set -euo pipefail

APP_USER=mignon
APP_DIR=/home/mignon/nckl
BACKEND="$APP_DIR/backend"
FRONTEND="$APP_DIR/frontend"
VENV="$BACKEND/.venv/bin"
SECRETS="$APP_DIR/deploy/.secrets.json"
DOMAIN=nckl.docufisc.de
PGDB=nckl_db
PGUSER=nckl_user
REDIS_PORT=6384

if [[ $EUID -ne 0 ]]; then echo "Must run as root (use sudo)."; exit 1; fi
if [[ ! -f "$APP_DIR/.env" ]]; then echo "Missing $APP_DIR/.env"; exit 1; fi
if [[ ! -f "$SECRETS" ]]; then echo "Missing $SECRETS"; exit 1; fi

read_secret() { python3 -c "import json;print(json.load(open('$SECRETS'))['$1'])"; }
DB_PASSWORD=$(read_secret DB_PASSWORD)
ADMIN_PASSWORD=$(read_secret ADMIN_PASSWORD)
ADMIN_EMAIL=$(python3 -c "import json;d=json.load(open('$SECRETS'));print(d.get('ADMIN_EMAIL','admin@$DOMAIN'))")

echo "1/8 PostgreSQL: $PGDB / $PGUSER"
DB_PASSWORD="$DB_PASSWORD" python3 - <<'PY_DB'
import os, subprocess
pw = os.environ['DB_PASSWORD'].replace("'", "''")
sql = f"""
DO $$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'nckl_user') THEN
      CREATE ROLE nckl_user LOGIN PASSWORD '{pw}';
   ELSE
      ALTER ROLE nckl_user LOGIN PASSWORD '{pw}';
   END IF;
END
$$;
"""
subprocess.run(['sudo','-u','postgres','psql','-v','ON_ERROR_STOP=1'], input=sql, text=True, check=True)
exists = subprocess.run(['sudo','-u','postgres','psql','-tAc',"SELECT 1 FROM pg_database WHERE datname='nckl_db'"], capture_output=True, text=True, check=True).stdout.strip()
if exists != '1':
    subprocess.run(['sudo','-u','postgres','createdb','-O','nckl_user','nckl_db'], check=True)
subprocess.run(['sudo','-u','postgres','psql','-v','ON_ERROR_STOP=1','-c','ALTER DATABASE nckl_db OWNER TO nckl_user;'], check=True)
subprocess.run(['sudo','-u','postgres','psql','-v','ON_ERROR_STOP=1','-c','GRANT ALL PRIVILEGES ON DATABASE nckl_db TO nckl_user;'], check=True)
PY_DB

echo "2/8 Redis: nckl-redis on 127.0.0.1:$REDIS_PORT"
mkdir -p "$APP_DIR/deploy/redis-data/nckl"
chown -R "$APP_USER:$APP_USER" "$APP_DIR/deploy/redis-data"
install -m 644 "$APP_DIR/deploy/systemd/nckl-redis.service" /etc/systemd/system/nckl-redis.service
systemctl daemon-reload
systemctl enable --now nckl-redis.service
sleep 2
systemctl is-active --quiet nckl-redis.service

echo "3/8 Frontend build"
sudo -u "$APP_USER" bash -lc "cd '$FRONTEND' && npm run build"

echo "4/8 Django migrate, collectstatic, seed, admin"
RUN="sudo -u $APP_USER env DJANGO_SETTINGS_MODULE=config.settings.production"
( cd "$BACKEND" && $RUN "$VENV/python" manage.py migrate --noinput )
( cd "$BACKEND" && $RUN "$VENV/python" manage.py collectstatic --noinput )
( cd "$BACKEND" && $RUN "$VENV/python" manage.py seed_initial_data ) || echo "seed skipped/failed; continue"
( cd "$BACKEND" && $RUN ADMIN_EMAIL="$ADMIN_EMAIL" ADMIN_PW="$ADMIN_PASSWORD" "$VENV/python" manage.py shell <<'PY_ADMIN'
import os
from django.contrib.auth import get_user_model
U = get_user_model()
email = os.environ['ADMIN_EMAIL']
pw = os.environ['ADMIN_PW']
u, created = U.objects.get_or_create(email=email, defaults={'role':'admin','is_staff':True,'is_superuser':True,'is_active':True})
u.is_staff = True; u.is_superuser = True; u.is_active = True
if hasattr(u, 'role'): u.role = 'admin'
if hasattr(u, 'email_verified'): u.email_verified = True
u.set_password(pw)
u.save()
print('admin', 'created' if created else 'updated', email)
PY_ADMIN
)

echo "5/8 systemd app services"
for svc in nckl-api nckl-worker nckl-beat nckl-frontend; do
  install -m 644 "$APP_DIR/deploy/systemd/$svc.service" "/etc/systemd/system/$svc.service"
done
systemctl daemon-reload
systemctl enable --now nckl-api.service nckl-worker.service nckl-beat.service nckl-frontend.service
sleep 3
for svc in nckl-redis nckl-api nckl-worker nckl-beat nckl-frontend; do systemctl is-active --quiet "$svc.service"; done

echo "6/8 Nginx HTTP site"
install -m 644 "$APP_DIR/deploy/nginx/nckl-frontend.conf" "/etc/nginx/sites-available/$DOMAIN"
ln -sf "/etc/nginx/sites-available/$DOMAIN" "/etc/nginx/sites-enabled/$DOMAIN"
nginx -t
systemctl reload nginx

echo "7/8 Certbot HTTPS"
certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --email "admin@$DOMAIN" --redirect
nginx -t
systemctl reload nginx

echo "8/8 Smoke tests"
curl -fsS "http://127.0.0.1:8040/api/services/" >/dev/null
curl -fsSI "http://127.0.0.1:3040/" >/dev/null
curl -fsSI "https://$DOMAIN/" >/dev/null
curl -fsS "https://$DOMAIN/api/services/" >/dev/null

echo "NCKL deployment complete: https://$DOMAIN"
echo "Admin email: $ADMIN_EMAIL"
echo "Admin password is stored in $SECRETS and was not printed."
