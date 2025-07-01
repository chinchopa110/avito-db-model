#!/bin/bash
set -e

export PGPASSWORD="$POSTGRES_PASSWORD"
BACKUP_DIR="/backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
FILENAME="backup_${TIMESTAMP}.dump"
FULL_PATH="${BACKUP_DIR}/${FILENAME}"

echo "[INFO] Starting binary backup: $FILENAME"

pg_dump -h "$PGHOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc -f "$FULL_PATH"

echo "[INFO] Backup saved to $FULL_PATH"

cd "$BACKUP_DIR"
TOTAL_BACKUPS=$(ls -1 backup_*.dump 2>/dev/null | wc -l)

if [ "$TOTAL_BACKUPS" -gt "$BACKUP_RETENTION_COUNT" ]; then
  echo "[INFO] Removing old backups..."
  ls -1t backup_*.dump | tail -n +$(($BACKUP_RETENTION_COUNT + 1)) | xargs rm -f
fi
