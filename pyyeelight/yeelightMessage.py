class YeelightMessage:
    """
        Generic class for all type of messages sent and received from a Yeelight Bulb
    """
    MESSAGE_TYPE_COMMAND = "command"
    MESSAGE_TYPE_RESPONSE = "response"
    MESSAGE_TYPE_NOTIFICATION = "notification"

    COMMAND_BODY = '{{"id":{},"method":"{}","params":[{}]}}\r\n'

    RESPONSE_ID = "id"
    RESPONSE_RESULT = "result"
    RESPONSE_ERROR = "error"

    ERROR_MESSAGE = "message"
    ERROR_CODE = "code"

    def __init__(self):
        """
        The generic class has no type
        """
        self.type = None

    def get_type(self):
        return self.type


class YeelightCommand(YeelightMessage):
    """
        Class used to handle command message sent to a bulb
    """

    def __init__(self, unique_id, method, params=None):
        """
            For some methods (stop_cf, toggle ...), params are not necessary (see API doc)

            :param unique_id: id to make the command unique
            :param method: method name (see API doc)
            :param params: parameters used with the method (see API doc)

            :type unique_id : int
            :type method : str
            :type params : list
        """
        super().__init__()
        self.type = self.MESSAGE_TYPE_COMMAND
        self.method = method
        self.params = params
        self.command_id = unique_id
        self.message = None
        self.build_message()

    def build_message(self):
        """
            Make the one string message sent to the bulb
        """
        if self.params is None:
            inline_params = ""
        else:
            # Put all params in one string
            inline_params = ""
            if type(self.params) is list:
                for x in self.params:
                    if x != self.params[0]:
                        inline_params += ", "
                    if type(x) is int:
                        inline_params += str(x)
                    else:
                        inline_params += '"{}"'.format(x)
            else:
                inline_params += '"{}"'.format(self.params)

        # Build message with that string
        self.message = self.COMMAND_BODY.format(str(self.command_id), self.method, inline_params)

    def get_message(self):
        """
            Return the one string message
            :rtype: str
        """
        return self.message

    def get_command_id(self):
        """
            Get the unique id
            :rtype: int
        """
        return self.command_id

    def __str__(self):
        """
            Verbose description of the command
            :rtype: str
        """
        return 'Command : "{}"\nParameters : "{}"\nId : {}'.format(self.method, self.params, self.command_id)


class YeelightResponse(YeelightMessage):
    """
        Class used to handle a response from the bulb to a command message
    """

    def __init__(self, raw_response, command):
        """
            Initiate the response
            :param raw_response: Not decoded one string response
            :param command : command used to generate the bulb response
            :type raw_response: str
            :type command: YeelightCommand
        """
        super().__init__()
        self.type = self.MESSAGE_TYPE_RESPONSE
        self.command = command
        self.response_id = None
        self.result = None
        self.decode_response(raw_response)

    def decode_response(self, raw_response):
        """
            Put in self.result the data from the response
            Can generate exception if the command and the response id does not match
            of if the response is an error
            :param raw_response:  Not decoded one string response
        """
        # Transform response into a dict
        import json
        data = json.loads(raw_response)
        # Retrieve the response id
        self.response_id = data[self.RESPONSE_ID]
        # Check if the response id match the command id
        self.check_id()
        # Get response data
        if self.RESPONSE_RESULT in data:
            self.result = data[self.RESPONSE_RESULT]
        elif self.RESPONSE_ERROR in data:
            # If the response is an error raise YeelightError Exception
            message = data[self.RESPONSE_ERROR][self.ERROR_MESSAGE]
            code = data[self.RESPONSE_ERROR][self.ERROR_CODE]
            raise YeelightError(message, code, self.command)

    def check_id(self):
        """
            Raise an exception if the command and the response id does not match
        """
        if self.response_id != self.command.get_command_id():
            raise Exception(
                "Error decoding response : the response id {} doesn't match the command id {}".format(self.response_id,
                                                                                                      self.command.get_command_id()))


class YeelightNotification(YeelightMessage):
    """
        Class used to handle notification message generate from the bulb
    """

    def __init__(self, ):
        super().__init__()
        self.type = self.MESSAGE_TYPE_NOTIFICATION


class YeelightError(Exception):
    """
        Exception for error message response from the bulb
    """

    def __init__(self, error_message, error_code, command):
        """
            This exception is mainly use to correctly generate the error message is the stack trace
            :param error_message: error message from the bulb
            :param error_code: error code generate by the bulb
            :param command: command that generate this response
            :type error_message: str
            :type error_code: int
            :type command: YeelightCommand
        """
        message = "Sent to the Yeelight Bulb :\n{}\n".format(command.__str__())
        message += "The Yeelight bulb returns the following error : {} (Code {})\n".format(error_message, error_code)
        Exception.__init__(self, message)
