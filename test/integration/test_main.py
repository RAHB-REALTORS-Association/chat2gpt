import unittest
from unittest.mock import patch, MagicMock
import datetime
from main import handle_message, user_sessions, turn_counts, last_received_times

class TestIntegration(unittest.TestCase):

    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key', 'SYSTEM_PROMPT': 'test_prompt', 'MAX_TURNS': '10', 'TTL': '600'})
    @patch('main.AIChat')
    def test_session_maintenance(self, mock_chat):
        mock_instance = MagicMock()
        mock_chat.return_value = mock_instance
        mock_instance.__call__.return_value = "AI response"

        # Send several messages in sequence from the same user
        for i in range(5):
            handle_message('test', 'User message')
        self.assertEqual(turn_counts.get('test'), 5)

        # Issue a '/reset' command
        mock_instance.__call__.return_value = "Your session has been reset. How can I assist you now?"
        response = handle_message('test', '/reset')
        self.assertEqual(response.get_json(), {'text': "Your session has been reset. How can I assist you now?"})
        self.assertEqual(turn_counts.get('test'), 0)  # Check that the turn count is reset


    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key', 'SYSTEM_PROMPT': 'test_prompt', 'MAX_TURNS': '10', 'TTL': '600'})
    @patch('main.AIChat')
    @patch('main.num_tokens_from_string')
    def test_token_counting_and_response_generation(self, mock_token_counting, mock_chat):
        mock_instance = MagicMock()
        mock_chat.return_value = mock_instance
        mock_instance.__call__.return_value = "AI response"
        mock_token_counting.return_value = 10

        response = handle_message('test', 'User message')
        mock_token_counting.assert_called_once_with('User message' + 'test_prompt')
        mock_instance.__call__.assert_called_once_with('User message')
        self.assertEqual(response.get_json(), {'text': 'AI response'})


    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key', 'SYSTEM_PROMPT': 'test_prompt', 'MAX_TURNS': '10', 'TTL': '600'})
    @patch('main.AIChat')
    def test_exceeding_max_turns(self, mock_chat):
        mock_instance = MagicMock()
        mock_chat.return_value = mock_instance
        mock_instance.__call__.return_value = "AI response"

        # Send a sequence of messages that exceeds the maximum number of turns
        for i in range(11):
            handle_message('test', 'User message')
        self.assertEqual(turn_counts.get('test'), 1)  # Check that the turn count has been reset


    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key', 'SYSTEM_PROMPT': 'test_prompt', 'MAX_TURNS': '10', 'TTL': '600'})
    @patch('main.AIChat')
    @patch('main.datetime')
    def test_ttl_expiry(self, mock_datetime, mock_chat):
        mock_instance = MagicMock()
        mock_chat.return_value = mock_instance
        mock_instance.__call__.return_value = "AI response"

        # Send a message
        mock_datetime.datetime.now.return_value = datetime.datetime(2022, 1, 1, 0, 0)
        handle_message('test', 'User message')

        # Wait for a period longer than the TTL and then send another message
        mock_datetime.datetime.now.return_value = datetime.datetime(2022, 1, 1, 0, 11)
        handle_message('test', 'User message')
        self.assertEqual(turn_counts.get('test'), 1)  # Check that the turn count has been reset


    def tearDown(self):
        user_sessions.clear()
        turn_counts.clear()
        last_received_times.clear()


if __name__ == '__main__':
    unittest.main()