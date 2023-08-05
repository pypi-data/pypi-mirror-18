from numpy import ones
from numpy import array
from numpy.random import RandomState
from numpy.testing import assert_almost_equal

from optimix import check_grad
from optimix import approx_fprime

from lim.mean import LinearMean


def test_value():
    random = RandomState(0)
    mean = LinearMean(5)
    effsizes = random.randn(5)
    mean.effsizes = effsizes

    x = random.randn(5)
    assert_almost_equal(mean.value(x), -0.956409566703)


def test_gradient():
    random = RandomState(1)
    mean = LinearMean(5)
    effsizes = random.randn(5)
    mean.effsizes = effsizes

    x = random.randn(5)

    def func(x0):
        mean.effsizes[0] = x0[0]
        return mean.value(x)

    def grad(x0):
        mean.effsizes[0] = x0[0]
        return [mean.derivative_effsizes(x)[0]]

    assert_almost_equal(check_grad(func, grad, [1.2]), 0, decimal=6)
