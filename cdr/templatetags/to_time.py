from django.template import Library
import datetime


register = Library()


@register.filter
def to_time(s):
    """
    Return time object from integer seconds.
    :param s: seconds as integer
    :return: time object
    """
    return datetime.datetime.utcfromtimestamp(s).time()
