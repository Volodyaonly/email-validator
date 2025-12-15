"""
End-to-end tests for the complete system
"""
import pytest
import tempfile
import os
from pathlib import Path


class TestEndToEnd:
    """End-to-end test cases"""
    
    @pytest.mark.e2e
    @pytest.mark.slow
    def test_complete_workflow(self, tmp_path):
        """Test complete workflow from file to validation"""
        # Создаем тестовый файл с email адресами
        email_file = tmp_path / "test_emails.txt"
        email_content = """test@gmail.com
invalid-email
test@mail.ru
"""
        email_file.write_text(email_content)
        
        # Создаем конфигурацию
        config_file = tmp_path / "config.ini"
        config_content = """[telegram]
bot_token = fake_token_for_testing
chat_id = 123456789
"""
        config_file.write_text(config_content)
        
        # Импортируем модули
        from src.check_email import check_email, process_file
        
        # Проверяем обработку файла
        emails = process_file(str(email_file))
        assert len(emails) == 3
        
        # Проверяем каждый email
        results = []
        for email in emails:
            result = check_email(email)
            results.append(result)
            assert isinstance(result, str)
            assert email in result
        
        # Убеждаемся что у нас есть разные типы результатов
        result_text = " ".join(results)
        # Должны быть хотя бы какие-то эмодзи статуса
        assert any(emoji in result_text for emoji in ["✅", "❌", "⚠️"])
    
    @pytest.mark.e2e
    @pytest.mark.slow
    def test_command_line_interface(self, tmp_path, capsys):
        """Test CLI interface end-to-end"""
        import sys
        from src.check_email import main as check_email_main
        
        # Создаем тестовый файл
        email_file = tmp_path / "cli_test.txt"
        email_file.write_text("test@gmail.com\ninvalid\n")
        
        # Сохраняем оригинальные аргументы
        original_argv = sys.argv
        
        try:
            # Устанавливаем тестовые аргументы
            sys.argv = ['check_email.py', '--file', str(email_file)]
            
            # Запускаем main
            check_email_main()
            
            # Проверяем вывод
            captured = capsys.readouterr()
            output = captured.out
            
            assert "ПРОВЕРКА MX-ЗАПИСЕЙ" in output
            assert "Всего проверено:" in output
            assert "test@gmail.com" in output
            
        finally:
            # Восстанавливаем аргументы
            sys.argv = original_argv


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "e2e"])
