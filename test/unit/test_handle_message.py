import unittest
from unittest.mock import patch, MagicMock
import datetime
from main import handle_message, user_sessions, turn_counts, last_received_times

class TestHandleMessage(unittest.TestCase):

    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key', 'SYSTEM_PROMPT': 'test_prompt', 'MAX_TURNS': '10', 'TTL': '600'})
    @patch('main.AIChat')
    def test_reset_command(self, mock_chat):
        mock_instance = MagicMock()
        mock_chat.return_value = mock_instance
        mock_instance.__call__.return_value = "AI response"

        # Send a message to initiate a session
        handle_message('test', 'User message')
        self.assertEqual(turn_counts.get('test'), 1)

        # Send a '/reset' command
        mock_instance.__call__.return_value = "Your session has been reset. How can I assist you now?"
        response = handle_message('test', '/reset')
        self.assertEqual(response.get_json(), {'text': "Your session has been reset. How can I assist you now?"})
        self.assertEqual(turn_counts.get('test'), 0)  # Check that the turn count has been reset


    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key', 'SYSTEM_PROMPT': 'test_prompt', 'MAX_TURNS': '10', 'TTL': '600'})
    @patch('main.AIChat')
    @patch('main.datetime')
    def test_turn_count_limit(self, mock_datetime, mock_chat):
        mock_instance = MagicMock()
        mock_chat.return_value = mock_instance
        mock_instance.__call__.return_value = "AI response"
        mock_datetime.datetime.now.return_value = datetime.datetime(2022, 1, 1, 0, 0)

        for i in range(10):  # Send 10 messages
            handle_message('test', 'User message')
        self.assertEqual(turn_counts.get('test'), 10)

        handle_message('test', 'User message')  # Send 11th message
        self.assertEqual(turn_counts.get('test'), 1)  # Check that the turn count has been reset


    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key', 'SYSTEM_PROMPT': 'test_prompt', 'MAX_TURNS': '10', 'TTL': '600'})
    @patch('main.AIChat')
    @patch('main.datetime')
    def test_ttl_limit(self, mock_datetime, mock_chat):
        mock_instance = MagicMock()
        mock_chat.return_value = mock_instance
        mock_instance.__call__.return_value = "AI response"

        mock_datetime.datetime.now.return_value = datetime.datetime(2022, 1, 1, 0, 0)  # Set current time
        handle_message('test', 'User message')
        self.assertEqual(last_received_times.get('test'), datetime.datetime(2022, 1, 1, 0, 0))

        mock_datetime.datetime.now.return_value = datetime.datetime(2022, 1, 1, 0, 11)  # Update current time to be more than TTL
        handle_message('test', 'User message')
        self.assertEqual(turn_counts.get('test'), 1)  # Check that the turn count has been reset due to TTL expiry
        self.assertEqual(last_received_times.get('test'), datetime.datetime(2022, 1, 1, 0, 11))  # Check that the last received time has been updated

    def tearDown(self):
        user_sessions.clear()
        turn_counts.clear()
        last_received_times.clear()

if __name__ == '__main__':
    unittest.main()