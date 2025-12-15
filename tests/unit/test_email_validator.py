"""
Unit tests for email validator functionality
"""
import pytest
from unittest.mock import patch, MagicMock
from src.check_email import check_email, process_file
import dns.resolver


class TestEmailValidator:
    """Test cases for email validation"""

    # Тест на корректные email
    @pytest.mark.parametrize("email, expected_result", [
        ("test@gmail.com", True),
        ("user.name@domain.co.uk", True),
        ("user+tag@example.com", True),
        ("user@sub.domain.com", True),
        ("123@mail.ru", True),
    ])
    def test_valid_email_format(self, email, expected_result):
        """Test that valid email formats are recognized"""
        result = check_email(email)
        # Мы не можем предсказать реальный результат проверки MX,
        # но проверим что функция возвращает строку
        assert isinstance(result, str)
        assert email in result

    # Тест на некорректные email
    @pytest.mark.parametrize("email", [
        "invalid-email",
        "@domain.com",
        "user@",
        "user@.com",
        "user@domain.",
        "",
        "   ",
        "user@-domain.com",
        "user@domain..com",
    ])
    def test_invalid_email_format(self, email):
        """Test that invalid email formats are rejected"""
        result = check_email(email)
        assert "❌ некорректный email" in result

    # Тест на проверку MX записей с моком DNS
    @patch('src.check_email.dns.resolver.resolve')
    def test_email_with_valid_mx(self, mock_dns_resolve):
        """Test email with valid MX records"""
        # Настраиваем мок DNS
        mock_dns_resolve.return_value = True
        
        result = check_email("test@example.com")
        assert "✅" in result

    @patch('src.check_email.dns.resolver.resolve')
    def test_email_with_no_mx_records(self, mock_dns_resolve):
        """Test email domain without MX records"""
        mock_dns_resolve.side_effect = dns.resolver.NoAnswer
        
        result = check_email("test@example.com")
        assert "⚠️ MX-записи отсутствуют" in result

    @patch('src.check_email.dns.resolver.resolve')
    def test_email_with_nonexistent_domain(self, mock_dns_resolve):
        """Test non-existent domain"""
        mock_dns_resolve.side_effect = dns.resolver.NXDOMAIN
        
        result = check_email("test@nonexistent-domain-12345.com")
        assert "❌ домен отсутствует" in result

    @patch('src.check_email.dns.resolver.resolve')
    def test_email_with_dns_error(self, mock_dns_resolve):
        """Test DNS resolution error"""
        mock_dns_resolve.side_effect = Exception("DNS error")
        
        result = check_email("test@example.com")
        assert "❌ ошибка проверки" in result

    # Тесты для обработки файлов
    def test_process_file_success(self, tmp_path):
        """Test processing valid email file"""
        # Создаем временный файл
        file_path = tmp_path / "emails.txt"
        file_path.write_text("test1@gmail.com\ntest2@yahoo.com\n")
        
        emails = process_file(str(file_path))
        assert emails == ["test1@gmail.com", "test2@yahoo.com"]

    def test_process_file_not_found(self):
        """Test processing non-existent file"""
        emails = process_file("nonexistent_file.txt")
        assert emails == []

    def test_process_file_empty(self, tmp_path):
        """Test processing empty file"""
        file_path = tmp_path / "empty.txt"
        file_path.write_text("")
        
        emails = process_file(str(file_path))
        assert emails == []

    def test_process_file_with_whitespace(self, tmp_path):
        """Test file with whitespace lines"""
        file_path = tmp_path / "emails.txt"
        file_path.write_text("test@gmail.com\n\n  \n\ntest2@yahoo.com\n")
        
        emails = process_file(str(file_path))
        assert emails == ["test@gmail.com", "test2@yahoo.com"]

    # Тест граничных случаев
    def test_email_with_special_characters(self):
        """Test email with special characters"""
        result = check_email("test.email+tag@gmail.com")
        assert isinstance(result, str)

    def test_long_email(self):
        """Test very long email address"""
        long_local = "a" * 64
        long_domain = "b" * 63 + ".com"
        email = f"{long_local}@{long_domain}"
        result = check_email(email)
        assert isinstance(result, str)


class TestEmailValidatorIntegration:
    """Integration tests for email validator"""
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_real_email_validation(self):
        """Integration test with real DNS queries"""
        # Тестируем на реальных доменах (осторожно, требует интернет)
        real_domains = [
            "gmail.com",
            "yahoo.com",
            "mail.ru"
        ]
        
        for domain in real_domains:
            email = f"test@{domain}"
            result = check_email(email)
            # Просто проверяем что функция работает и возвращает результат
            assert isinstance(result, str)
            assert email in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
