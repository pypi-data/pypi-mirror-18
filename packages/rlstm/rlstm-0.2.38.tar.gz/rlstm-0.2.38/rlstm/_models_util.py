from __future__ import print_function
from collections import defaultdict

import autograd.numpy as np
from autograd import value_and_grad, grad
from rlstm.optimize import adam
from rlstm.debug_utils import getCurMemCost_MiB


# -- train functions --


def _train_by_sgd(
        obs_set,
        loglike_fun,
        logpred_fun,
        num_weights,
        out_set=None,
        init_weights=None,
        min_epoch=100,
        max_epoch=500,
        batch_size=128,
        param_scale=0.01,
        # regularization
        obs_lambda=0,
        l1_lambda=0,
        l2_lambda=0,
        num_l1_weights=0,
        num_l2_weights=0,
        # optimization
        stop_criterion=1e-3,
        early_stop=False,
        patience=10,
        regression=False,
        # validation set
        va_obs_set=None,
        va_out_set=None,
        # overwrite functions
        batch_indices=None,
        regularized_loss=None,
        batch_loss=None,
        callback=None):
    ''' Generic function for training using stochastic gradient descent.
        All models are wrapped around this function.
    '''

    # assume the *num_data* is always last index
    num_batches = int(np.ceil(obs_set.shape[-1] / float(batch_size)))

    if init_weights is None:
        init_weights = np.random.randn(num_weights) * param_scale

    # choose the proper error function
    error_func = get_mean_squared_error if regression else get_accuracy

    if batch_indices is None:
        def batch_indices(iter):
            idx = iter % num_batches
            return slice(idx * batch_size, (idx+1) * batch_size)

    # wrapper around loss function
    if regularized_loss is None:
        def regularized_loss(weights, obs_set,out_set):
            loss = loglike_fun(weights, obs_set, out_set)
            if not out_set is None and obs_lambda > 0:
                # Add a parameter to balance between out log-likelihood and obs log-likelihood
                loss += obs_lambda*loglike_fun(weights, obs_set, None)

            # negative log like + regularizers
            loss = -loss + \
                l1_lambda * np.sum(np.abs(weights[:num_l1_weights])) + \
                l2_lambda * np.sum(np.power(weights[:num_l2_weights], 2))
            return loss

    # loss function in batches
    if batch_loss is None:
        def batch_loss(weights, iter):
            idx = batch_indices(iter)
            batch_obs_set = obs_set[..., idx]
            batch_out_set = None if out_set is None else out_set[..., idx]
            return regularized_loss(weights, batch_obs_set, batch_out_set)

    if callback is None:
        def callback(e_i, b_i, ll, acc, va_ll, va_acc, x):
            print('epoch {:_<4}  |  batch {:_<2}/{:_<2}  |  loss {:_<10}  |  acc {:_<6}'.format(
                e_i,
                b_i+1,
                num_batches,
                round(ll, 4),
                round(acc, 4)))
            if b_i == num_batches - 1:
                print('======================================================================================================')
                print('EPOCH SUMMARY - LOSS {:_<10} | ACC {:_<6} | VA_LOSS {:_<10} | VA_ACC {:_<6} | MEM {:_<10}'.format(
                    round(ll, 4),
                    round(acc, 4),
                    round(va_ll, 4) if va_ll else 'nan',
                    round(va_acc, 4) if va_acc else 'nan',
                    getCurMemCost_MiB()))
                print('======================================================================================================')

    grad_fun = grad(batch_loss)
    weights = adam(grad_fun,
                   init_weights,
                   step_size=0.001,
                   num_batches=num_batches,
                   min_epoch=min_epoch,
                   max_epoch=max_epoch,
                   callback=callback,
                   stop_criterion=stop_criterion,
                   ll_fun=lambda x, i: batch_loss(x, i),
                   err_fun=lambda x, i: batch_error(x, i),
                   va_ll_fun=lambda x: regularized_loss(x, va_obs_set, va_out_set) if va_obs_set is not None else None,
                   va_err_fun=lambda x: error_func(va_out_set, np.exp(logpred_fun(x, va_obs_set))) if va_obs_set is not None else None,
                   early_stop=early_stop,
                   patience=patience)

    return weights
