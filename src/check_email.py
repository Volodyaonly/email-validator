#!/usr/bin/env python3
"""
Email Validator - проверка email адресов через MX-записи
"""

import sys
import argparse
import dns.resolver
import re

def check_email(email):
    """Проверяет валидность email адреса и MX-записи домена"""
    email = email.strip()
    if not email:
        return None
    
    # Проверяем формат email
    match = re.search(r'@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', email)
    if not match:
        return f"{email}: ❌ некорректный email"
    
    domain = match.group(1)
    
    try:
        dns.resolver.resolve(domain, 'MX')
        return f"{email}: ✅ домен валиден (MX записи найдены)"
    except dns.resolver.NXDOMAIN:
        return f"{email}: ❌ домен отсутствует"
    except dns.resolver.NoAnswer:
        return f"{email}: ⚠️ MX-записи отсутствуют"
    except Exception as e:
        return f"{email}: ❌ ошибка проверки: {str(e)}"

def process_file(filename):
    """Обрабатывает файл с email адресами"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            emails = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден")
        return []
    
    return emails

def main():
    parser = argparse.ArgumentParser(description='Проверка MX-записей email адресов')
    parser.add_argument('-f', '--file', default='data/emails.txt', 
                       help='Файл с email адресами')
    parser.add_argument('-e', '--email', help='Проверить один email адрес')
    parser.add_argument('-o', '--output', help='Сохранить результаты в файл')
    
    args = parser.parse_args()
    
    print("=== ПРОВЕРКА MX-ЗАПИСЕЙ EMAIL АДРЕСОВ ===")
    print("=" * 50)
    
    valid_count = 0
    total_count = 0
    results = []
    
    if args.email:
        emails = [args.email]
    else:
        emails = process_file(args.file)
    
    for email in emails:
        result = check_email(email)
        if result:
            print(result)
            results.append(result)
            total_count += 1
            if "✅" in result:
                valid_count += 1
    
    print("=" * 50)
    print(f"Всего проверено: {total_count}")
    print(f"Валидных: {valid_count}")
    print(f"Невалидных: {total_count - valid_count}")
    
    # Сохранение в файл если указано
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write("\n".join(results))
                f.write(f"\n\nВсего проверено: {total_count}")
                f.write(f"\nВалидных: {valid_count}")
                f.write(f"\nНевалидных: {total_count - valid_count}")
            print(f"\nРезультаты сохранены в файл: {args.output}")
        except Exception as e:
            print(f"Ошибка сохранения файла: {e}")
    
    return results

if __name__ == "__main__":
    main()
