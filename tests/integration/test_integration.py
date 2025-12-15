"""
Integration tests for the email validator system
"""
import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from src.check_email import main as check_email_main
from src.telegram_sender import main as telegram_main
import sys


class TestIntegration:
    """Integration tests for the whole system"""
    
    @pytest.fixture
    def sample_email_file(self):
        """Create a temporary file with sample emails"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("""test@gmail.com
invalid-email
nonexistent@domain-that-does-not-exist-12345.com
test@mail.ru
""")
            temp_path = f.name
        
        yield temp_path
        
        # Cleanup
        os.unlink(temp_path)
    
    @pytest.fixture
    def mock_dns(self):
        """Mock DNS resolver for integration tests"""
        with patch('src.check_email.dns.resolver.resolve') as mock_resolve:
            # Настраиваем разные ответы для разных доменов
            def side_effect(domain, record_type):
                if 'gmail.com' in str(domain) or 'mail.ru' in str(domain):
                    return MagicMock()  # Успешный ответ
                elif 'domain-that-does-not-exist' in str(domain):
                    raise dns.resolver.NXDOMAIN()
                else:
                    raise dns.resolver.NoAnswer()
            
            mock_resolve.side_effect = side_effect
            yield mock_resolve
    
    def test_full_email_validation_flow(self, sample_email_file, mock_dns, capsys):
        """Test the complete email validation flow"""
        # Сохраняем оригинальные аргументы
        original_argv = sys.argv
        
        try:
            # Устанавливаем аргументы командной строки
            sys.argv = ['check_email.py', '--file', sample_email_file]
            
            # Запускаем main функцию
            check_email_main()
            
            # Перехватываем вывод
            captured = capsys.readouterr()
            output = captured.out
            
            # Проверяем что вывод содержит ожидаемые результаты
            assert "=== ПРОВЕРКА MX-ЗАПИСЕЙ EMAIL АДРЕСОВ ===" in output
            assert "Всего проверено:" in output
            assert "Валидных:" in output
            assert "Невалидных:" in output
            
            # Проверяем конкретные результаты
            assert "test@gmail.com" in output
            assert "invalid-email" in output
            assert "nonexistent@domain-that-does-not-exist-12345.com" in output
            
            # Проверяем что DNS был вызван для реальных доменов
            assert mock_dns.called
            
        finally:
            # Восстанавливаем оригинальные аргументы
            sys.argv = original_argv
    
    def test_email_validation_with_output_file(self, sample_email_file, mock_dns, tmp_path):
        """Test email validation with output to file"""
        output_file = tmp_path / "results.txt"
        
        # Сохраняем оригинальные аргументы
        original_argv = sys.argv
        
        try:
            # Устанавливаем аргументы командной строки
            sys.argv = ['check_email.py', '--file', sample_email_file, '--output', str(output_file)]
            
            # Запускаем main функцию
            check_email_main()
            
            # Проверяем что файл создан
            assert output_file.exists()
            
            # Проверяем содержимое файл
            content = output_file.read_text()
            assert "test@gmail.com" in content
            assert "Всего проверено:" in content
            
        finally:
            # Восстанавливаем оригинальные аргументы
            sys.argv = original_argv
    
    @patch('src.telegram_sender.send_to_telegram')
    def test_telegram_cli_interface(self, mock_send):
        """Test Telegram sender CLI interface"""
        mock_send.return_value = True
        
        # Сохраняем оригинальные аргументы
        original_argv = sys.argv
        
        try:
            # Тест с сообщением из командной строки
            test_message = "Test message from CLI"
            sys.argv = ['telegram_sender.py', '--message', test_message]
            
            telegram_main()
            
            # Проверяем что функция была вызвана с правильным сообщением
            mock_send.assert_called_once()
            assert mock_send.call_args[0][0] == test_message
            
        finally:
            sys.argv = original_argv
    
    def test_single_email_validation(self, mock_dns, capsys):
        """Test validation of single email from command line"""
        original_argv = sys.argv
        
        try:
            sys.argv = ['check_email.py', '--email', 'test@gmail.com']
            
            check_email_main()
            
            captured = capsys.readouterr()
            output = captured.out
            
            assert "test@gmail.com" in output
            assert mock_dns.called
            
        finally:
            sys.argv = original_argv


@pytest.mark.e2e
class TestEndToEnd:
    """End-to-end tests (require real services)"""
    
    @pytest.mark.slow
    def test_real_email_check_with_internet(self):
        """Real email check with internet connection"""
        from src.check_email import check_email
        
        # Используем реальные домены для проверки
        real_emails = [
            "test@gmail.com",      # Должен существовать
            "invalid-format",      # Неправильный формат
        ]
        
        for email in real_emails:
            result = check_email(email)
            assert isinstance(result, str)
            assert email in result
            
            # Логируем результат для отладки
            print(f"{email}: {result}")
    
    @pytest.mark.skip(reason="Requires real Telegram bot token")
    def test_real_telegram_send(self):
        """Real Telegram send test (requires configuration)"""
        # Этот тест должен быть пропущен в CI
        # Для запуска вручную нужно настроить config.ini
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
