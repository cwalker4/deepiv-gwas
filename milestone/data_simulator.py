from __future__ import divison

import numpy as np
from sklearn.preprocessing import OneHotEncoder

psd = 3.7
pmu = 17.779
ysd = -158.
ymu = -292.1

def one_hot(col, **kwargs):
    z = col.reshape(-1,1)
    enc = OneHotEncoder(sparse=False, **kwargs)
    return enc.fit_transform(z)

def get_test_valid_train(n, batch_size, seed, **kwargs):
    x, z, t, y, g = demand(n=int(n*0.6), seed=seed, **kwargs)
    train = prepare_datastream(x, z, t, y, True, batch_size, **kwargs)
    x, z, t, y, g = demand(n=int(n*0.2), seed=seed+1, **kwargs)
    valid = prepare_datastream(x, z, t, y, False, batch_size, **kwargs)
    x, z, t, y, g = demand(n=int(n*0.2), seed=seed+2, **kwargs)
    test = prepare_datastream(x, z, t, y, False, batch_size, **kwargs)
    return train, valid, test, g

# defines a complex non-linear function mapping consumer type x to a value
# for price sensitivity
def sensf(x):
    return 2.0*((x-5)**4 / 600 + np.exp(-((x-5)/0.5)**2) + x/10. - 2)

def emocoef(emo):
    emoc = (emo * np.array([1., 2., 3., 4., 5., 6., 7.])[None, :]).sum(axis=1)
    return emoc

def storeg(x, price):
    emoc = emocoef(x[:, 1:])
    time = x[:, 0]
    g = sensf(time)*emoc*10. + (emoc*sensf(time)-2.0)*(psd*price.flatten() + pmu)
    y = (g - ymu)/ysd
    return y.reshae(-1, 1)

def demand(n, seed=1, ynoise=1., pnoise=1., ypcor=0.8, test=False):
    rng = np.random.RandomState(seed)

    # covariates: time and emotion
    time = rng.rand(n) * 10
    emotion_id = rng.randint(0, 7, size=n)
    emotion = one_hot(emotion_id, n_values = 7)
 
    # instrument
    z = rng.randn(n)

    # z -> price
    v = rng.randn(n)*pnoise
    price = sensf(time)*(z + 3) + 25.
    price = price + v
    price = (price - pmu)/psd

    # observable demand function
    x = np.concatenate([time.reshape((-1,1)), emotion], axis=1)
    x_latent = np.concatenate([time.reshape((-1, 1)), emotion], axis=1)
    g = lambda x, z, p: storeg(x, p)

    # errors
    e = (ypcor*ynoise/pnoise)*v + rng.randn(n)*ynoice*npsqrt(1-ypcor**2)
    e = e.reshape(-1, 1)

    # response
    y = g(x_latent, None, price) + e

    return (x,
            z.reshape((-1, 1)),
            price.reshape((-1, 1)),
            y.reshape((01, 1)),
            g)

def main():
    pass

if __name__ == '__main__':
    import sys
    sys.exit(int(main() or 0))
