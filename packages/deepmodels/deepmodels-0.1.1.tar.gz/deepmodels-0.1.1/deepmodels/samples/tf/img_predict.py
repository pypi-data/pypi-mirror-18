"""Sample of loading a trained model to do prediction.
"""

import glob
import os

import numpy as np

import tensorflow as tf
import tensorflow.contrib.slim as slim

from deepmodels.core import commons
from deepmodels.core.tf import common_flags
from deepmodels.core.tf import model_zoo
from deepmodels.core.tf import data_provider
from deepmodels.core.tf.templates.dm_classifier import DMClassifier


flags = tf.app.flags
FLAGS = flags.FLAGS


class MyClassifier(DMClassifier):
  def build_model(self, inputs, model_params):
    pred_logits, end_points = model_zoo.build_net(
        commons.NetNames.INCEPTION_V3,
        inputs, model_params.cls_num,
        commons.ModelMode.TEST)
    self.input_tensor_name = inputs.name
    self.output_tensor_name = pred_logits.name
    return pred_logits, end_points


def classify_imgs(img_format=commons.ImgFormat.JPG,
                  net_type=commons.NetNames.VGG16):
  """Perform classification on images of a given directory.

  Args:
    img_format: format of image files.
    net_type: type of pretrained model. Only VGG16 has been tested.
  """
  net_params = model_zoo.net_params[net_type]
  preprocess_fn = model_zoo.net_preprocess(net_type, commons.ModelMode.TEST)
  if FLAGS.img_dir != "":
    imgs, img_fns = data_provider.load_img_fns(FLAGS.img_dir,
                                               net_params.input_img_width,
                                               net_params.input_img_height,
                                               img_format=img_format,
                                               scaling=True,
                                               preprocess_fn=preprocess_fn)
    assert len(img_fns) > 0, "no image files found."
  if FLAGS.input_meta != "":
    batch_data = data_provider.clf_input_from_image_fns(
        FLAGS.input_meta, 3,
        net_params.input_img_width,
        net_params.input_img_height,
        FLAGS.batch_size,
        scaling=True,
        preprocess_fn=preprocess_fn,
        shuffle=True)
    imgs, _, fn_batch, _, _ = batch_data
    img_fns = fn_batch.eval(session=tf.Session())

  # build model.
  model_params = commons.ModelParams(model_type=net_type,
                                     model_mode=commons.ModelMode.TEST,
                                     cls_num=net_params.cls_num)
  my_clf = MyClassifier()
  my_clf.build_model(imgs, model_params)
  model_fn = model_zoo.get_default_net_weights_fn(net_type)
  my_clf.load_model_from_checkpoint_fn(model_fn)
  all_imgs = imgs.eval(session=tf.Session())
  # prediction.
  pred_labels, pred_probs = my_clf.predict(all_imgs)
  top_k = 5
  label_to_name = model_zoo.net_label_names(net_type)
  for img_id in range(len(img_fns)):
    fn_parts = img_fns[img_id].split("/")
    disp_fn = "{}/{}".format(fn_parts[-2], fn_parts[-1])
    print "image: {}".format(disp_fn)
    for k in range(top_k):
      cur_label = pred_labels[img_id, k]
      cur_prob = pred_probs[img_id, k]
      print "{}:{} ({})".format(k, label_to_name[cur_label], cur_prob)
    print ""


# TODO(jiefeng): finish implementation.
def classify_imgs_from_pb(img_dir, img_format=commons.ImgFormat.JPG):
  """Use model saved in pb file, e.g. inceptionv3 production version.
  """
  # load data.
  net_params = model_zoo.net_params[commons.NetNames.INCEPTION_V3]
  imgs, img_fns = load_img_fns(img_dir,
                               net_params.input_img_width,
                               net_params.input_img_height,
                               img_format=img_format)


def main(_):
  tf.logging.set_verbosity(tf.logging.INFO)
  classify_imgs(net_type=commons.NetNames.INCEPTION_V3)


if __name__ == "__main__":
  tf.app.run()
