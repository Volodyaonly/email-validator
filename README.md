# Email Validator Tool 🚀

Профессиональный инструмент для валидации email адресов и проверки MX-записей доменов с интеграцией Telegram.

## ✨ Возможности

- ✅ Проверка корректности email адресов (синтаксис + MX записи)
- ✅ Массовая проверка через файл или одиночные адреса
- ✅ Отправка результатов в Telegram
- ✅ Поддержка PowerShell и Batch скриптов
- ✅ Автоматическая установка зависимостей
- ✅ Безопасное хранение конфигурации

## 📁 Структура проекта

\\\
email-validator/
├── src/                    # Исходный код Python
│   ├── check_email.py     # Основная логика проверки
│   └── telegram_sender.py # Отправка в Telegram
├── scripts/               # Скрипты для запуска
│   ├── powershell/       # PowerShell скрипты
│   └── batch/            # BAT файлы
├── data/                  # Примеры данных
│   ├── emails.txt        # Тестовые email адреса
│   └── example_message.txt
├── tests/                 # Автотесты
├── docs/                  # Документация
├── .gitignore            # Игнорируемые файлы
├── README.md             # Эта документация
├── requirements.txt      # Зависимости Python
├── setup.py             # Установка как пакет
├── config.ini.example    # Пример конфигурации
└── LICENSE              # Лицензия MIT
\\\

## ⚡ Быстрый старт
 1. Установка зависимостей
\\\ash
pip install -r requirements.txt
\\\

 2. Настройка конфигурации
\\\ash
# Скопируйте пример конфигурации
cp config.ini.example config.ini

# Отредактируйте config.ini:
# - Получите токен бота у @BotFather
# - Узнайте chat_id у @userinfobot
\\\

 3. Проверка email адресов
\\\ash
 Через Python
python src/check_email.py --file data/emails.txt

 Через PowerShell
.\scripts\powershell\check_email.ps1

 Через Batch файл
.\scripts\batch\start_all.bat
\\\

 🔧 Использование

 Проверка одного email
\\\ash
python src/check_email.py --email "test@example.com"
\\\

 Проверка файла с email адресами
\\\ash
python src/check_email.py --file "data/emails.txt"
\\\

 Отправка тестового сообщения в Telegram
\\\ash
python src/telegram_sender.py
\\\

 📝 Примеры

 emails.txt
\\\
john.doe@gmail.com
jane.smith@yahoo.com
info@company.com
test@nonexistent-domain.com
invalid-email-address
\\\

 Результат проверки
\\\
=== ПРОВЕРКА MX-ЗАПИСЕЙ EMAIL АДРЕСОВ ===
==================================================
john.doe@gmail.com: ✅ домен валиден (MX записи найдены)
jane.smith@yahoo.com: ✅ домен валиден (MX записи найдены)
info@company.com: ✅ домен валиден (MX записи найдены)
test@nonexistent-domain.com: ❌ домен отсутствует
invalid-email-address: ❌ некорректный email
==================================================
Всего проверено: 5
Валидных: 3
Невалидных: 2
\\\

 🔧 Технические детали

 Зависимости
- Python 3.6+
- dnspython>=2.3.0
- requests>=2.28.0

 Поддерживаемые проверки
1. **Синтаксис email** (RFC 5322)
2. **MX записи домена** (через DNS запросы)
3. **Существование домена** (NXDOMAIN проверка)

 🚀 Расширенные возможности

 Telegram бот
- Отправка результатов проверки
- Уведомления о статусе системы
- Поддержка форматирования сообщений

 Архитектура для масштабирования
- Поддержка 1200+ email адресов
- Интеграция с Amazon SES, Mailgun, SendGrid
- Мониторинг через Prometheus + Grafana
- Автоматическая ротация аккаунтов

 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл LICENSE.

 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для ваших изменений
3. Сделайте коммит с описанием изменений
4. Отправьте пул-реквест

 📞 Поддержка

Для вопросов и предложений:
1. Создайте Issue в репозитории
2. Напишите в Telegram бот
3. Проверьте документацию в папке docs/
