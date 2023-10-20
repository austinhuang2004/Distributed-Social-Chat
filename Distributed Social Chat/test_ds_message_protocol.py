# Austin Huang
# austh10@uci.edu
# 28821105

import unittest
import ds_protocol

class TestDirectMessage(unittest.TestCase):
    def test_directmessage(self):
        message = 'testing message'
        recipient = 'Austin test'
        user_token = 'test token'
        answer = ds_protocol.direct_message(user_token, message, recipient)
        self.assertTrue(answer)
        print(answer)

if __name__ == '__main__':
    unittest.main()
