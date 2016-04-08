from django.core.cache import cache
from django.http import Http404
from django.contrib.auth.models import Group

class staff_required(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return self.func(request, *args, **kwargs)


class group_required(object):
    def __init__(self, group_name):
        self.group_name = group_name

    def __call__(self, func):
        def wrapper(request, *args, **kwargs):
            group = Group.objects.get(name=self.group_name)
            if not group in request.user.groups.all():
                raise Http404
            return func(request, *args, **kwargs)
        return wrapper


def _make_key(base, args):
        return base + "".join(map(str, args))

# Decorator to cache the result of a function
# Return value must be json serializable
# Cached key is a combination of the function name and the string value of all the args (not kwargs)
class cached_function(object):
    def __init__(self, time):
        self.time = time

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            key = _make_key(func.__name__, args)
            cached_result = cache.get(key)
            if cached_result:
                return cached_result
            res = func(*args, **kwargs)
            cache.set(key, res, self.time)
            return res
        return wrapper
