import argh
from argh import arg
import cPickle
from os.path import join
import autograd.numpy as np
import common_util
import pdb


def normalize(X, axis=0):
    return np.divide(X.T, np.sum(X, axis=axis)).T


def toy_matrices():
    pi_mat = np.array([.5, .5, 0, 0, 0])
    trans_mat = np.array(([.5, .5, 0, 0, 0],
                          [.25, .5, .25, 0, 0],
                          [0, .25, .5, .25, 0],
                          [0, 0, .25, .5, .25],
                          [0, 0, 0, .5, .5]))
    obs_mat = np.array(([.5, .5, .5, 0, 0, 0, 0],
                        [0, .5, .5, .5, 0, 0, 0],
                        [0, 0, .5, .5, .5, 0, 0],
                        [0, 0, 0, .5, .5, .5, 0],
                        [0, 0, 0, 0, .5, .5, .5]))
    # obs_mat = np.array( ( [ 1, 0, 0, 0, 0, 0, 0 ], \
    #                       [ 0, 1, 0, 0, 0, 0, 0 ], \
    #                       [ 0, 0, 1, 0, 0, 0, 0 ], \
    #                       [ 0, 0, 0, 1, 0, 0, 0 ], \
    #                       [ 0, 0, 0, 0, 1, 0, 0 ] ) )
    return pi_mat, trans_mat, obs_mat


def spurious_matrices():
    pi_mat = np.array([.2, .2, .2, .2, .2])
    trans_mat = np.array(([.2, .2, .2, .2, .2],
                          [.2, .2, .2, .2, .2],
                          [.2, .2, .2, .2, .2],
                          [.2, .2, .2, .2, .2],
                          [.2, .2, .2, .2, .2]))
    obs_mat = np.array(([.5, .5, .5, 0, 0, 0, 0],
                        [0, .5, .5, .5, 0, 0, 0],
                        [0, 0, .5, .5, .5, 0, 0],
                        [0, 0, 0, .5, .5, .5, 0],
                        [0, 0, 0, 0, .5, .5, .5]))
    return pi_mat, trans_mat, obs_mat


def create_discrete_toy_data(
        data_count, time_count, bias_mat=np.array([15, 15]),
        weight_mat=np.array(([10, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0],
                             [0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0]))):

    # N is the number of samples and T is the length of the series.
    # Store data in DxTxN array because we'll want to slice by samples.

    # weight_mat is Ox(K+D)-dimensional.
    # bias_mat is O-dimensional (determines the proportion of 0s and 1s in
    # binary output).

    # Define the HMM:
    #   K is the number of states
    #   trans_mat(k,k') is the probability that we transition to k' from k (KxK-dimensional)
    # obs_mat(k,d) is the probability of 1 in dimension d in state k
    # (KxD-dimensional)
    state_count = 5  # number of states K (default = 5)
    # observation dimension D (default=7)
    dim_count = np.shape(weight_mat)[1] - state_count
    out_count = np.shape(weight_mat)[0]  # output dimension O (default=2)

    pi_mat, trans_mat, obs_mat = toy_matrices()

    # Create the sequences
    obs_set = np.zeros((dim_count, time_count, data_count), dtype=int)
    out_set = np.zeros((out_count, time_count, data_count), dtype=int)
    state_set = np.zeros((state_count, time_count, data_count), dtype=int)
    for data_iter in range(data_count):
        for time_iter in range(time_count):
            if time_iter == 0:
                state = np.random.multinomial(1, pi_mat)
                state_set[:, 0, data_iter] = state
            else:
                tvec = np.dot(state_set[:, time_iter - 1, data_iter], trans_mat)
                state = np.random.multinomial(1, tvec)
                state_set[:, time_iter, data_iter] = state
    for data_iter in range(data_count):
        for time_iter in range(time_count):
            obs_vec = np.dot(state_set[:, time_iter, data_iter], obs_mat)
            obs = np.random.binomial(1, obs_vec)
            obs_set[:, time_iter, data_iter] = obs
            in_vec = np.hstack((state_set[:, time_iter, data_iter],
                                obs_set[:, time_iter, data_iter]))
            out_vec = 1 / (1 + np.exp(-1 * (np.dot(weight_mat, in_vec) - bias_mat)))
            out = np.random.binomial(1, out_vec)
            out_set[:, time_iter, data_iter] = out

    # collect the outputs
    param_set = {'state_set': state_set,
                 'pi_mat': pi_mat,
                 'trans_mat': trans_mat,
                 'obs_mat': obs_mat,
                 'weight_mat': weight_mat,
                 'bias_mat': bias_mat}

    # output
    return obs_set, out_set, param_set


