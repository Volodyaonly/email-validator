"""
Pytest configuration and fixtures
"""
import pytest
import tempfile
import os
from pathlib import Path


def pytest_configure(config):
    """Pytest configuration hook"""
    # Регистрируем пользовательские маркеры
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as end-to-end test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


@pytest.fixture
def sample_emails():
    """Fixture providing sample emails for testing"""
    return [
        "valid@gmail.com",
        "another@yahoo.com",
        "invalid-email",
        "test@nonexistent-domain-12345.com",
        "user@mail.ru",
    ]


@pytest.fixture
def email_file(tmp_path, sample_emails):
    """Create temporary email file for testing"""
    file_path = tmp_path / "test_emails.txt"
    file_path.write_text("\n".join(sample_emails))
    return str(file_path)


@pytest.fixture
def valid_config(tmp_path):
    """Create valid config file for Telegram tests"""
    config_content = """[telegram]
bot_token = test_bot_token_1234567890
chat_id = 123456789

[email]
default_file = data/emails.txt
timeout = 10

[logging]
level = INFO
file = test.log
"""
    config_file = tmp_path / "config.ini"
    config_file.write_text(config_content)
    return str(config_file)


@pytest.fixture
def invalid_config(tmp_path):
    """Create invalid config file for Telegram tests"""
    config_content = """[wrong_section]
key = value
"""
    config_file = tmp_path / "config_invalid.ini"
    config_file.write_text(config_content)
    return str(config_file)


@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """Setup test environment before each test"""
    # Устанавливаем временную папку для тестов
    temp_dir = tempfile.mkdtemp()
    monkeypatch.setenv('TEST_TEMP_DIR', temp_dir)
    
    # Меняем текущую рабочую директорию
    original_cwd = os.getcwd()
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    yield
    
    # Восстанавливаем оригинальную директорию
    os.chdir(original_cwd)
    
    # Очищаем временные файлы
    import shutil
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)


# Хук для игнорирования медленных тестов по умолчанию
def pytest_addoption(parser):
    parser.addoption(
        "--run-slow", action="store_true", default=False, help="run slow tests"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-slow"):
        # Если указан --run-slow, запускаем все тесты
        return
    
    skip_slow = pytest.mark.skip(reason="need --run-slow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
