import numpy as np
from rlstm.nn_util import sigmoid, add_bias_and_multiply
import time

def benchmark_runtime_for_func(func, *args, **kwargs):
    if 'n_reps' in kwargs:
        n_reps = kwargs['n_reps']
        del kwargs['n_reps']
    else:
        n_reps = 1
    elapsed_time_sec_per_rep = np.zeros(n_reps)
    for rep in xrange(n_reps):
        start_time_sec = time.time()
        func(*args, **kwargs)
        elapsed_time_sec_per_rep[rep] = time.time() - start_time_sec

    print "n_reps %d  median sec %9.4f  max sec %9.4f  %s" % (
        n_reps,
        np.median(elapsed_time_sec_per_rep),
        np.max(elapsed_time_sec_per_rep),
        func.__name__,
        )
    return np.mean(elapsed_time_sec_per_rep), elapsed_time_sec_per_rep

def simple_update_for_single_timestep_with_preweighted_input(
        curr_weighted_input,
        prev_hiddens,
        update_x_weights,
        update_h_weights):
    update = sigmoid(
        curr_weighted_input +
        np.dot(prev_hiddens, update_h_weights))
    hiddens = (1 - update) * prev_hiddens
    return hiddens

def simple_update_for_single_timestep(
        curr_input,
        prev_hiddens,
        update_x_weights,
        update_h_weights):
    update = sigmoid(
        add_bias_and_multiply(update_x_weights, curr_input) +
        np.dot(prev_hiddens, update_h_weights))
    hiddens = (1 - update) * prev_hiddens
    return hiddens

def calc_loss_one_sequence_some_vectorization(
        curr_input=None,
        hiddens=None,
        update_x_weights=None,
        update_h_weights=None):
    weighted_input = add_bias_and_multiply(update_x_weights, curr_input.T)
    loss = 0.0
    time_count = curr_input.shape[1]
    for time_iter in range(time_count):
        hiddens = simple_update_for_single_timestep_with_preweighted_input(
            weighted_input[time_iter],
            hiddens,
            update_x_weights,
            update_h_weights)
        loss = loss + np.sum(hiddens)
    return loss

def calc_loss_one_sequence_forloop(
        curr_input=None,
        hiddens=None,
        update_x_weights=None,
        update_h_weights=None):
    loss = 0.0
    time_count = curr_input.shape[1]
    for time_iter in range(time_count):
        hiddens = simple_update_for_single_timestep(
            np.expand_dims(curr_input[:, time_iter], axis=0),
            hiddens,
            update_x_weights,
            update_h_weights)
        loss = loss + np.sum(hiddens)
    return loss

if __name__ == '__main__':
    T = 20000
    D = 6
    H = 100
    prng = np.random.RandomState(0)
    curr_input = prng.randn(D, T)
    update_x_weights = prng.randn(D+1, H)
    update_h_weights = prng.randn(H, H)
    hiddens = prng.randn(1, H)

    loss1 = calc_loss_one_sequence_forloop(
        curr_input,
        hiddens,
        update_x_weights,
        update_h_weights)
    print loss1

    loss2 = calc_loss_one_sequence_some_vectorization(
        curr_input,
        hiddens,
        update_x_weights,
        update_h_weights)
    print loss2

    args = (curr_input, hiddens, update_x_weights, update_h_weights)

    # Time the old-school forloop over each timestep
    benchmark_runtime_for_func(
        calc_loss_one_sequence_forloop,
        *args,
        n_reps=3)

    # Time the newer version, which does some vectorization
    benchmark_runtime_for_func(
        calc_loss_one_sequence_some_vectorization,
        *args,
        n_reps=3)
