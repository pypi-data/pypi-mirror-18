from __future__ import absolute_import

from pandas_ply import symbolic
from pandas_ply.symbolic import X
from six.moves import reduce
from six import wraps

import pandas as pd
import numpy as np
import warnings


# Initialize the global X symbol
X(0)

class pipe(object):
    """Generic pipe decorator class that allows DataFrames to be passed
    through the `__rrshift__` binary operator, `>>`

    Adapted from:
    https://github.com/JulienPalard/Pipe/blob/master/pipe.py

    Where the two differences are the `>>` operator is used instead of the
    `|` operator, and DataFrame copying logic occurs in the operator
    overloader function.
    """

    __name__ = "pipe"


    def __init__(self, function):
        self.function = function


    def __rrshift__(self, other):
        other_copy = other.copy()
        other_copy._grouped_by = getattr(other, '_grouped_by', None)
        return self.function(other_copy)


    def __call__(self, *args, **kwargs):
        return pipe(lambda x: self.function(x, *args, **kwargs))



class group_delegation(object):
    """Decorator class that managing grouped operations on DataFrames.

    Checks for an attached `df._grouped_by` attribute added to a
    pandas DataFrame by the `groupby` function.

    If groups are found, the operation defined by the function is
    carried out for each group individually. The internal
    `_apply_combine_reset` function ensures that hierarchical
    indexing is removed.
    """

    __name__ = "group_delegation"

    def __init__(self, function):
        self.function = function


    def _apply_combine_reset(self, grouped, *args, **kwargs):
        combined = grouped.apply(self.function, *args, **kwargs)

        for name in combined.index.names[:-1]:
            if name in combined:
                combined.reset_index(level=0, drop=True, inplace=True)
            else:
                combined.reset_index(level=0, inplace=True)

        if (combined.index == 0).all():
            combined.reset_index(drop=True, inplace=True)

        return combined


    def __call__(self, *args, **kwargs):
        assert (len(args) > 0) and (isinstance(args[0], pd.DataFrame))

        df = args[0]
        grouped_by = getattr(df, "_grouped_by", None)

        if grouped_by is not None:
            df = df.groupby(grouped_by)

            try:
                assert self.function.function.__name__ == 'transmute'
                pass_args = grouped_by
            except:
                pass_args = args[1:]

            df = self._apply_combine_reset(df, *pass_args, **kwargs)
            if all([True if group in df.columns else False for group in grouped_by]):
                df._grouped_by = grouped_by
            else:
                warnings.warn('Grouping lost during transformation.')
            return df

        else:
            return self.function(*args, **kwargs)



class SymbolicHandler(object):

    __name__ = "SymbolicHandler"

    def __init__(self, function):
        super(SymbolicHandler, self).__init__()
        self.function = function

    def recursive_action(self, arg):
        if isinstance(arg, (list, tuple)):
            arglist = [self.recursive_action(subarg) for subarg in arg]
            return symbolic.sym_call(lambda *x: x, *arglist)
        else:
            return arg

    def recurse_args(self, args):
        return [self.recursive_action(arg) for arg in args]

    def recurse_kwargs(self, kwargs):
        return {k:self.recursive_action(v) for k,v in kwargs.items()}

    def call_wrapper(self, args, kwargs):
        return symbolic.Call(self.function, args=self.recurse_args(args),
                             kwargs=self.recurse_kwargs(kwargs))

    def __call__(self, *args, **kwargs):
        return self.call_wrapper(args, kwargs)



class make_symbolic(SymbolicHandler):

    __name__ = "make_symbolic"
    symbolic_arguments = False

    def __init__(self, function):
        super(make_symbolic, self).__init__(function)


    def recursive_action(self, arg):
        if isinstance(arg, (list, tuple)):
            arglist = [self.recursive_action(subarg) for subarg in arg]
            return symbolic.sym_call(lambda *x: x, *arglist)
        if isinstance(arg, symbolic.Expression):
            self.symbolic_arguments = True
        return arg


    def call_wrapper(self, args, kwargs):
        symbolic_function = symbolic.Call(self.function,
                                          args=self.recurse_args(args),
                                          kwargs=self.recurse_kwargs(kwargs))
        if not self.symbolic_arguments:
            return symbolic.eval_if_symbolic(symbolic_function, {})
        else:
            self.symbolic_arguments = False
            return symbolic_function



class symbolic_evaluation(SymbolicHandler):

    __name__ = "symbolic_evaluation"

    def __init__(self, function):
        super(symbolic_evaluation, self).__init__(function)


    def call_wrapper(self, args, kwargs):
        symbolic_function = symbolic.Call(self.function,
                                          args=self.recurse_args(args),
                                          kwargs=self.recurse_kwargs(kwargs))
        return symbolic.to_callable(symbolic_function)(args[0])



class symbolic_reference(SymbolicHandler):

    __name__ = "symbolic_reference"

    def __init__(self, function):
        super(symbolic_reference, self).__init__(function)


    def recursive_action(self, arg):
        if hasattr(arg, '_eval'):
            arg = symbolic.to_callable(arg)(self.df)
        if isinstance(arg, pd.Series):
            return arg.name
        elif isinstance(arg, pd.DataFrame):
            return symbolic.sym_call(lambda *x: x, arg.columns.tolist())
        elif isinstance(arg, (list, tuple)):
            arglist = [self.recursive_action(subarg) for subarg in arg]
            return symbolic.sym_call(lambda *x: x, *arglist)
        return arg


    def call_wrapper(self, args, kwargs):
        self.df = args[0]
        symbolic_function = symbolic.Call(self.function,
                                          args=[self.df]+self.recurse_args(args[1:]),
                                          kwargs=self.recurse_kwargs(kwargs))
        return symbolic.to_callable(symbolic_function)(self.df)



