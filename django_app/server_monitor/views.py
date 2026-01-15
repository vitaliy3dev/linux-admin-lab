from django.shortcuts import render
from django.http import JsonResponse
import psutil
import platform
from  datetime import datetime
import os

def server_status(request):
	"""Возвращает статус сервера в JSON формате"""
	data = {
	    'timestamp': datetime.now().isoformat(),
	    'hostname': platform.node(),
	    'os': f"{platform.system()} {platform.release()}",
	    'cpu_percent': psutil.cpu_percent(interval=1),
	    'memory_percent': psutil.virtual_memory().percent,
	    'disk_percent': psutil.disk_usage('/').percent,
	    'uptime': os.popen('uptime -p').read().strip(),
	    'status': 'healthy'
	}

	# Проверка порогов для алертов
	if data['cpu_percent'] > 80:
	    data['alerts'] = ['High CPU usage']
	if data['memory_percent'] > 85:
	    data['alerts'] = data.get('alerts', []) + ['High memory usage']

	return JsonResponse(data)

def index(request):
    """Главная страница с информацией о сервере"""
    context = {
        'hostname': platform.node(),
	'os': platform.system(),
	'python_version': platform.python_version(),
    }

    return render(request, 'server_monitor/index.html', context)
