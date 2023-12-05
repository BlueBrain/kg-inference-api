"""
Module: exceptions.py

This module defines a custom exception classes
"""


class ResourceNotFoundException(Exception):
    """Exception raised when a requested resource is not found.

    This exception is typically used to indicate that a resource, such as a file, database record,
    or network endpoint, is expected to exist but cannot be located.
    """
