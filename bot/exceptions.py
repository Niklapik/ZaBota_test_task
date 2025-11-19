class BaseConfigException(Exception):
    """Базовое исключение для настроек конфигурации бота."""
    pass


class BotTokenNotFoundException(BaseConfigException):
    """Исключение при отсутствии токена бота."""

    def __init__(self, message='BOT_TOKEN не определён'):
        super().__init__(message)


class OpenaiApiKeyNotFoundException(BaseConfigException):
    """Исключение при отсутствии токена OPENAI."""

    def __init__(self, message='OPENAI_API_KEY не определён'):
        super().__init__(message)
