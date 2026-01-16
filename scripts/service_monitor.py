#!/usr/bin/env python3

"""
Service Monitor Script
Chekcs status of critical services and sends alerts
"""

import subprocess
import smtplib
from email.mime.text import MIMEText
import json
from datetime import datetime

def check_service(service_name):
	"""Проверка статуса сист-ого сервиса"""
	try:
		result = subprocess.run(
			['systemctl', 'is-active', service_name],
			capture_output=True,
			text=True,
			timeout=5
		)
		return result.stdout.strip() == 'active'
	except subprocess.TimeoutExpired:
		return False
	except Exception as e:
		print(f"Error cheking {service_name}: {e}")
		return False

def check_port(port):
	"""Проверка доступности порта"""
	try:
		result = subprocess.run(
			['nc', '-z', 'localhost', str(port)],
			capture_output=True,
			timeout=5
		)
		return result.returncode == 0
	except:
		return False

def check_disk_usage(threshold=80):
	"""Проверка использования диска"""
	import psutil
	usage = psutil.disk_usage('/').percent
	return usage < threshold, f"Disk usage: {usage}%"

def main():
	"""Основная функц-я мониторинга"""
	services_to_check = [
		'ssh', 'nginx', 'postgresql', 'django'
	]

	ports_to_check = [
		22,   # SSH
		80,   # HTTP
		5432, # PostgreSQL
		8000, # Django
		9090, # Prometheus
		9100  # Node Exporter
	]

	results = {
		'timestamp': datetime.now().isoformat(),
		'services': {},
		'ports': {},
		'alerts': []
	}

	# Проверка сервисов
	for service in services_to_check:
		status = check_service(service)
		results['services'][service] = status
		if not status:
			results['alerts'].append(f"Service {service} is DOWN")

	# Прверка портов
	for port in ports_to_check:
		status = check_port(port)
		results['ports'][port] = status
		if not status:
			results['alerts'].append(f"Port {port} is not accessible")

	# Проверка диска
	disk_ok, disk_msg = check_disk_usage()
	results['disk'] = disk_msg
	if not disk_ok:
		results['alerts'].append(disk_msg)

	# Сохранение результатов
	with open('/tmp/monitoring_report.json', 'w') as f:
		json.dump(results, f, indent=2)

	# Вывод результатов
	print(f"Monitoring report generated at: {results['timestamp']}")
	print(f"Services: {sum(results['services'].values())}/{len(results['services'])} OK")
	print(f"Ports: {sum(results['ports'].values())}/{len(results['ports'])} OK")

	if results['alerts']:
		print("\nALERTS:")
		for alert in results['alerts']:
			print(f" ⚠️  {alert}")
		return False
	else:
		print("\n✅ All systems operational")
		return True

if __name__ == '__main__':
	success = main()
	exit(0 if success else 1)
