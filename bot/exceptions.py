class BaseConfigException(Exception):
    pass


class BotTokenNotFoundException(BaseConfigException):
    def __init__(self, message='BOT_TOKEN не определён'):
        super().__init__(message)


class OpenaiApiKeyNotFoundException(BaseConfigException):
    def __init__(self, message='OPENAI_API_KEY не определён'):
        super().__init__(message)
