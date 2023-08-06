from collections import defaultdict
import inspect

def overloaded_impl_name(name, n_args):
    return '__overloaded_{}_{}'.format(name, n_args)

class Meta(type):

    curr_overloads = defaultdict(lambda: [])

    def __new__(cls, name, parents, attrs):
        cls.do_overload(cls, attrs)
        return super(Meta, cls).__new__(cls, name, parents, attrs)

    @staticmethod
    def do_overload(cls, attrs):
        overloads = cls.curr_overloads
        cls.curr_overloads = defaultdict(lambda: [])
        for name, funcs in overloads.items():
            for func in funcs:
                func = cls.rename_func(func)
                attrs[func.__name__] = func
            def dispatch(self, *args, **kwds):
                n_args = len(args) + len(kwds) + 1
                impl_name = overloaded_impl_name(name, n_args)
                f = getattr(self.__class__, impl_name, None)
                if not f:
                    raise ValueError(
                        'No overloaded {} with {} arguments'.format(
                            name, n_args)
                    )
                return f(self, *args, **kwds)
            attrs[name] = dispatch

    @staticmethod
    def rename_func(f):
        n_args = len(inspect.getargspec(f).args)
        f.__name__ = '__overloaded_{}_{}'.format(f.__name__, n_args)
        return f

# currently only support:
#     1. method overloading of different number of arguments
# future plan:
#     1. function overloading
#     2. overloading with different types of arguments
def overload(f):
    '''
    constraints:
        1. place all global overloaded functions after class definitions
           (if the class contains overloadings)
        2. method overloading require the class to subclass Object
           (mutiple inherintance is fine)
    '''
    Meta.curr_overloads[f.__name__].append(f)
    return f

class Object(object):

    __metaclass__ = Meta
