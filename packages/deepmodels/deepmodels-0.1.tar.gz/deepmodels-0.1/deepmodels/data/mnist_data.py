"""MNIST data manager.
"""

import os
import cPickle as pickle

import numpy as np

import tensorflow as tf

from ..tools import data_manager


class MNISTData(object):
  """Class to manage CIFAR10 data source.
  """
  train_imgs = None
  train_labels = None
  train_samp_num = 0
  train_cls_num = 0
  test_imgs = None
  test_labels = None
  test_samp_num = 0
  test_cls_num = 0


  def __init__(self):
    pass
  
  def load_base_data(self):
    pass
  
  def get_data_for_clf(self, data_type="train", batch_size=16, use_queue=True):
    """Get corresponding data for classification.

    Args:
      data_type: train or test.
    """
    if data_type == "train":
      if not use_queue:
        return self.train_imgs, self.train_labels, self.train_samp_num, self.train_cls_num
      else:
        data_tensor = tf.convert_to_tensor(self.train_imgs, tf.float32)
        label_tensor = tf.convert_to_tensor(self.train_labels, tf.int32)
        img_batch, label_batch = tf.train.shuffle_batch(
            [data_tensor, label_tensor],
            batch_size=batch_size,
            enqueue_many=True,
            capacity=batch_size*20,
            min_after_dequeue=batch_size)
        return img_batch, label_batch, self.train_samp_num, self.train_cls_num
    else:
      if not use_queue:
        return self.test_imgs, self.test_labels, self.test_samp_num, self.test_cls_num
      else:
        data_tensor = tf.convert_to_tensor(self.test_imgs, tf.float32)
        label_tensor = tf.convert_to_tensor(self.test_labels, tf.int32)
        img_batch, label_batch = tf.train.shuffle_batch(
            [data_tensor, label_tensor],
            batch_size=batch_size,
            enqueue_many=True,
            capacity=batch_size*20,
            min_after_dequeue=batch_size)
        return img_batch, label_batch, self.test_samp_num, self.test_cls_num