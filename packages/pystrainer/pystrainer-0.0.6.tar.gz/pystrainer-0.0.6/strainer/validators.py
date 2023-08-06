"""
Validators
==========

Validators are functions that validate data.

"""
import iso8601

from functools import partial, wraps
from .exceptions import ValidationException
from six import text_type


def export_validator(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        return partial(f, *args, **kwargs)

    return wrapper


def clamp_to_interval(value, bounds):
    min_bound, max_bound = bounds
    return min(max_bound, max(min_bound, value))


@export_validator
def integer(value, bounds=None, context=None):
    """converts a value to integer, applying optional bounds
    """
    try:
        value = int(value)
        if bounds:
            return clamp_to_interval(value, bounds)
        return value
    except (TypeError, ValueError):
        raise ValidationException('This field is not an integer')


@export_validator
def string(value, max_length=None, context=None):
    """converts a value into a string, optionally with a max length"""
    try:
        value = text_type(value)
    except (TypeError, ValueError):
        raise ValidationException('This field isn\'t a string')
    print "String validator value: %s max_length: %s" % (value, max_length)
    if max_length and len(value) > max_length:
        raise ValidationException('This field is to long, max length is %s' % (max_length))

    return value


@export_validator
def required(value, context=None):
    """validates that a field exists in the input"""
    if value is 0:
        return value

    if not value:
        raise ValidationException('This field is required')

    return value


@export_validator
def boolean(value, context=None):
    """Converts a field into a boolean"""
    try:
        return bool(value)
    except (TypeError, ValueError):
        raise ValidationException('This field is suppose to be boolean')


@export_validator
def datetime(value, default_tzinfo=iso8601.UTC, context=None):
    """validates that a a field is an ISO 8601 string, and converts it to a datetime object."""
    try:
        return iso8601.parse_date(value, default_timezone=default_tzinfo)
    except iso8601.ParseError as e:
        raise ValidationException('Invalid date: %s' % (e))
