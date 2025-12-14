#!/usr/bin/env python3
"""
Отправка сообщений в Telegram через API бота
"""

import requests
import configparser
import argparse
from pathlib import Path

def load_config(config_file='config.ini'):
    """Загружает конфигурацию из файла"""
    config = configparser.ConfigParser()
    config.read(config_file)
    
    if 'telegram' not in config:
        raise ValueError("Секция [telegram] не найдена в config.ini")
    
    return config['telegram']

def send_to_telegram(message, config_file='config.ini'):
    """Отправляет сообщение в Telegram"""
    
    try:
        config = load_config(config_file)
        token = config.get('bot_token')
        chat_id = config.get('chat_id')
        
        if not token or token == 'ваш_токен_бота_здесь':
            print("❌ Токен бота не настроен. Отредактируйте config.ini")
            return False
            
        if not chat_id or chat_id == 'ваш_chat_id_здесь':
            print("❌ Chat ID не настроен. Отредактируйте config.ini")
            return False
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("✅ Сообщение успешно отправлено в Telegram")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка отправки в Telegram: {e}")
        return False
    except ValueError as e:
        print(f"❌ Ошибка конфигурации: {e}")
        return False

def send_file_to_telegram(filename, config_file='config.ini'):
    """Отправляет содержимое файла в Telegram"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        message = f"📄 Файл: {Path(filename).name}\n\n{content}"
        return send_to_telegram(message, config_file)
    except FileNotFoundError:
        print(f"❌ Файл не найден: {filename}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Отправка сообщений в Telegram')
    parser.add_argument('-m', '--message', help='Текст сообщения')
    parser.add_argument('-f', '--file', help='Отправить содержимое файла')
    
    args = parser.parse_args()
    
    if args.file:
        send_file_to_telegram(args.file)
    elif args.message:
        send_to_telegram(args.message)
    else:
        # Тестовое сообщение по умолчанию
        message = """🚀 ТЕСТОВОЕ СООБЩЕНИЕ ОТ EMAIL VALIDATOR

📅 Дата: 10.12.2025
⏰ Время: 09:13:32

✅ Система работает корректно

📊 СТАТУС СИСТЕМЫ:
• Проверка MX-записей: Работает
• Отправка в Telegram: Работает

🔧 ВОЗМОЖНОСТИ СИСТЕМЫ:
1. Проверка email-адресов
2. Отправка сообщений через Telegram-бота
3. Многоуровневая архитектура с отказоустойчивостью

📞 Для связи: используйте Telegram бота"""
        
        send_to_telegram(message)

if __name__ == "__main__":
    main()
