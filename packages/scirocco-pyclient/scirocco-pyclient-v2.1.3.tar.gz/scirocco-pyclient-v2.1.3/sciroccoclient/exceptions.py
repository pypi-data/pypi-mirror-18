class SciroccoError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)


class SciroccoRequestAdapterError(SciroccoError):
    """ Raised when theres some problem at request low level. Probably the request manager aka urllib3 changed its behaviour
        or something else.
    """

    def __init__(self, message):
        super(SciroccoRequestAdapterError, self).__init__(message)


class SciroccoInitParamsError(SciroccoError):
    """
        Raised when theres a problem with initial parameters, token , server url .
    """

    def __init__(self):
        message = "You must init your connection to scirocco server with three positional arguments, host, node_id and auth_token."
        super(SciroccoInitParamsError, self).__init__(message)


class SciroccoHTTPDAOError(SciroccoError):
    """
        Raised when thers an unexpected result in DAO layer.
    """

    def __init__(self, message):
        message = ''.join(["HTTPDAO received an unexpected status code ", str(message)])

        super(SciroccoHTTPDAOError, self).__init__(message)


class SciroccoInvalidMessageScheduleTimeError(SciroccoError):
    def __init__(self):
        message = "The message schedule time param must be an datetime instance."
        super(SciroccoInvalidMessageScheduleTimeError, self).__init__(message)


class SciroccoInvalidMessageError(SciroccoError):
    def __init__(self):
        message = "The message param must be an instance of SciroccoMessage."
        super(SciroccoInvalidMessageError, self).__init__(message)


class SciroccoInvalidMessageDataError(SciroccoError):
    """
        Raised when try tu push and emtpy message.
    """

    def __init__(self):
        message = "The message data cannot be empty."
        super(SciroccoInvalidMessageDataError, self).__init__(message)


class SciroccoInvalidMessageDestinationError(SciroccoError):
    def __init__(self):
        message = "The message destination data cannot be empty."
        super(SciroccoInvalidMessageDestinationError, self).__init__(message)


class SciroccoInvalidMessageStatusError(SciroccoError):
    def __init__(self):
        message = "The message status must be 'pending' or 'scheduled' ."
        super(SciroccoInvalidMessageStatusError, self).__init__(message)


class SciroccoInvalidOnReceiveCallBackError(SciroccoError):
    """
    The callbackfunction provided by user its not valid
    """

    def __init__(self, message):
        super(SciroccoInvalidOnReceiveCallBackError, self).__init__(message)


class SciroccoInterruptOnReceiveCallbackError(SciroccoError):
    """
    Raised by user custom callback. Its intended to stop the consumer thread gracefully.
    """

    def __init__(self, message):
        super(SciroccoInterruptOnReceiveCallbackError, self).__init__(message)
