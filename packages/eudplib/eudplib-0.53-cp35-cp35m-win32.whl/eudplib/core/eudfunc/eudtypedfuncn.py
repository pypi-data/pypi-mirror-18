from ... import utils as ut
from .. import variable as ev

from .eudfuncn import EUDFuncN


def applyTypes(typesdecl, varlist):
    """
    EUD-Typecast each variable to declared types.

    :param typesdecl: List of types. Can be set to None if you don't want
        to typecast anything. Each item of the list can also be None which is
        equivilant to EUDVariable here.
    :param varlist: List of variables.

    :returns: List of casted variables.
    """
    if typesdecl is None:
        return varlist

    ut.ep_assert(len(varlist) == len(typesdecl))

    rets = []
    for vartype, var in zip(typesdecl, varlist):
        if vartype == ev.EUDVariable or vartype is None:
            rets.append(var)
        else:
            rets.append(vartype(var))

    return rets


class EUDTypedFuncN(EUDFuncN):

    """
    EUDFuncN specialization for EUDTypedFunc. This will pre-convert
    arguments to types prior to function call.
    """

    def __init__(self, argn, callerfunc, bodyfunc, argtypes, rettypes):
        super().__init__(argn, callerfunc, bodyfunc)
        self._argtypes = argtypes
        self._rettypes = rettypes

    def __call__(self, *args):
        # This layer is nessecary for function to accept non-EUDVariable object
        # as argument. For instance, EUDFuncN.
        args = applyTypes(self._argtypes, args)
        rets = super().__call__(*args)

        # Cast returns to rettypes before caller code.
        rets = applyTypes(self._rettypes, rets)
        return rets
