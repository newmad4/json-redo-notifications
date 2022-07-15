
class EmptyMandatoryParameterError(ValueError):
    """Appear when system check is mandatory parameter present and is not null in data."""


class ProviderError(Exception):
    """Appear when system get error when try to send notification via external(or internal) providers."""
