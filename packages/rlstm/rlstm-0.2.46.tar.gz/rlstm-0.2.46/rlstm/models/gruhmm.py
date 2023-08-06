from __future__ import absolute_import, print_function

import pdb
from builtins import range
from copy import copy

import autograd.numpy as np
from autograd import value_and_grad
from autograd.scipy.misc import logsumexp

from rlstm.models import gru, hmm
from rlstm.weights_parser import WeightsParser
from rlstm.nn_util import sigmoid, add_bias_and_multiply
from rlstm.common_util import safe_log

# HMM provides continuous support for HMM through
# continuous emission functions.
from rlstm.emission_models import bernoulli_multivariate
from rlstm.emission_models import diagonal_gaussian_multivariate

# --------------------
#  GRUHMM CONSTRUCTOR
# --------------------


def build(
    input_count,
    hmm_state_count,
    gru_state_count,
    output_count,
    max_conn=0,
    redun_epsilon=0,
    emission_type='bernoulli'
):

    # emission_type defines the distribution behind the emission
    # matrix used in HMM. discrete and continuous matrices are supported.
    assert emission_type in [
        'bernoulli', 'gaussian'], 'EMISSION_TYPE not recognized.'

    if emission_type == 'bernoulli':
        emission_module = bernoulli_multivariate
        calc_log_proba_arr_for_x = emission_module.calc_log_proba_data_arr_NK
    else:  # must be gaussian
        emission_module = diagonal_gaussian_multivariate
        calc_log_proba_arr_for_x = emission_module.calc_log_proba_data_arr_NK_flat

    # the input count is just the number of input dimensions, we
    # assume that any/all 1-hot encoding, etc. has been done already.
    # the output count is the *number* of *binary* outputs (no
    # multinomial or continuous support at the moment)
    parser = WeightsParser()

    # GRU parameters
    parser.add_shape('init_hiddens', (1, gru_state_count))
    parser.add_shape('update_x_weights', (input_count + 1, gru_state_count))
    parser.add_shape('update_h_weights', (gru_state_count, gru_state_count))
    parser.add_shape('reset_x_weights', (input_count + 1, gru_state_count))
    parser.add_shape('reset_h_weights', (gru_state_count, gru_state_count))
    parser.add_shape('thidden_x_weights', (input_count + 1, gru_state_count))
    parser.add_shape('thidden_h_weights', (gru_state_count, gru_state_count))
    parser.add_shape('output_h_weights', (gru_state_count, output_count))

    num_gru_weights = parser.num_weights

    # HMM parameters
    parser.add_shape('lpi_mat', (hmm_state_count, 1))
    parser.add_shape('ltrans_mat', (hmm_state_count, hmm_state_count))
    if emission_type == 'bernoulli':
        parser.add_shape('eta_mat', (input_count, hmm_state_count))
    else:  # must be gaussian
        parser.add_shape('eta_mat', (input_count, hmm_state_count*2))
    parser.add_shape('output_hmm_weights', (output_count, hmm_state_count + 1))

    num_hmm_weights = parser.num_weights - num_gru_weights

    # Make predictions through a linear combination of GRU and HMM parameters
    def outputs(
        weights,
        input_set,
        fence_set,
        output_set=None,
        return_lstate_set=False,
        return_pred_set=False
    ):

        # grab all gru weights
        update_x_weights = parser.get(weights, 'update_x_weights')
        update_h_weights = parser.get(weights, 'update_h_weights')
        reset_x_weights = parser.get(weights, 'reset_x_weights')
        reset_h_weights = parser.get(weights, 'reset_h_weights')
        thidden_x_weights = parser.get(weights, 'thidden_x_weights')
        thidden_h_weights = parser.get(weights, 'thidden_h_weights')
        output_h_weights = parser.get(weights, 'output_h_weights')

        # grab hmm weights
        lpi_mat = parser.get(weights, 'lpi_mat')
        ltrans_mat = parser.get(weights, 'ltrans_mat')
        eta_mat = parser.get(weights, 'eta_mat')
        output_hmm_weights = parser.get(weights, 'output_hmm_weights')

        # normalize probas
        lpi_mat = lpi_mat - logsumexp(lpi_mat, axis=0)
        ltrans_mat = ltrans_mat - logsumexp(ltrans_mat, axis=1, keepdims=True)
        start_log_proba_K = lpi_mat.flatten()

        data_count = len(fence_set) - 1
        feat_count = input_set.shape[0]

        hmm_ll = 0.0
        gru_ll = 0.0
        n_i_track = 0
        fence_base = fence_set[0]

        pred_set = None
        lstate_set = None

        if return_pred_set:
            pred_set = np.zeros((output_count, input_set.shape[1]))

        if return_lstate_set:
            lstate_set = np.zeros((hmm_state_count, input_set.shape[1]))

        # the output set of dimension ( output_count, time_count, data_count )
        # output_set = np.zeros( ( output_count, time_count, data_count ) )
        for data_iter in range(data_count):
            # Initialize hidden states in the HMM
            hiddens = copy(parser.get(weights, 'init_hiddens'))

            # use fenceposts to get time sequences
            fence_post_1 = fence_set[data_iter] - fence_base
            fence_post_2 = fence_set[data_iter+1] - fence_base
            time_count = fence_post_2 - fence_post_1

            # grab sequence for this data_iter
            curr_input_DT = input_set[:, fence_post_1:fence_post_2]

            # add bias and multiply weights into inputs all together
            weighted_input_HT = add_bias_and_multiply(
                update_x_weights, curr_input_DT.T).T

            # get log proba array from emissions
            curr_input_log_proba_TK = calc_log_proba_arr_for_x(
                curr_input_DT, eta_DK=eta_mat)

            # Initialize fwd belief vector at t = 0
            cur_belief_log_proba_K = start_log_proba_K + \
                curr_input_log_proba_TK[0]
            cur_x_log_proba = logsumexp(cur_belief_log_proba_K)
            cur_belief_log_proba_K = cur_belief_log_proba_K - cur_x_log_proba

            # Loop over time steps
            for time_iter in range(time_count):
                # update gru
                hiddens = gru.update(
                    max_conn,
                    redun_epsilon,
                    np.expand_dims(weighted_input_HT[:, time_iter], axis=0),
                    hiddens,
                    update_x_weights,
                    update_h_weights,
                    reset_x_weights,
                    reset_h_weights,
                    thidden_x_weights,
                    thidden_h_weights
                )

                # update hmm
                if time_iter > 0:
                    cur_belief_log_proba_K, cur_x_log_proba = hmm.update_belief_log_probas(
                        cur_belief_log_proba_K,
                        curr_input_log_proba_TK[time_iter],
                        ltrans_mat
                    )

                # get ll
                lstate_norm = np.expand_dims(cur_belief_log_proba_K, axis=1)
                curr_state = np.vstack(
                    (copy(lstate_norm), np.ones((1, lstate_norm.shape[1]))))

                if output_set is not None:
                    out_proba = sigmoid(
                        np.sign(output_set[:, n_i_track] - 1e-3)
                        * (np.dot(hiddens, output_h_weights)
                           + np.transpose(np.dot(output_hmm_weights, curr_state))))
                    out_lproba = safe_log(out_proba)
                    gru_ll += np.sum(out_lproba)
                else:
                    out_proba = sigmoid(
                        np.dot(hiddens, output_h_weights)
                        + np.transpose(np.dot(output_hmm_weights, curr_state)))
                    out_lproba = safe_log(out_proba)

                if return_pred_set:
                    pred_set[:, n_i_track] = out_lproba[0]

                if return_lstate_set:
                    lstate_set[:, n_i_track] = cur_belief_log_proba_K

                n_i_track += 1

            my_ll = logsumexp(cur_belief_log_proba_K)
            hmm_ll = hmm_ll + my_ll

        return gru_ll, pred_set, hmm_ll, lstate_set

    def prediction(weights, input_set, fence_set):
        _, out, _, _ = outputs(
            weights,
            input_set,
            fence_set,
            return_pred_set=True
        )
        return out

    def log_likelihood(weights, input_set, fence_set, output_set=None):
        gru_ll, _, hmm_ll, _ = outputs(
            weights,
            input_set,
            fence_set,
            output_set=output_set,
            return_pred_set=False,
            return_lstate_set=False
        )

        return hmm_ll if output_set is None else gru_ll

    return prediction, log_likelihood, num_gru_weights, num_hmm_weights
