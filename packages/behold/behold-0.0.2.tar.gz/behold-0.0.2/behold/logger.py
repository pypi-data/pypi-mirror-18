import functools
import inspect
import operator
import sys


class _Sentinal(object):
    pass


class Item(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Behold(object):
    # class variable to hold all context values
    _context = {}

    # operators to handle django-style querying
    _op_for = {
        '__lt': operator.lt,
        '__lte': operator.le,
        '__le': operator.le,
        '__gt': operator.gt,
        '__gte': operator.ge,
        '__ge': operator.ge,
        '__ne': operator.ne,
        '__in': lambda value, options: value in options
    }

    def __init__(self, tag=None, auto=True, stream=None):
        self.tag = tag
        self.auto = auto
        if stream is None:
            self.stream = sys.stdout
        else:
            self.stream = stream

        # these filters apply to context variables
        self.passes = True
        self.context_filters = []

        # a list of fields that will be printed if filters pass
        self.print_keys = []

        # holds a string rep for this object
        self._str = ''

    def _key_to_field_op(self, key):
        # this method looks at a key and checks if it ends in any of the
        # endings that have special django-like query meanings.
        # It translates those into comparision operators and returns the
        # name of the actual key.
        op = operator.eq
        name = key
        for op_name, trial_op in self.__class__._op_for.items():
            if key.endswith(op_name):
                op = trial_op
                name = key.split('__')[0]
                break
        return op, name

    @classmethod
    def set_context(cls, **kwargs):
        """
        This method sets context variables
        """
        cls._context.update(kwargs)

    @classmethod
    def unset_context(cls, *keys):
        """
        This method unsets the specified context variables
        """
        for key in keys:
            if key in cls._context:
                cls._context.pop(key)

    def reset(self):
        """
        resets filtering state
        """
        self.passes = False
        self.context_filters = []

    def when(self, *bools):
        self.passes = self.passes and all(bools)
        return self

    def excluding(self, *bools):
        self.passes = self.passes and not any(bools)
        return self

    def when_context(self, **criteria):
        self._add_context_filters(False, **criteria)
        return self

    def excluding_context(self, **criteria):
        self._add_context_filters(True, **criteria)
        return self

    def _add_context_filters(self, exclude, **criteria):
        for key, val in criteria.items():
            op, field = self._key_to_field_op(key)
            self.context_filters.append((op, field, val, exclude))

    def _passes_context_filter(self):
        if not self.context_filters:
            return True

        passes = False
        for (op, field, filter_val, exclude) in self.context_filters:
            context_val = self.__class__._context.get(field, _Sentinal())
            if not isinstance(context_val, _Sentinal):
                passes = exclude ^ op(context_val, filter_val)

        return passes

    def passes_all(self):
        return self.passes and self._passes_context_filter()

    def _separate_names_objects(self, values):
        att_names = []
        objs = []
        for val in values:
            if isinstance(val, str):
                att_names.append(val)
            else:
                objs.append(val)
        return att_names, objs

    def show(self, *values, **data):
        """
        If data is provided, then that will be used as source.  In this case
        if values are also provided, only those values are shown, otherwise all
        in key-sorted order.

        If data is not provided, *values are searched for non-string inputs.
        Any non-string input will be treated as the data source and only
        attributes listed in the string values will be extracted.  In this
        case if values are all strings with no non-string, then
        global() + locals() will be used as the data source.
        """

        if not self.passes_all():
            self.reset()
            return self.passes_all()

        att_names, objs = self._separate_names_objects(values)

        # at most one object is allowed
        if len(objs) > 1:
            raise ValueError(
                'Non key-word arguments to Behold().show() can only have '
                'one non-string value.'
            )

        # make sure kwargs and data not simultaneously specified
        elif data and len(objs) == 1:
            raise ValueError(
                'Error in Behold().show().  You specified both keyword '
                'arguments and a non-string argument. You can\'t do that.'
            )

        # handle case of no kwargs but non string in args
        elif not data and len(objs) == 1:
            item = objs[0]

        # handle case of kwargs only
        elif not objs and data:
            item = Item(**data)
            if not att_names:
                att_names = sorted(data.keys())

        # if no object specified, use locals() + globals()
        else:
            try:
                frame = inspect.currentframe().f_back

                # get globals
                att_dict = {}

                # get closures
                att_dict.update(frame.f_back.f_locals)

                # get locals
                att_dict.update(frame.f_locals)

                # make the item.  There's not a good way to test this
                # since testing classes always have a 'self'.  That's why
                # the pragma no cover.
                if 'self' in att_dict:  # pragma: no cover
                    del att_dict['self']
                item = Item(**att_dict)
            finally:
                del frame

        # set the string value
        self._str = self.stringify_item(item, att_names)
        if self.auto:
            self.stream.write(self._str + '\n')

        passes_all = self.passes_all()
        self.reset()
        return passes_all

    def stringify_item(self, item, att_names):
        if not att_names:
            raise ValueError(
                'Error in Behold.show().  Could not determine attributes/'
                'variables to show.')

        out = []
        for ind, key in enumerate(att_names):
            out.append(key + ': ')
            if ind < len(att_names) - 1 or self.tag:
                ending = ', '
            else:
                ending = ''

            val = self.extract(item, key)
            out.append(val + ending)
        if self.tag:
            out.append(self.tag)
        return ''.join(out)

    def extract(self, item, name):
        """
        Override this to perform any custom field extraction
        """
        val = ''
        if hasattr(item, name):
            val = getattr(item, name)
        return str(val)

    def __str__(self):
        return self._str

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return self.passes_all()


class in_context(object):
    _behold_class = Behold

    def __init__(self, **context_vars):
        self._context_vars = context_vars

    def __call__(self, f):
        @functools.wraps(f)
        def decorated(*args, **kwds):
            with self:
                return f(*args, **kwds)
        return decorated

    def __enter__(self):
        self.__class__._behold_class.set_context(**self._context_vars)

    def __exit__(self, *args, **kwargs):
        self.__class__._behold_class.unset_context(*self._context_vars.keys())


def set_context(**kwargs):
    Behold.set_context(**kwargs)


def unset_context(*keys):
    Behold.unset_context(*keys)
