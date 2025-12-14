param(
    [string]$EmailFile = "data\emails.txt",
    [string]$OutputFile = ""
)

Write-Host "=== ПРОВЕРКА MX-ЗАПИСЕЙ EMAIL АДРЕСОВ ===" -ForegroundColor Cyan
Write-Host ""

# Проверяем Python
try {
    python --version 2>&1 | Out-Null
    Write-Host "✓ Python найден" -ForegroundColor Green
} catch {
    Write-Host "❌ Python не найден" -ForegroundColor Red
    Write-Host "Установите Python с https://python.org" -ForegroundColor Yellow
    exit 1
}

# Проверяем файл с email адресами
if (-not (Test-Path $EmailFile)) {
    Write-Host "Файл $EmailFile не найден. Создаем пример..." -ForegroundColor Yellow
    @"
john.doe@gmail.com
jane.smith@yahoo.com
info@company.com
contact@business.org
test@nonexistent-domain-12345.com
invalid-email-address
support@example.com
sales@mail.ru
admin@yandex.ru
user@outlook.com
"@ | Out-File -FilePath $EmailFile -Encoding UTF8
    Write-Host "✓ Создан файл: $EmailFile" -ForegroundColor Green
}

# Устанавливаем зависимости
Write-Host "Проверка зависимостей Python..." -ForegroundColor Yellow
pip install dnspython requests -q 2>$null
Write-Host "✓ Зависимости установлены" -ForegroundColor Green

# Формируем команду Python
$pythonCommand = "python src/check_email.py --file `"$EmailFile`""

if ($OutputFile) {
    $pythonCommand += " --output `"$OutputFile`""
}

Write-Host ""
Write-Host "Запуск проверки..." -ForegroundColor Green
Write-Host "Команда: $pythonCommand" -ForegroundColor Gray
Write-Host ""

# Запускаем Python скрипт
Invoke-Expression $pythonCommand

# Если указан выходной файл, показываем его содержимое
if ($OutputFile -and (Test-Path $OutputFile)) {
    Write-Host ""
    Write-Host "Содержимое выходного файла ($OutputFile):" -ForegroundColor Cyan
    Get-Content $OutputFile
}
