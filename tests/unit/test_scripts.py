"""
Tests for PowerShell and batch scripts functionality
"""
import pytest
import subprocess
import sys
import os
from pathlib import Path


class TestScripts:
    """Test cases for script files"""
    
    @pytest.fixture
    def project_root(self):
        """Get project root directory"""
        return Path(__file__).parent.parent.parent
    
    def test_powershell_script_exists(self, project_root):
        """Check that PowerShell script exists"""
        script_path = project_root / "scripts" / "powershell" / "check_email.ps1"
        assert script_path.exists(), f"Script not found: {script_path}"
    
    def test_batch_script_exists(self, project_root):
        """Check that batch script exists"""
        script_path = project_root / "scripts" / "batch" / "start_all.bat"
        assert script_path.exists(), f"Script not found: {script_path}"
    
    def test_scripts_have_correct_content(self, project_root):
        """Check scripts have required content"""
        # Проверяем PowerShell скрипт
        ps_script = project_root / "scripts" / "powershell" / "check_email.ps1"
        content = ps_script.read_text(encoding='utf-8')
        
        assert 'param(' in content  # Должен принимать параметры
        assert 'python src/check_email.py' in content  # Должен вызывать Python скрипт
        
        # Проверяем batch скрипт
        batch_script = project_root / "scripts" / "batch" / "start_all.bat"
        content = batch_script.read_text(encoding='utf-8')
        
        assert '@echo off' in content  # Должен быть batch заголовок
        assert 'python src/check_email.py' in content  # Должен вызывать Python
    
    @pytest.mark.integration
    @pytest.mark.skipif(sys.platform != "win32", reason="Requires Windows")
    def test_powershell_script_execution(self, project_root, tmp_path):
        """Test PowerShell script execution on Windows"""
        # Создаем тестовый файл с email
        test_file = tmp_path / "test_emails.txt"
        test_file.write_text("test@gmail.com\n")
        
        script_path = project_root / "scripts" / "powershell" / "check_email.ps1"
        
        # Запускаем PowerShell скрипт
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", 
             str(script_path), "-EmailFile", str(test_file)],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        
        # Проверяем что скрипт выполнился без критических ошибок
        assert result.returncode == 0 or result.returncode == 1  # 1 может быть если email невалидный
        
        # Проверяем что в выводе есть ожидаемый текст
        assert "ПРОВЕРКА MX-ЗАПИСЕЙ" in result.stdout or "ПРОВЕРКА MX-ЗАПИСЕЙ" in result.stderr


class TestRequirements:
    """Test requirements and dependencies"""
    
    def test_requirements_file_exists(self, project_root):
        """Check requirements.txt exists"""
        req_file = project_root / "requirements.txt"
        assert req_file.exists()
        
        content = req_file.read_text()
        assert 'dnspython' in content
        assert 'pytest' in content
    
    def test_can_import_main_modules(self):
        """Test that main modules can be imported"""
        # Эта проверка гарантирует что структура проекта корректна
        try:
            from src import check_email
            from src import telegram_sender
            assert True
        except ImportError as e:
            pytest.fail(f"Import error: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
