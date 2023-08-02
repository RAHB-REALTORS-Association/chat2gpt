import os
import unittest
from unittest.mock import patch, MagicMock
import datetime
from main import handle_message, process_event, user_sessions, turn_counts, last_received_times, MAX_TURNS, TTL

os.environ['OPENAI_API_KEY'] = 'test'
os.environ['SYSTEM_PROMPT'] = 'test'
os.environ['MAX_TURNS'] = '10'
os.environ['TTL'] = '600'

class TestHandleMessage(unittest.TestCase):
    @patch('main.AIChat')
    def test_max_turns(self, mock_aichat):
        user_id = 'test_user'
        user_message = 'Hello, bot!'
        mock_aichat_instance = mock_aichat.return_value
        mock_aichat_instance.__call__ = MagicMock(return_value='Hello, user!')

        # Send MAX_TURNS + 1 messages
        for _ in range(int(MAX_TURNS) + 1):
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
        mock_aichat_instance = mock_aichat.return_value
        mock_aichat_instance.__call__ = MagicMock(return_value='Hello, user!')

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

    @patch('main.AIChat')
    def test_process_event(self, mock_aichat):
        event_data_message = {
            'type': 'MESSAGE',
            'user': {'name': 'test_user'},
            'message': {'text': 'Hello, bot!'}
        }
        mock_aichat_instance = mock_aichat.return_value
        mock_aichat_instance.__call__ = MagicMock(return_value='Hello, user!')
        response = process_event(MagicMock(get_json=MagicMock(return_value=event_data_message)))
        self.assertEqual(response.get_json(), {'text': 'Hello, user!'})
    
        event_data_added_to_space = {
            'type': 'ADDED_TO_SPACE',
            'user': {'name': 'test_user'}
        }
        response = process_event(MagicMock(get_json=MagicMock(return_value=event_data_added_to_space)))
        self.assertEqual(response.get_json(), {'text': 'Hello! I am your Chat bot. How can I assist you today?'})
    
        event_data_unknown_type = {
            'type': 'UNKNOWN_TYPE',
            'user': {'name': 'test_user'}
        }
        response = process_event(MagicMock(get_json=MagicMock(return_value=event_data_unknown_type)))
        self.assertEqual(response.get_json(), {'text': 'Sorry, I can only process messages and being added to a space.'})

if __name__ == '__main__':
    unittest.main()