def create_continuous_toy_data(
        data_count, time_count, bias_mat=np.array([15, 15]),
        weight_mat=np.array(([10, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0],
                             [0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0]))):

    ''' Similar to the discrete toy data but sampling from Gaussian
        to create a continuous state based dataset.
    '''
    state_count = 5
    dim_count = np.shape(weight_mat)[1] - state_count
    out_count = np.shape(weight_mat)[0]

    pi_mat, trans_mat, _ = toy_matrices()  # obs_mat not useful here
    obs_set = np.zeros((dim_count, time_count, data_count))
    out_set = np.zeros((out_count, time_count, data_count), dtype=int)
    state_set = np.zeros((state_count, time_count, data_count), dtype=int)

    # generate state sequences
    for data_iter in range(data_count):
        for time_iter in range(time_count):
            if time_iter == 0:
                state = np.random.multinomial(1, pi_mat)
                state_set[:, 0, data_iter] = state
            else:
                tvec = np.dot(state_set[:, time_iter - 1, data_iter], trans_mat)
                state = np.random.multinomial(1, tvec)
                state_set[:, time_iter, data_iter] = state

    mu_set = np.argmax(state_set, axis=0)
    sigma_set = np.ones(dim_count)*np.sqrt(2)

    # generate observations
    for dim_iter in range(dim_count):
        obs_set[dim_iter, :, :] = np.random.randn(
            time_count, data_count)*sigma_set[dim_iter] + mu_set[dim_iter]

    # generate outputs
    for data_iter in range(data_count):
        for time_iter in range(time_count):
            in_vec = np.hstack((state_set[:, time_iter, data_iter],
                                obs_set[:, time_iter, data_iter]))
            out_vec = 1 / (1 + np.exp(-1 * (np.dot(weight_mat, in_vec) - bias_mat)))
            out = np.random.binomial(1, out_vec)
            out_set[:, time_iter, data_iter] = out

    param_set = {'state_set': state_set,
                 'pi_mat': pi_mat,
                 'trans_mat': trans_mat,
                 'mu_set': mu_set,
                 'sigma_set': sigma_set,
                 'weight_mat': weight_mat,
                 'bias_mat': bias_mat}

    return obs_set, out_set, param_set


def create_discrete_2hmm_toy_data(
        data_count, time_count, bias_mat=np.array([15, 15]),
        weight_mat=np.array(([10, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0],
                             [0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0]))):

    # Define two independent HMMs. Both will help generate the observations but one
    # one of them will generate the output. The HMM not modelling output is
    # basically noise.

    state_count = 5  # number of states K (default = 5)
    # observation dimension D (default=7)
    dim_count = np.shape(weight_mat)[1] - state_count
    out_count = np.shape(weight_mat)[0]  # output dimension O (default=2)

    pi_mat_1, trans_mat_1, obs_mat_1 = toy_matrices()  # hmm1
    pi_mat_2, trans_mat_2, obs_mat_2 = spurious_matrices()  # hmm2

    # store results here (int because only integers)
    obs_set = np.zeros((dim_count * 2, time_count, data_count), dtype=int)
    out_set = np.zeros((out_count, time_count, data_count), dtype=int)
    state_set_1 = np.zeros((state_count, time_count, data_count), dtype=int)  # hmm1
    state_set_2 = np.zeros((state_count, time_count, data_count), dtype=int)  # hmm2

    # create state sequences for both
    for data_iter in range(data_count):
        for time_iter in range(time_count):
            if time_iter == 0:
                state_1 = np.random.multinomial(1, pi_mat_1)
                state_2 = np.random.multinomial(1, pi_mat_2)
                state_set_1[:, 0, data_iter] = state_1
                state_set_2[:, 0, data_iter] = state_2
            else:
                tvec_1 = np.dot(state_set_1[:, time_iter - 1, data_iter], trans_mat_1)
                tvec_2 = np.dot(state_set_2[:, time_iter - 1, data_iter], trans_mat_2)
                state_1 = np.random.multinomial(1, tvec_1)
                state_2 = np.random.multinomial(1, tvec_2)
                state_set_1[:, time_iter, data_iter] = state_1
                state_set_2[:, time_iter, data_iter] = state_2

    # generate obs and out matrices
    for data_iter in range(data_count):
        for time_iter in range(time_count):
            # obs
            obs_vec_1 = np.dot(state_set_1[:, time_iter, data_iter], obs_mat_1)
            obs_vec_2 = np.dot(state_set_2[:, time_iter, data_iter], obs_mat_2)
            obs_1 = np.random.binomial(1, obs_vec_1)
            obs_2 = np.random.binomial(1, obs_vec_2)
            obs = np.hstack((obs_1, obs_2))  # concat together
            obs_set[:, time_iter, data_iter] = obs

            # out
            in_vec = np.hstack((state_set_1[:, time_iter, data_iter],  # only use hmm1 to make output
                                obs_set[:, time_iter, data_iter][:dim_count]))
            out_vec = 1 / (1 + np.exp(-1 * (np.dot(weight_mat, in_vec) - bias_mat)))
            out = np.random.binomial(1, out_vec)
            out_set[:, time_iter, data_iter] = out

    # collect the outputs
    param_set = {
        'state_set_1': state_set_1,
        'pi_mat_1': pi_mat_1,
        'trans_mat_1': trans_mat_1,
        'obs_mat_1': obs_mat_1,
        'state_set_2': state_set_2,
        'pi_mat_2': pi_mat_2,
        'trans_mat_2': trans_mat_2,
        'obs_mat_2': obs_mat_2,
        'weight_mat': weight_mat,
        'bias_mat': bias_mat
    }

    return obs_set, out_set, param_set


