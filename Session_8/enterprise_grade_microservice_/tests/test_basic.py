```python
import unittest
from unittest.mock import patch, MagicMock
from your_module import YourClass

class TestYourClass(unittest.TestCase):

    @patch('your_module.YourClass')
    def test_your_method(self, mock_your_class):
        # Arrange
        mock_your_class.return_value = MagicMock()
        mock_your_class.return_value.your_method.return_value = 'expected_result'

        # Act
        result = YourClass().your_method()

        # Assert
        self.assertEqual(result, 'expected_result')
        mock_your_class.return_value.your_method.assert_called_once()

    @patch('your_module.YourClass')
    def test_your_method_with_error(self, mock_your_class):
        # Arrange
        mock_your_class.return_value = MagicMock()
        mock_your_class.return_value.your_method.side_effect = Exception('test exception')

        # Act and Assert
        with self.assertRaises(Exception):
            YourClass().your_method()

    def test_your_method_without_mock(self):
        # Act and Assert
        with self.assertRaises(NotImplementedError):
            YourClass().your_method()

if __name__ == '__main__':
    unittest.main()
```