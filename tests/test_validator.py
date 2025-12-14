import unittest
from src.check_email import check_email

class TestEmailValidator(unittest.TestCase):
    
    def test_valid_email(self):
        result = check_email("test@gmail.com")
        self.assertIn("✅", result)
    
    def test_invalid_email(self):
        result = check_email("invalid-email")
        self.assertIn("❌", result)
    
    def test_no_mx_records(self):
        result = check_email("test@nonexistent-domain-12345.com")
        self.assertIn("❌", result)

if __name__ == '__main__':
    unittest.main()
