import numpy as np
from sklearn.preprocessing import OneHotEncoder
import pdb 

psd = 3.7
pmu = 17.779
ysd = 158.
ymu = -292.1

def monte_carlo_error(g_hat, data_fn, ntest=5000):
    pdb.set_trace()
    seed = np.random.randint(1e9)
    x, z, p, y, g_true = demand(ntest, seed, test=True)

    p = np.linspace(np.percentile(p, 2.5), np.percentile(p, 97.5), ntest).reshape(-1,1)
    y = g_true(x, z, p)
    y_true = y.flatten()
    y_hat = g_hat(x, z, p).flatten()
    return ((y_hat - y_true)**2).mean()

def one_hot(col, **kwargs):
    '''
    Transforms labels vector to one-hot encoding

    Arguments:
    col -- python numpy array of shape (n, 1) representing classes of customer

    Returns:
    z -- one-hot encoding of col with shape (n, num_classes)
    '''
    z = col.reshape(-1,1)
    enc = OneHotEncoder(sparse=False, **kwargs)
    return enc.fit_transform(z)

def get_test_valid_train(n, batch_size, seed, **kwargs):
    '''
    Generates train, validate, and test data simulations with IV model

    Arguments:
    n -- number of observations to generate
    batch_size -- size of batches
    seed -- random seed

    Returns:
    x, z, t, y, g for train, validate, and test sets
    '''
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
    '''
    Calculates price sensitivity via a complex non-linear function of time

    Arguments:
    x -- numpy array of shape (n,) representing time classes

    Returns:
    sensf -- numpy array of shape (n,) representing price sensitivity
    '''
    return 2.0*((x-5)**4 / 600 + np.exp(-((x-5)/0.5)**2) + x/10. - 2)

def emocoef(emo):
    '''
    Converts one-hot encoding of consumer labels back to label encoding

    Arguments:
    emo -- numpy array of shape (n,7) representing one-hot encoding

    Returns:
    emoc -- numpy array of shape (n,1) representing consumer labels
    '''
    emoc = (emo * np.array([1., 2., 3., 4., 5., 6., 7.])[None, :]).sum(axis=1)
    return emoc

def storeg(x, p):
    '''
    Calculates sales numbers as a noisy function of price and consumer type

    Arguments:
    x -- numpy array of shape (n,8) with time and consumer type covariates
    price -- response vector of shape (n,) with prices

    Returns:
    y -- numpy array of shape (n,1) giving normalized response (sales)
    '''
    emoc = emocoef(x[:, 1:])
    time = x[:, 0]

    # corresponds to eqn for y in Hartford et al., with steps added to 
    # un-normalize price
    pdb.set_trace()
    g = sensf(time)*emoc*10. + (emoc*sensf(time)-2.0)*(psd*p.flatten() + pmu)
    y = (g - ymu)/ysd
    return y.reshape(-1, 1)

def demand(n, seed=1, ynoise=1., pnoise=1., ypcor=0.8, test=False):
    '''
    Generates full simulated demand data via process described in deepiv_proposal

    Arguments:
    n -- number of observations
    seed -- random seed
    ynoise -- noise on sales
    pnoise -- noise on price
    ypcor -- amount of endogeneity

    Returns:
    x -- simulated covariates
    z -- instrument
    price -- observed prices
    y -- observed sales
    g -- sales generating function
    '''
    rng = np.random.RandomState(seed)

    # covariates: time and emotion (emotion = customer type)
    time = rng.rand(n) * 10
    emotion_id = rng.randint(0, 7, size=n)
    emotion = one_hot(emotion_id, n_values = 7)
 
    # instrument
    z = rng.randn(n)

    # z -> price
    # calculate price -> add noise (v) -> normalize
    v = rng.randn(n)*pnoise
    price = sensf(time)*(z + 3) + 25.
    price = price + v
    price = (price - pmu)/psd

    # observable demand function (hotels observe average price sensitivity and
    # the time of the year
    x = np.concatenate([time.reshape((-1,1)), emotion], axis=1)
    g = lambda x, z, p: storeg(x, p)

    # errors
    e = (ypcor*ynoise/pnoise)*v + rng.randn(n)*ynoise*np.sqrt(1-ypcor**2)
    e = e.reshape(-1, 1)

    # response
    y = g(x, None, price) + e

    return (x,
            z.reshape((-1, 1)),
            price.reshape((-1, 1)),
            y.reshape((-1, 1)),
            g)

def main():
    pass

if __name__ == '__main__':
    import sys
    sys.exit(int(main() or 0))
