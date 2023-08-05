from numpy import sqrt
from numpy import std
from ..link import LogitLink
from ..link import LogLink
from ..lik import BernoulliLik
from ..lik import BernoulliProdLik
from ..lik import BinomialProdLik
from ..lik import PoissonProdLik
from ..mean import OffsetMean
from ..mean import LinearMean
from ..mean import SumMean
from ..cov import LinearCov
from ..cov import SumCov
from ..cov import EyeCov
from .glmm import GLMMSampler
from ..util.fruits import Apples
from ..tool.normalize import stdnorm


def bernoulli(offset, G, heritability=0.5, random_state=None):

    nsamples = G.shape[0]
    G = stdnorm(G, axis=0)
    G /= sqrt(G.shape[1])

    link = LogitLink()

    mean = OffsetMean()
    mean.offset = offset

    cov = LinearCov()

    mean.set_data(nsamples, 'sample')
    cov.set_data((G, G), 'sample')

    r = heritability / (1 - heritability)
    cov.scale = BernoulliLik.latent_variance(link) * r

    lik = BernoulliProdLik(None, link)
    sampler = GLMMSampler(lik, mean, cov)

    return sampler.sample(random_state)


def binomial(ntrials,
             offset,
             G,
             heritability=0.5,
             causal_variants=None,
             causal_variance=0,
             random_state=None):

    nsamples = G.shape[0]
    G = stdnorm(G, axis=0)
    G /= sqrt(G.shape[1])

    link = LogitLink()

    mean1 = OffsetMean()
    mean1.offset = offset

    cov1 = LinearCov()
    cov2 = EyeCov()
    cov = SumCov([cov1, cov2])

    mean1.set_data(nsamples, 'sample')
    cov1.set_data((G, G), 'sample')
    a = Apples(nsamples)
    cov2.set_data((a, a), 'sample')

    cov1.scale = heritability - causal_variance
    cov2.scale = 1 - heritability - causal_variance

    means = [mean1]
    if causal_variants is not None:
        means += [_causal_mean(causal_variants, causal_variance, random_state)]

    mean = SumMean(means)

    lik = BinomialProdLik(None, ntrials, link)
    sampler = GLMMSampler(lik, mean, cov)

    return sampler.sample(random_state)


def poisson(offset, G, heritability=0.5, random_state=None):

    nsamples = G.shape[0]
    G = stdnorm(G, axis=0)
    G /= sqrt(G.shape[1])

    link = LogLink()

    mean = OffsetMean()
    mean.offset = offset

    cov1 = LinearCov()
    cov2 = EyeCov()
    cov = SumCov([cov1, cov2])

    mean.set_data(nsamples, 'sample')
    cov1.set_data((G, G), 'sample')
    a = Apples(nsamples)
    cov2.set_data((a, a), 'sample')

    cov1.scale = heritability
    cov2.scale = 1 - heritability

    lik = PoissonProdLik(None, link)
    sampler = GLMMSampler(lik, mean, cov)

    return sampler.sample(random_state)


def _causal_mean(causal_variants, causal_variance, random):
    causal_variants = stdnorm(causal_variants, axis=0)
    causal_variants /= sqrt(causal_variants.shape[1])
    p = causal_variants.shape[1]
    directions = random.randn(p)
    directions[directions < 0.5] = -1
    directions[directions >= 0.5] = +1
    s = std(directions)
    if s > 0:
        directions /= s
    directions *= sqrt(causal_variance)
    directions -= directions.mean()
    mean = LinearMean(p)
    mean.set_data((causal_variants, ), 'sample')
    mean.effsizes = directions
    return mean
