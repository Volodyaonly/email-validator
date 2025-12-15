"""
Unit tests for Telegram sender functionality
"""
import pytest
from unittest.mock import patch, MagicMock, mock_open
import requests
from src.telegram_sender import send_to_telegram, send_file_to_telegram, load_config


class TestTelegramSender:
    """Test cases for Telegram sender"""
    
    # Фикстуры
    @pytest.fixture
    def valid_config(self, tmp_path):
        """Create a valid config file for testing"""
        config_content = """
[telegram]
bot_token = test_token_12345
chat_id = 123456789
"""
        config_file = tmp_path / "config.ini"
        config_file.write_text(config_content)
        return str(config_file)
    
    @pytest.fixture
    def invalid_config(self, tmp_path):
        """Create an invalid config file for testing"""
        config_content = """
[wrong_section]
key = value
"""
        config_file = tmp_path / "config_invalid.ini"
        config_file.write_text(config_content)
        return str(config_file)
    
    # Тесты для загрузки конфигурации
    def test_load_config_success(self, valid_config):
        """Test loading valid configuration"""
        config = load_config(valid_config)
        assert config['bot_token'] == 'test_token_12345'
        assert config['chat_id'] == '123456789'
    
    def test_load_config_file_not_found(self):
        """Test loading non-existent config file"""
        with pytest.raises(ValueError, match="Секция \\[telegram\\] не найдена"):
            load_config("nonexistent.ini")
    
    def test_load_config_invalid_section(self, invalid_config):
        """Test config without telegram section"""
        with pytest.raises(ValueError, match="Секция \\[telegram\\] не найдена"):
            load_config(invalid_config)
    
    # Тесты для отправки сообщений
    @patch('src.telegram_sender.requests.post')
    def test_send_to_telegram_success(self, mock_post, valid_config):
        """Test successful message sending"""
        # Настраиваем мок
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'ok': True, 'result': {}}
        mock_post.return_value = mock_response
        
        result = send_to_telegram("Test message", valid_config)
        assert result is True
        
        # Проверяем что запрос был сделан правильно
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert "https://api.telegram.org/bottest_token_12345/sendMessage" in args[0]
        assert kwargs['json']['chat_id'] == '123456789'
        assert kwargs['json']['text'] == 'Test message'
    
    @patch('src.telegram_sender.requests.post')
    def test_send_to_telegram_network_error(self, mock_post, valid_config):
        """Test network error when sending message"""
        mock_post.side_effect = requests.exceptions.ConnectionError("Network error")
        
        result = send_to_telegram("Test message", valid_config)
        assert result is False
    
    @patch('src.telegram_sender.requests.post')
    def test_send_to_telegram_api_error(self, mock_post, valid_config):
        """Test Telegram API error"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("API error")
        mock_post.return_value = mock_response
        
        result = send_to_telegram("Test message", valid_config)
        assert result is False
    
    def test_send_to_telegram_missing_token(self, tmp_path):
        """Test with missing bot token in config"""
        config_content = """
[telegram]
bot_token = ваш_токен_бота_здесь
chat_id = 123456789
"""
        config_file = tmp_path / "config.ini"
        config_file.write_text(config_content)
        
        result = send_to_telegram("Test message", str(config_file))
        assert result is False
    
    def test_send_to_telegram_missing_chat_id(self, tmp_path):
        """Test with missing chat ID in config"""
        config_content = """
[telegram]
bot_token = real_token
chat_id = ваш_chat_id_здесь
"""
        config_file = tmp_path / "config.ini"
        config_file.write_text(config_content)
        
        result = send_to_telegram("Test message", str(config_file))
        assert result is False
    
    # Тесты для отправки файлов
    @patch('src.telegram_sender.send_to_telegram')
    def test_send_file_to_telegram_success(self, mock_send, tmp_path, valid_config):
        """Test successful file sending"""
        # Создаем тестовый файл
        test_file = tmp_path / "test.txt"
        test_file.write_text("File content")
        
        mock_send.return_value = True
        
        result = send_file_to_telegram(str(test_file), valid_config)
        assert result is True
        
        # Проверяем что send_to_telegram была вызвана с правильным сообщением
        mock_send.assert_called_once()
        call_args = mock_send.call_args[0]
        assert "📄 Файл: test.txt" in call_args[0]
        assert "File content" in call_args[0]
    
    @patch('src.telegram_sender.send_to_telegram')
    def test_send_file_to_telegram_not_found(self, mock_send, valid_config):
        """Test sending non-existent file"""
        result = send_file_to_telegram("nonexistent.txt", valid_config)
        assert result is False
        mock_send.assert_not_called()
    
    # Тесты граничных случаев
    @patch('src.telegram_sender.requests.post')
    def test_send_to_telegram_empty_message(self, mock_post, valid_config):
        """Test sending empty message"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        result = send_to_telegram("", valid_config)
        # Telegram API позволяет отправлять пустые сообщения?
        # Проверяем хотя бы что функция не падает
        assert isinstance(result, bool)
    
    @patch('src.telegram_sender.requests.post')
    def test_send_to_telegram_long_message(self, mock_post, valid_config):
        """Test sending very long message"""
        long_message = "A" * 4096  # Длинное сообщение
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        result = send_to_telegram(long_message, valid_config)
        # Проверяем что функция была вызвана
        assert mock_post.called
        # Проверяем что длинное сообщение было отправлено
        args, kwargs = mock_post.call_args
        assert kwargs['json']['text'] == long_message


class TestTelegramSenderIntegration:
    """Integration tests for Telegram sender"""
    
    @pytest.mark.integration
    @pytest.mark.slow
    @patch('src.telegram_sender.requests.post')
    def test_real_telegram_api_call(self, mock_post):
        """Integration test with mocked Telegram API"""
        # Здесь можно протестировать с реальным токеном (осторожно!)
        # Или использовать моки для проверки формата запроса
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
