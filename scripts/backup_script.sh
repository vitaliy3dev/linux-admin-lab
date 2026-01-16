#!/bin/bash

# Backup script for System Administrator Lab
# Repforms daily backups of critical data

# Конфигурация
BACKUP_ROOT="/home/jindrew/linux-admin-lab/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$BACKUP_ROOT/$TIMESTAMP"

# Что бэкапим
ITEMS_TO_BACKUP=(
	"/etc/nginx"
	"/etc/postgresql"
	"/etc/systemd/system"
	"/home/jindrew/linux-admin-lab/django_app"
	"/home/jindrew/linux-admin-lab/scripts"
	"/home/jindrew/linux-admin-lab/configs"
)

# Функции
log_message() {
	echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

create_backup() {
	log_message "Starting backup process..."

	# Создаем директорию для бэкапа
	mkdir -p "$BACKUP_DIR"

	# Бэкап PostgreSQL БД
	log_message "Backing up PostgreSQL database..."
	cd /tmp
	sudo -u postgres pg_dump djangodb > "/tmp/djangodb_backup.sql"
	cp "/tmp/djangodb_backup.sql" "$BACKUP_DIR/"
	rm "/tmp/djangodb_backup.sql"
	cd "$BACKUP_ROOT" 

	# Бэкап файлов
	log_message "Backing up configuration files..."
	for item in "${ITEMS_TO_BACKUP[@]}"; do
		if [ -e "$item" ]; then
			log_message " -> $item"
			cp -r "$item" "$BACKUP_DIR/" 2>/dev/null || true
		fi
	done

	# Создаем архив
	log_message "Creating archive..."
	cd "$BACKUP_ROOT"
	tar -czf "${TIMESTAMP}.tar.gz" "$TIMESTAMP"

	# Удаляем временную директорию
	rm -rf "$BACKUP_DIR"

	# Проверяем целостность архива
	if tar -tzf "${TIMESTAMP}.tar.gz" > /dev/null 2>&1; then
		SIZE=$(du -h "${TIMESTAMP}.tar.gz" | cut -f1)
		log_message "✅ Backup successful: ${TIMESTAMP}.tar.gz ($SIZE)"
		return 0
	else
		log_message "❌ Backup failed: archive is corrupted"
		return 1
	fi
}

cleanup_old_backups() {
	log_message "Cleaning up old backups (keeping last 7 days)..."
	find "$BACKUP_ROOT" -name "*.tar.gz" -mtime +7 -delete
}

# Основной скрипт
main() {
	log_message "=== Backup script started ==="

	# Создаем бэкап
	if create_backup; then
		# Очищаем старые бэкапы
		cleanup_old_backups

		# Логируем успех
		log_message "Backup process completed successfully"
		echo "Backup completed: ${TIMESTAMP}.tar.gz"
	else
		log_message "Backup process failed"
		exit 1
	fi
}

# Запуск
main
