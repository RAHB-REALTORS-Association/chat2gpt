import unittest
from unittest.mock import Mock, patch
from main import process_event

class TestProcessEvent(unittest.TestCase):

    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key', 'SYSTEM_PROMPT': 'test_prompt'})
    def setUp(self):
        self.request = Mock()


    def test_added_to_space(self):
        self.request.get_json.return_value = {'type': 'ADDED_TO_SPACE', 'user': {'name': 'test'}}
        self.assertEqual(process_event(self.request).get_json(), {'text': 'Hello! I am your Chat bot. How can I assist you today?'})


    @patch('main.handle_message')
    def test_message_event(self, mock_handle_message):
        self.request.get_json.return_value = {'type': 'MESSAGE', 'user': {'name': 'test'}, 'message': {'text': 'Hi!'}}
        process_event(self.request)
        mock_handle_message.assert_called_once_with('test', 'Hi!')


    def test_unknown_event(self):
        self.request.get_json.return_value = {'type': 'UNKNOWN', 'user': {'name': 'test'}}
        self.assertEqual(process_event(self.request).get_json(), {'text': 'Sorry, I can only process messages and being added to a space.'})


    def test_malformed_request(self):
        self.request.get_json.side_effect = Exception()
        self.assertEqual(process_event(self.request).get_json(), {'text': 'Sorry, I encountered an error while processing your message.'})


if __name__ == '__main__':
    unittest.main()