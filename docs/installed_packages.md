# Основные системные пакеты:

## 1. Базовые утилиты
- git - система контроля версий
- curl - утилита для передачи данных
- wget - утилита для загрузки файлов
- htop - монитор процессов
- neofetch - информация о системе

## 2. Редакторы и файловый менеджер
- vim - текстовый редактор
- nano - простой текстовый редактор
- mc (Midnight Commander) - файловый менеджер
- tree - отображение структуры каталогов

## 3. Сетевые утилиты
- openssh-server - SSH сервер
- net-tools - сетевые утилиты (ifconfig, netstat)

## 4. Python окружение
- python3 - Python интерпретатор
- python3-pip - менеджер пакетов Python
- python3-venv - виртуальные окружения Python

## 5. База данных
- postgresql - система управления базами данных PostgreSQL
- postgresql-contrib - дополнительные модули PostgreSQL

## 6. Веб-сервер
- nginx - высокопроизводительный веб-сервер

## 7. Безопасность
- fail2ban - защита от brute-force атак
- ufw (Uncomplicated Firewall) - простой фаервол

## 8. Мониторинг
- prometheus-node-exporter - экспортер метрик для Prometheus

## 9. Контейнеризация
- docker.io - платформа контейнеризации Docker
- docker-compose - оркестрация Docker контейнеров

# Версии пакетов:

## Проверенные версии:
- **git**:  done
- **nginx**:  done
- **postgresql**:  done
- **python3**:  done
- **docker.io**:  done

## Команды для проверки:
```bash
# Проверить конкретный пакет
apt-cache policy название_пакета

# Посмотреть все установленные пакеты
dpkg --get-selections | grep -v deinstall
```
