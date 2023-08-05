from __future__ import division

from numpy.random import RandomState
from numpy.testing import assert_almost_equal
from numpy import sqrt
from numpy import ones

from limix_math.linalg import qs_decomposition

from lim.inference import FastLMM
from lim.inference import SlowLMM
from lim.util.fruits import Apples
from lim.cov import LinearCov
from lim.cov import EyeCov
from lim.cov import SumCov
from lim.mean import OffsetMean
from lim.random import RegGPSampler
from lim.genetics import DesignMatrixTrans


def test_optimization():
    random = RandomState(9458)
    N = 50
    X = random.randn(N, 75)
    X -= X.mean(0)
    X /= X.std(0)
    X /= sqrt(X.shape[1])
    offset = 1.2

    mean = OffsetMean()
    mean.offset = offset
    mean.set_data(N)
    mean.set_data(N, purpose='sample')

    cov_left = LinearCov()
    cov_left.scale = 1.5
    cov_left.set_data((X, X))
    cov_left.set_data((X, X), purpose='sample')

    cov_right = EyeCov()
    cov_right.scale = 1.5
    cov_right.set_data((Apples(N), Apples(N)))
    cov_right.set_data((Apples(N), Apples(N)), purpose='sample')

    cov = SumCov([cov_left, cov_right])

    y = RegGPSampler(mean, cov).sample(random)

    slmm = SlowLMM(y, mean, cov)
    slmm.learn()
    delta = cov_right.scale / (cov_left.scale + cov_right.scale)
    QS = qs_decomposition(DesignMatrixTrans(X).transform(X))
    flmm = FastLMM(y, ones((N, 1)), QS[0][0], QS[0][1], QS[1][0])
    flmm.delta = delta
    assert_almost_equal(slmm.lml(), flmm.lml())
    assert_almost_equal(mean.offset, flmm.beta[0], decimal=6)
