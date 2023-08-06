import math
import autograd.numpy as np
from rlstm.common_util import safe_log
from rlstm.emission_models import bernoulli_multivariate, diagonal_gaussian_multivariate


def sigmoid(x):
    return 0.5 * (np.tanh(x) + 1)


def rbf(x):
    return np.exp(-x**2)


def relu(x):
    return np.maximum(x, 0.0)


def logit(p):
    return np.log(p / (1 - p))


def softmax(x, temperature=1, axis=0):
    return np.exp(np.divide(x, temperature)) / np.expand_dims(np.sum(np.exp(np.divide(x, temperature)), axis=axis), axis=1)


def reverse_sigmoid(x):
    return safe_log(1 - x) - safe_log(x)


def add_bias_and_multiply(weights, inputs):
    cat_state = np.hstack((inputs, np.ones((inputs.shape[0], 1))))
    return np.dot(cat_state, weights)


def count_gru_weights(state_count, input_count, output_count):
    return 3*state_count**2+state_count*(3*input_count+output_count+4)


def count_lr_weights(state_count, output_count):
    return output_count*(state_count+1)


def count_ffbs_weights(state_count, input_count):
    return state_count*(1+state_count+input_count)


def init_hmm_ffbs_weights(state_count, obs_count, flatten=False):
    ''' Randomly intialize pi, trans, obs mats with
        appropriate distribution and 0-1 constraints
    '''
    init_pi = np.random.random((state_count, 1))
    init_pi = init_pi / np.sum(init_pi)
    init_trans = np.random.random((state_count, state_count))
    init_trans = init_trans / np.sum(init_trans, 1, keepdims=True)
    init_obs = np.random.random((state_count, obs_count))

    if flatten:
        init_weights = np.hstack((safe_log(init_pi.flatten()),
                                  safe_log(init_trans.flatten()),
                                  reverse_sigmoid(init_obs.flatten())))
        return init_weights

    return init_pi, init_trans, init_obs


def init_hmm_emission_weights(state_count, obs_count, flatten=False, emission_type='bernoulli'):
    init_pi = np.random.random((state_count, 1))
    init_pi = init_pi / np.sum(init_pi)
    init_trans = np.random.random((state_count, state_count))
    init_trans = init_trans / np.sum(init_trans, 1, keepdims=True)

    if emission_type == 'bernoulli':
        init_eta = bernoulli_multivariate.init_natural_param_array(obs_count, state_count)
        if flatten:
            init_weights = np.hstack((safe_log(init_pi.flatten()),
                                      safe_log(init_trans.flatten()),
                                      init_eta.flatten()))
            return init_weights
        return init_pi, init_trans, init_eta

    else:  # emission_type == 'gaussian':
        init_eta_mu, init_eta_stddev = diagonal_gaussian_multivariate.init_natural_param_array(obs_count, state_count)
        if flatten:
            init_weights = np.hstack((safe_log(init_pi.flatten()),
                                      safe_log(init_trans.flatten()),
                                      init_eta_mu.flatten(),
                                      init_eta_stddev.flatten()))
            return init_weights
        return init_pi, init_trans, init_eta_mu, init_eta_stddev


def init_hmm_out_weights(state_count, output_count=None, param_scale=0.01):
    init_weights = param_scale * \
        np.random.normal(0, 1, (output_count, state_count+1)).flatten()
    return init_weights


def init_vanilla_gru_weights(state_count, input_count, output_count, param_scale=0.01):
    return np.random.randn(count_gru_weights(state_count,
                                           input_count,
                                           output_count)) * param_scale


def flatten_io(input_set, output_set=None):
    in_dim_count = input_set.shape[0]
    input_set = np.reshape(input_set, (in_dim_count, -1))
    if output_set is None:
        return input_set
    else:
        out_dim_count = output_set.shape[0]
        output_set = np.reshape(output_set, (out_dim_count, -1))
        return input_set, output_set
