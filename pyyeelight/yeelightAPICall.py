import socket
import uuid
from .yeelightMessage import YeelightCommand, YeelightResponse


class YeelightAPICall:
    """
        Class used to send and receive thought sockets command and response messages
    """

    DEFAULT_PORT = 55443

    def __init__(self, ip, port=DEFAULT_PORT):
        """
            Build the API Call

            :param ip: ip of the bulb you want to manipulate
            :param port: port used to send and receive messages (should be the default port)

        """
        self.ip = ip
        self.port = port
        self.command_id = 0
        self.command = None
        self.response = None

    def get_response(self):
        return self.response.result

    def get_command(self):
        return self.command

    def next_cmd_id(self):
        """
            Each command should be run with an unique id, uuid generate this id
            This id is converted to an 16 bit int that can be sent to the bulb
            Test with 32 and 64bits length int failed
            :return: Unique id
            :rtype: int
        """
        self.command_id = uuid.uuid4().int & (1 << 16) - 1
        return self.command_id

    def operate_on_bulb(self, method, params=None):
        """
            Build socket and send command to the bulb through it

            :param method: method you want to use
            :param params: parameters needed for this method (can be a string if ony one parameter is needed)

            :type method: str
            :type params: list of str
        """
        # Get the message
        self.command = YeelightCommand(self.next_cmd_id(), method, params)
        # Send with socket
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((self.ip, int(self.port)))
        tcp_socket.send(self.command.get_message().encode())
        data = tcp_socket.recv(4096)
        tcp_socket.close()
        # Process the response
        self.response = YeelightResponse(data.decode(), self.command)
