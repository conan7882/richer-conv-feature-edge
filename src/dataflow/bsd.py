#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: bsd.py
# Author: Qian Ge <geqian1001@gmail.com>

import os
import numpy as np 
from scipy.io import loadmat

from src.dataflow.base import DataFlow
import src.utils.utils as utils
from src.utils.dataflow import load_image
# from ..common import *
# from ..normalization import *
# from tensorcv.dataflow.common import get_file_list, load_image
# from tensorcv.dataflow.image import ImageFromFile

def identity(inputs):
    return inputs

class BSDS500HED(DataFlow):
    def __init__(self,
                 name, 
                 data_dir='',
                 # n_channel,
                 shuffle=True,
                 batch_dict_name=None,
                 pf_list=None):

        im_dir = os.path.join(data_dir, 'images', name)
        gt_dir = os.path.join(data_dir, 'groundTruth', name)

        if pf_list is None:
            pf_list = [identity, identity]

        pf_list = utils.make_list(pf_list)
        if len(pf_list) == 1:
            pf_list.append(identity)
        assert len(pf_list) == 2

        def read_im(file_name):
            return load_image(file_name, read_channel=3,  pf=pf_list[0])

        def read_mat(file_name):
            gt = loadmat(file_name)['groundTruth'][0]
            num_gt = gt.shape[0]
            gt = sum(gt[k]['Boundaries'][0][0] for k in range(num_gt))
            gt = gt.astype('float32')
            gt = 1.0 * gt / num_gt
            zero_ind = gt < 0.3
            gt[zero_ind] = 0
            gt = pf_list[1](gt)
            gt[np.where(gt > 0)] = 1
            return gt

        super(BSDS500HED, self).__init__(
            data_name_list=['.jpg', '.mat'],
            data_dir_list=[im_dir, gt_dir],
            # data_dir=data_dir,
            shuffle=shuffle,
            batch_dict_name=batch_dict_name,
            load_fnc_list=[read_im, read_mat],
            # pf_list=pf_list
            )

# class BSDS500HED(ImageFromFile):
#     def __init__(self,
#                  name, 
#                  data_dir='', 
#                  shuffle=True, 
#                  # normalize=None,
#                  is_mask=False,
#                  # normalize_fnc=identity,
#                  # resize=None
#                  pf=identity,
#                  ):

#         assert name in ['train', 'test', 'val', 'infer']
#         self._load_name = name
#         self._is_mask = is_mask

#         super(BSDS500HED, self).__init__('.jpg', 
#                                       data_dir=data_dir, 
#                                       num_channel=3,
#                                       shuffle=shuffle, 
#                                       pf=pf,
#                                       # normalize=normalize,
#                                       # normalize_fnc=normalize_fnc,
#                                       # resize=resize
#                                       )

#     def next_batch_data(self):
#         batch_data = self.next_batch()
#         return {'image': batch_data[0], 'label': batch_data[1]}

#     def _load_file_list(self, _):
#         im_dir = os.path.join(self.data_dir, 'images', self._load_name)
#         self._im_list = get_file_list(im_dir, '.jpg')

#         gt_dir = os.path.join(self.data_dir, 'groundTruth', self._load_name)
#         self._gt_list = get_file_list(gt_dir, '.mat')

#         if self._shuffle:
#             self._suffle_file_list()

#     def _load_data(self, start, end):
#         input_im_list = []
#         input_label_list = []
#         for k in range(start, end):
#             im = load_image(self._im_list[k], read_channel=self._read_channel,
#                             resize=self._resize, pf=self._pf)
#             input_im_list.extend(im)

#             # gt = load_image(self._gt_list[k], read_channel=1,
#             #                 resize=self._resize)
#             # gt = gt * 1.0 / np.amax(gt)

#             gt = loadmat(self._gt_list[k])['groundTruth'][0]
#             num_gt = gt.shape[0]
#             gt = sum(gt[k]['Boundaries'][0][0] for k in range(num_gt))
#             gt = gt.astype('float32')
#             gt = 1.0 * gt / num_gt
#             zero_ind = gt < 0.3
#             gt[zero_ind] = 0
#             gt = self._pf(gt)
#             gt[np.where(gt > 0)] = 1
#             # try:
#             #     gt = misc.imresize(gt, (self._resize[0], self._resize[1]))
#             # except TypeError:
#             #     pass
#             # gt = np.squeeze(gt, axis = -1)
#             input_label_list.append(gt)

#         # input_im_list = self._normalize_fnc(np.array(input_im_list), 
#         #                                   self._get_max_in_val(), 
#         #                                   self._get_half_in_val())

#         input_label_list = np.array(input_label_list)
#         input_im_list = np.array(input_im_list) 

#         return input_im_list, input_label_list

#     def _suffle_file_list(self):
#         idxs = np.arange(self.size())
#         self.rng.shuffle(idxs)
#         self._im_list = self._im_list[idxs]
#         self._gt_list = self._gt_list[idxs]
#         # try:
#         #     self._mask_list = self._mask_list[idxs]
#         # except AttributeError:
#         #     pass
