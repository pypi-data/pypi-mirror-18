''' Often time series data may be too long for machines to
    handle. We need a good way of sub-sampling a long time
    series sequence.

    My plan is to for each data sequence, find the locations
    of the positive examples. Pick some number of them. And then
    subsample randomly for the negative examples bewteen the
    positive ones as well.
'''

import numpy as np


def subsample_array(A, num, return_indexes=False):
    indexes = np.sort(np.random.choice(xrange(A.size), size=num))
    if return_indexes:
        return indexes
    return A[indexes]


class LocalTimeSeriesSampler(object):
    ''' LocalTimeSeriesSampler

        Takes every single positive example but keeps only a
        local subset of the negative examples.

        Example:

        y = 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 1 0 1 0 0 1 0 0 0 0 0 0 1 0 0 0 0 1
        t = 1 2 3 4 5 6 7 8 9 a b c d e f g h i j k l m n o p q r s t u v w x y z

        First sequence: t = 1 2 3 4 5 6
        Second sequence: t = a b c d e f g h i j k l m
        Third sequence: t = o p q r s t u v w x y

        Args:
        pre_range <- number of local examples to take before every + example
             this should be large (50-500)
        post_range <- number of local examples to take after every + example
             this should be small (0-50)
        pos_frac <- fraction of positive examples to take (default 1)
    '''

    def _init__(self):
        pass

    def subsample(self, X, y, fcpt,
                              pre_range=100,
                              post_range=0,
                              pos_frac=1):
        ''' Args
            ----
            X : np array
               a (F x N) matrix where F is # features,
               N is a flattened time x data points
            y : np array
                is a (1 x N) matrix
                multidimensional outputs are not supported.
            fcpt : np array
                   a D + 1 array showing the splits between data
            pos_frac : double
            pre_range : integer
            post_range : integer

            Returns
            -------
            sub_X : np array
                    a (F x M) matrix where t is a subset of T
            sub_y : np array
                    a (O x M) matrix (binary)
            sub_fcpt : np array
                       a D'+1 array
        '''

        assert pos_frac >= 0 and pos_frac <= 1, \
            'fraction of positive examples must be between 0 and 1'
        assert pre_range >= 0, 'pre_range must be greater than 0'
        assert post_range >= 0, 'pre_range must be greater than 0'
        assert len(X.shape) == 2, '<X> must be 2 dimensional.'
        assert len(y.shape) == 2, '<y> must be 2 dimensional.'
        assert y.shape[0] == 1, '<y> can only have 1 dimension for now'
        assert list(np.unique(y)) == [0, 1], '<y> must only contain 0 or 1.'

        num_features, num_collapse = X.shape
        num_data = fcpt.size - 1

        sub_X, sub_y, sub_fcpt = [], [], [0]

        for data_i in range(num_data):
            fcpt_s_i = fcpt[data_i]
            fcpt_e_i = fcpt[data_i+1]
            num_time = fcpt_e_i - fcpt_s_i

            # grab the current outputs as a flat array
            cur_y = y[0, fcpt_s_i:fcpt_e_i]

            # find indexes of positive samples
            cur_y_where_pos = np.where(cur_y > 0)[0]
            if pos_frac < 1:
                cur_y_where_pos = np.random.choice(
                    cur_y_where_pos,
                    int(cur_y_where_pos.shape[0]*pos_frac))

            indexes_to_keep = []
            for i in range(len(cur_y_where_pos[:-1])):
                cur_idx = cur_y_where_pos[i]
                nex_idx = cur_y_where_pos[i+1]

                s_i = cur_idx-pre_range
                e_i = cur_idx+post_range
                if e_i >= nex_idx:
                    e_i = nex_idx - 1

                cur_slice = range(s_i, e_i+1)
                indexes_to_keep += cur_slice

            # do same for last index
            cur_idx = cur_y_where_pos[-1]
            s_i = cur_idx-pre_range
            e_i = num_time - 1
            cur_slice = range(s_i, e_i+1)
            indexes_to_keep += cur_slice
            indexes_to_keep = np.array(indexes_to_keep)
            indexes_to_keep = np.sort(np.unique(indexes_to_keep[indexes_to_keep >= 0]))
            # shift to true index
            indexes_to_keep += fcpt_s_i

            cur_X = X[:, indexes_to_keep]
            cur_y = y[:, indexes_to_keep]
            cur_fcpt = indexes_to_keep.size + fcpt_s_i

            sub_X.append(cur_X)
            sub_y.append(cur_y)
            sub_fcpt.append(cur_fcpt)

        sub_X = np.concatenate(sub_X, axis=1)
        sub_y = np.concatenate(sub_y, axis=1)
        sub_fcpt = np.array(sub_fcpt)

        return sub_X, sub_y, sub_fcpt
