# Starter code for assignment 3 in ICS 32 Programming

# Replace the following placeholders with your information.

# Austin Huang
# austh10@uci.edu
# 28821105
'''
This module is used to send messages, retrieve new anda ll messages
'''
import socket
import ds_protocol


class DirectMessage:
    '''
    Class that includes recipient, message, and timestamp.
    '''
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    '''
    Class that connects to DSU server, sends messages, and retrieves messages
    '''
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.messages = []
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
            srv.connect((self.dsuserver, 3021))
            joining_message = ds_protocol.join(self.username, self.password)
            srv.sendall((joining_message + "\n").encode('utf-8'))
            response = srv.recv(4096)
            json_resp = ds_protocol.response_process(response)
            print('The response:', json_resp)
            self.token = ds_protocol.getting_token(json_resp)

    def send(self, recipient: str, message: str) -> bool:
        '''
        The send function joins a ds server and sends a message, bio, or both

        :param server: The ip address for the ICS 32 DS server.
        :param port: The port where the ICS 32 DS server is accept connection.
        :param username: The user name to be assigned to the message.
        :param password: The password associated with the username.
        :param message: The message to be sent to the server.
        :param bio: Optional, a bio for the user.
        '''
        if self.token is None:
            print('Error: no token')
            return False
        direct_message_json = ds_protocol.direct_message(self.token, message, recipient)

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, 3021))
                client.sendall((direct_message_json + "\n").encode('utf-8'))
                response = client.recv(4096)
                json_resp = ds_protocol.response_process(response)
                return bool(json_resp['response']['type'] == 'ok')
        except (socket.gaierror, ConnectionRefusedError, TimeoutError, ConnectionResetError, OSError) as problem:
            print(f'Error when trying to connect to ther server: {problem}')
            return False

    def retrieve_new(self) -> list:
        '''
        This function is used to retrieve new messages
        '''
        if self.token is None:
            print('Error: no token')
            return []

        unread_directmessages = ds_protocol.requesting_directmessage(self.token, 'new')

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, 3021))
                client.sendall((unread_directmessages + "\n").encode('utf-8'))
                response = client.recv(4096).decode('utf-8')
                json_resp = ds_protocol.response_process(response)
                messages = []
                for message in json_resp['messages']:
                    get_directmessage = DirectMessage()
                    get_directmessage = message['to']
                    get_directmessage = message['message']
                    get_directmessage = message['timestamp']
                    messages.append(get_directmessage)
                return messages
        except (socket.gaierror, ConnectionRefusedError, TimeoutError, ConnectionResetError, OSError) as problem:
            print(f'Error when trying to connect to ther server: {problem}')
            return False

    def retrieve_all(self) -> list:
        '''
        This function is used to retrieve all messages
        '''
        if self.token is None:
            print('Error: no token')
            return []

        all_directmessages = ds_protocol.requesting_directmessage(self.token, 'all')

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, 3021))
                client.sendall((all_directmessages + "\n").encode('utf-8'))
                response = client.recv(4096)
                json_resp = ds_protocol.response_process(response)
            return self.analyze_messages(json_resp)
        except (socket.gaierror, ConnectionRefusedError, TimeoutError, ConnectionResetError, OSError) as problem:
            print(f'Error when trying to connect to ther server: {problem}')
            return False

    def analyze_messages(self, json_resp):
        '''
        Function used to return messages
        '''
        directmessages = []
        for the_message in json_resp['direct_messages']:
            get_message = DirectMessage()
            get_message.recipient = the_message['recipient']
            get_message.message = the_message['message']
            get_message.timestamp = the_message['timstamp']
            directmessages.append(get_message)