def _arg_extractor(args):
    """Extracts arguments from lists or tuples and returns them
    "flattened" (extracting lists within lists to a flat list).

    Args:
        args: can be any argument.

    Returns:
        list
    """
    flat = []
    for arg in args:
        if isinstance(arg, (list, tuple, pd.Index)):
            flat.extend(_arg_extractor(arg))
        else:
            flat.append(arg)
    return flat


def flatten_arguments(f):
    """Decorator that "flattens" any arguments contained inside of lists or
    tuples. Designed primarily for selection and dropping functions.

    Example:
        args = (a, b, (c, d, [e, f, g]))
        becomes
        args = (a, b, c, d, e, f, g)

    Args:
        f (function): function for which the arguments should be flattened.

    Returns:
        decorated function
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        assert len(args) > 0 and isinstance(args[0], pd.DataFrame)
        if len(args) > 1:
            flat_args = [args[0]]+_arg_extractor(args[1:])
            return f(*flat_args, **kwargs)
        else:
            return f(*args, **kwargs)
    return wrapped


def join_index_arguments(f):
    """Decorator for joining indexing arguments together. Designed primarily for
    `row_slice` to combine arbitrary single indices and lists of indices
    together.

    Example:
        args = (1, 2, 3, [4, 5], [6, 7])
        becomes
        args = ([1, 2, 3, 4, 5, 6, 7])

    Args:
        f (function): function to be decorated.

    Returns:
        decorated function
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        assert (len(args) > 0) and (isinstance(args[0], pd.DataFrame))
        if len(args) > 1:
            args_ = reduce(lambda x, y: np.concatenate([np.atleast_1d(x), np.atleast_1d(y)]),
                           args[1:])
            args = [args[0]] + [np.atleast_1d(args_)]
        return f(*args, **kwargs)
    return wrapped



def _col_ind_to_position(columns, indexer):
    """Converts column indexers to their integer position.

    Args:
        columns (list): list of column names.
        indexer (str or int): either a column name or an integer position of the
            column.

    Returns:
        Integer column position.
    """
    if isinstance(indexer, str):
        if indexer not in columns:
            raise Exception("String label "+str(indexer)+' is not in columns.')
        return columns.index(indexer)
    elif isinstance(indexer, int):
        #if indexer < 0:
        #    raise Exception("Int label "+str(indexer)+' is negative. Not currently allowed.')
        return indexer
    else:
        raise Exception("Column indexer not of type str or int.")



def _col_ind_to_label(columns, indexer):
    """Converts column indexers positions to their string label.

    Args:
        columns (list): list of column names.
        indexer (int or str): either a column name or an integer position of
            the column.

    Returns:
        String column name.
    """
    if isinstance(indexer, str):
        return indexer
    elif isinstance(indexer, int):
        warnings.warn('Int labels will be inferred as column positions.')
        if indexer < -1*len(columns):
            raise Exception(str(indexer)+' is negative and less than length of columns.')
        elif indexer >= len(columns):
            raise Exception(str(indexer)+' is greater than length of columns.')
        else:
            return list(columns)[indexer]
    else:
        raise Exception("Label not of type str or int.")


def column_indices_as_labels(f):
    """Decorator that convertes column indicies to label. Typically decoration
    occurs after decoration by `symbolic_reference`.

    Args:
        f (function): function to be decorated.

    Returns:
        Decorated function with any column indexers converted to their string
        labels.
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        assert (len(args) > 0) and (isinstance(args[0], pd.DataFrame))
        if len(args) > 1:
            label_args = [_col_ind_to_label(args[0].columns.tolist(), arg)
                          for arg in args[1:]]
            args = [args[0]]+label_args
        return f(*args, **kwargs)
    return wrapped


def column_indices_as_positions(f):
    """Decorator that converts column indices to integer position. Typically
    decoration occurs after decoration by `symbolic_reference`.

    Args:
        f (function): function to be decorated.

    Returns:
        Decorated function with any column indexers converted to their integer
        positions.
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        assert (len(args) > 0) and (isinstance(args[0], pd.DataFrame))
        if len(args) > 1:
            label_args = [_col_ind_to_position(args[0].columns.tolist(), arg)
                          for arg in args[1:]]
            args = [args[0]]+label_args
        return f(*args, **kwargs)
    return wrapped



def label_selection(f):
    """Convenience chain of decorators for functions that operate with the
    expectation of having column labels as arguments (despite user potentially
    providing symbolic `pandas.Series` objects or integer column positions).

    Args:
        f (function): function to be decorated.

    Returns:
        Decorated function with any column indexers converted to their string
        labels and arguments flattened.
    """
    return pipe(
        symbolic_reference(
            flatten_arguments(
                column_indices_as_labels(f)
            )
        )
    )


def positional_selection(f):
    """Convenience chain of decorators for functions that operate with the
    expectation of having column integer positions as arguments (despite
    user potentially providing symbolic `pandas.Series` objects or column labels).

    Args:
        f (function): function to be decorated.

    Returns:
        Decorated function with any column indexers converted to their integer
        positions and arguments flattened.
    """
    return pipe(
        symbolic_reference(
            flatten_arguments(
                column_indices_as_positions(f)
            )
        )
    )



def dfpipe(f):
    """Standard chain of decorators for a function to be used with dfply.
    The function can be chained with >> by `pipe`, application of the function
    to grouped DataFrames is enabled by `group_delegation`, and symbolic
    arguments are evaluated as-is using a default `symbolic_evaluation`.

    Args:
        f (function): function to be decorated.

    Returns:
        Decorated function chaining the `pipe`, `group_delegation`, and
        `symbolic_evaluation` decorators.
    """
    return pipe(
        group_delegation(
            symbolic_evaluation(f)
        )
    )
