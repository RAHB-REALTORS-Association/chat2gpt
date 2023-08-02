import unittest
from unittest.mock import patch, MagicMock
import datetime
from main import handle_message, user_sessions, turn_counts, last_received_times

class TestHandleMessage(unittest.TestCase):
    @patch('main.AIChat')

    def test_max_turns(self, mock_aichat):
        user_id = 'test_user'
        user_message = 'Hello, bot!'
        mock_aichat.return_value = MagicMock(**{'__call__.return_value': 'Hello, user!'})

        # Send MAX_TURNS + 1 messages
        for _ in range(MAX_TURNS + 1):
            response = handle_message(user_id, user_message)
            self.assertEqual(response.get_json(), {'text': 'Hello, user!'})
            self.assertIsNotNone(user_sessions.get(user_id))

        # Check that turn count has been reset
        self.assertEqual(turn_counts.get(user_id), 1)

    @patch('main.AIChat')
    @patch('main.datetime')

  
    def test_ttl_expiration(self, mock_datetime, mock_aichat):
        user_id = 'test_user'
        user_message = 'Hello, bot!'
        mock_aichat.return_value = MagicMock(**{'__call__.return_value': 'Hello, user!'})

        # First message
        mock_datetime.datetime.now.return_value = datetime.datetime(2022, 1, 1, 0, 0)
        response = handle_message(user_id, user_message)
        self.assertEqual(response.get_json(), {'text': 'Hello, user!'})
        self.assertIsNotNone(user_sessions.get(user_id))
        self.assertEqual(turn_counts.get(user_id), 1)
        self.assertEqual(last_received_times.get(user_id), datetime.datetime(2022, 1, 1, 0, 0))

        # Second message, after TTL has expired
        mock_datetime.datetime.now.return_value = datetime.datetime(2022, 1, 1, 0, 11)
        response = handle_message(user_id, user_message)
        self.assertEqual(response.get_json(), {'text': 'Hello, user!'})
        self.assertIsNotNone(user_sessions.get(user_id))
        self.assertEqual(turn_counts.get(user_id), 1)  # Turn count has been reset
        self.assertEqual(last_received_times.get(user_id), datetime.datetime(2022, 1, 1, 0, 11))  # Last received time has been updated


if __name__ == '__main__':
    unittest.main()
