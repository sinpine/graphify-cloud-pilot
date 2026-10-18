"""Errors cross validation, persistence, service and transport boundaries."""


class InputError(ValueError):
    pass


class StorageError(RuntimeError):
    pass


class ConflictError(StorageError):
    pass


class ServiceError(RuntimeError):
    pass
