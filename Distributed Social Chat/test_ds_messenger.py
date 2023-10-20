# Austin Huang
# austh10@uci.edu
# 28821105

import unittest
from ds_messenger import DirectMessenger

class TestDirectMessenger(unittest.TestCase):
    
    def test_send_message(self):
        messenger = DirectMessenger(dsuserver = '168.235.86.101', username='asduasd', password='testpassasd23')
        message = "hello world"
        recipient = "anna"
        result = messenger.send(message, recipient)
        self.assertTrue(result)

    def test_new(self):
        messenger = DirectMessenger(dsuserver = '168.235.86.101', username='hwoasasdasddaoasd', password='testpa')
        message = "hello welcome to this place"
        recipient = "ColePylasdasdast"
        messenger.send(message, recipient)
        messages = messenger.retrieve_new()
        self.assertIsNotNone(messages)
        the_last_message = messages[-1]
        self.assertEqual(the_last_message['sender'], messenger.username)
        self.assertEqual(the_last_message['recipient'], recipient)
        self.assertEqual(the_last_message['message'], message)

        return messages

    def test_all(self):
        messenger = DirectMessenger(dsuserver = '168.235.86.101', username='asduasd', password='testpassasd23')
        messages = messenger.retrieve_all()
        self.assertTrue(messages)

if __name__ == '__main__':
    unittest.main()