def create_continuous_2hmm_toy_data(
        data_count, time_count, bias_mat=np.array([15, 15]),
        weight_mat=np.array(([10, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0],
                             [0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0]))):
    state_count = 5
    dim_count = np.shape(weight_mat)[1] - state_count
    out_count = np.shape(weight_mat)[0]

    pi_mat_1, trans_mat_1, _ = toy_matrices()
    pi_mat_2, trans_mat_2, _ = spurious_matrices()

    obs_set = np.zeros((dim_count * 2, time_count, data_count), dtype=int)
    out_set = np.zeros((out_count, time_count, data_count), dtype=int)
    state_set_1 = np.zeros((state_count, time_count, data_count), dtype=int)  # hmm1
    state_set_2 = np.zeros((state_count, time_count, data_count), dtype=int)  # hmm2

    # create state sequences for both
    for data_iter in range(data_count):
        for time_iter in range(time_count):
            if time_iter == 0:
                state_1 = np.random.multinomial(1, pi_mat_1)
                state_2 = np.random.multinomial(1, pi_mat_2)
                state_set_1[:, 0, data_iter] = state_1
                state_set_2[:, 0, data_iter] = state_2
            else:
                tvec_1 = np.dot(state_set_1[:, time_iter - 1, data_iter], trans_mat_1)
                tvec_2 = np.dot(state_set_2[:, time_iter - 1, data_iter], trans_mat_2)
                state_1 = np.random.multinomial(1, tvec_1)
                state_2 = np.random.multinomial(1, tvec_2)
                state_set_1[:, time_iter, data_iter] = state_1
                state_set_2[:, time_iter, data_iter] = state_2

    mu_set_1 = state_set_1
    mu_set_2 = state_set_2
    sigma_set = np.ones(dim_count)*np.sqrt(2)

    # generate observations
    for dim_iter in range(dim_count):
        obs_1 = np.random.randn(time_count, data_count)*sigma_set[dim_iter] + mu_set_1[dim_iter]
        obs_2 = np.random.randn(time_count, data_count)*sigma_set[dim_iter] + mu_set_2[dim_iter]
        obs_set[dim_iter, :, :] = obs_1
        obs_set[(dim_count-1)+dim_iter, :, :] = obs_2

    # generate outputs
    for data_iter in range(data_count):
        for time_iter in range(time_count):
            in_vec = np.hstack((state_set_1[:, time_iter, data_iter],
                                obs_set[:, time_iter, data_iter][:dim_count]))
            out_vec = 1 / (1 + np.exp(-1 * (np.dot(weight_mat, in_vec) - bias_mat)))
            out = np.random.binomial(1, out_vec)
            out_set[:, time_iter, data_iter] = out

    param_set = {
        'state_set_1': state_set_1,
        'pi_mat_1': pi_mat_1,
        'trans_mat_1': trans_mat_1,
        'state_set_2': state_set_2,
        'pi_mat_2': pi_mat_2,
        'trans_mat_2': trans_mat_2,
        'mu_set_1':mu_set_1,
        'mu_set_2':mu_set_2,
        'stdev_set':stdev_set,
        'weight_mat': weight_mat,
        'bias_mat': bias_mat
    }

    return obs_set, out_set, param_set


