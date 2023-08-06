# Copyright (C) 2016 Allen Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Data constructors for Python.

Classes:
Constructor -- Data constructor metaclass
"""

import abc


class Constructor(abc.ABCMeta):

    """Metaclass for Haskell-like data constructors.

    Classes must define an arity class attribute.

    Example:

        class SomeType: pass
        class SomeValue(SomeType, metaclass=Constructor):
            arity = 1

    Very roughly speaking, equivalent to Haskell's:

        data SomeType a = SomeValue a

    Python does not support generics or type constructors, so you cannot do
    ``SomeType str`` or ``SomeType int`` as in Haskell.

    Values should be unpacked by assignment to distinguish data constructor
    instances from regular tuples:

        value, = SomeValue(value)
    """

    def __new__(meta, name, bases, dct):
        arity = int(dct.pop('arity'))
        dict_method = _dict_method_adder(dct)

        @dict_method
        def __new__(cls, *values):
            if len(values) != arity:
                raise TypeError('__new__() takes %d arguments' % (arity,))
            return tuple.__new__(cls, values)

        @dict_method
        def __eq__(self, other):
            return (isinstance(other, type(self))
                    and super(type(self), self).__eq__(other))

        @dict_method
        def __ne__(self, other):
            return not self == other

        bases += (tuple,)
        return super(Constructor, meta).__new__(meta, name, bases, dct)


def _dict_method_adder(dct):
    """Decorator for adding methods to a dict."""
    def decorator(f):
        dct[f.__name__] = f
        return f
    return decorator
