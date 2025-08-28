"""Custom exception hierarchy for media_puller.

This module defines exception classes that categorize errors into user
input issues, internal system failures, and third-party dependency
errors. All custom exceptions inherit from :class:`MediaPullerError` to
allow callers to catch a single base type if desired.
"""
from __future__ import annotations


class MediaPullerError(Exception):
    """Base class for all media_puller exceptions."""


class UserInputError(MediaPullerError, ValueError):
    """Raised when user input is invalid."""


class SystemOperationError(MediaPullerError, RuntimeError):
    """Raised when an internal system operation fails."""


class ThirdPartyError(MediaPullerError, RuntimeError):
    """Raised when a third-party dependency fails."""