@arg('data_type', help='select from toy_obs_only, toy_obs_and_out, toy_two_hmm')
@arg('-tr', '--train_count', default=20, help='number of data groups in train set')
@arg('-te', '--test_count', default=10, help='number of data groups in test set')
@arg('-va', '--valid_count', default=0, help='number of data groups in validation set')
@arg('-t', '--time_count', default=50, help='number of time indices per group')
@arg('-s', '--save_path', default='.', help='directory to save numpy files')
@arg('-b', '--binary', default=True, help='whether to generated binary or continuous data')
def output_toy_data(data_type,
                    train_count=20,
                    test_count=10,
                    valid_count=0,
                    time_count=50,
                    save_path=None,
                    binary=True):
    ''' Runs create_discrete_toy_data or create_discrete_2hmm_toy_data and saves
        it into the X_train, y_train, ... style

        Args
        ----
        data_type : string
                    Choose from toy_obs_only, toy_obs_and_out, toy_two_hmm
        train_count : int
                      Number of groups in training set
        test_count : int
                     Number of groups in testing set
        valid_count : int
                      Number of groups in validation set
        time_count : int
                     Number of time steps per group
        save_path : string / None
                    Where to save the outputs
        binary : boolean
                 whether to generated binary or continuous data

        Returns
        -------
        X_train : np array
        y_train : np array
        X_test : np array
        y_test : np array
        X_valid : np array
        y_valid : np array

    '''
    data_count = train_count + test_count + valid_count

    if data_type == 'toy_obs_only':
        bias_mat = np.array([5, 5])
        weight_mat = np.array(([10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
        func = create_discrete_toy_data if binary else create_continuous_toy_data
        obs_set, out_set, param_set = func(data_count, time_count, bias_mat, weight_mat)
    elif data_type == 'toy_obs_and_out':
        bias_mat = np.array([15, 15])
        weight_mat = np.array(([10, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0],
                               [0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0]))
        func = create_discrete_toy_data if binary else create_continuous_toy_data
        obs_set, out_set, param_set = func(data_count, time_count, bias_mat, weight_mat)
    elif data_type == 'toy_two_hmm':
        bias_mat = np.array([15, 15])
        weight_mat = np.array(([10, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0],
                               [0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0]))
        func = create_discrete_2hmm_toy_data if binary else create_continuous_2hmm_toy_data
        obs_set, out_set, param_set = func(data_count, time_count, bias_mat, weight_mat)

    if save_path is None:
        save_path = join('datasets', data_type)

    np.save(join(save_path, 'obs_set.npy'), obs_set)
    np.save(join(save_path, 'out_set.npy'), out_set)
    with open(join(save_path, 'param_set.pkl'), 'wb') as fp:
        cPickle.dump(param_set, fp)

    # do a train_test_split by hand
    train_obs_set = obs_set[:, :, :train_count]
    train_out_set = out_set[:, :, :train_count]
    test_obs_set = obs_set[:, :, train_count:train_count+test_count]
    test_out_set = out_set[:, :, train_count:train_count+test_count]
    valid_obs_set = obs_set[:, :, train_count+test_count:data_count]
    valid_out_set = out_set[:, :, train_count+test_count:data_count]

    train_obs_set, train_fcpt_set = common_util.map_3d_to_2d(train_obs_set)
    valid_obs_set, valid_fcpt_set = common_util.map_3d_to_2d(valid_obs_set)
    test_obs_set, test_fcpt_set = common_util.map_3d_to_2d(test_obs_set)

    train_out_set, _ = common_util.map_3d_to_2d(train_out_set)
    valid_out_set, _ = common_util.map_3d_to_2d(valid_out_set)
    test_out_set, _ = common_util.map_3d_to_2d(test_out_set)

    np.save(join(save_path, 'X_train.npy'), train_obs_set)
    np.save(join(save_path, 'y_train.npy'), train_out_set)
    np.save(join(save_path, 'fcpt_train.npy'), train_fcpt_set)
    np.save(join(save_path, 'X_test.npy'), test_obs_set)
    np.save(join(save_path, 'y_test.npy'), test_out_set)
    np.save(join(save_path, 'fcpt_test.npy'), test_fcpt_set)
    np.save(join(save_path, 'X_valid.npy'), valid_obs_set)
    np.save(join(save_path, 'y_valid.npy'), valid_out_set)
    np.save(join(save_path, 'fcpt_valid.npy'), valid_fcpt_set)

if __name__ == '__main__':
    argh.dispatch_command(output_toy_data)

