from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import cPickle as pickle
import os.path as osp

import numpy as np
from scipy.misc import imread
from sklearn.datasets.base import Bunch

import plyvel

import fcn


class SegmentationClassDataset(Bunch):

    target_names = np.array([
        'background',
        'aeroplane',
        'bicycle',
        'bird',
        'boat',
        'bottle',
        'bus',
        'car',
        'cat',
        'chair',
        'cow',
        'diningtable',
        'dog',
        'horse',
        'motorbike',
        'person',
        'potted plant',
        'sheep',
        'sofa',
        'train',
        'tv/monitor',
    ])
    mean_bgr = np.array((104.00698793, 116.66876762, 122.67891434))

    def __init__(self, db_path=None):
        super(self.__class__, self).__init__()
        if db_path is None:
            db_path = osp.join(fcn.data_dir, 'SegmentationClassDataset_db')
        self.db = plyvel.DB(db_path, create_if_missing=True)
        self.pascal_dir = osp.join(fcn.data_dir, 'pascal/VOC2012')
        self._load_segmentation_files()

    def _load_segmentation_files(self):
        for type in ['train', 'trainval', 'val']:
            id_list_file = osp.join(
                self.pascal_dir, 'ImageSets/Segmentation/{0}.txt'.format(type))
            ids = [id_.strip() for id_ in open(id_list_file)]
            setattr(self, type, np.array(ids))

    def _load_datum(self, id):
        # check cache
        datum = self.db.get(str(id))
        if datum is not None:
            return pickle.loads(datum)
        # there is no cache
        img_file = osp.join(self.pascal_dir, 'JPEGImages', id + '.jpg')
        img = imread(img_file, mode='RGB')
        label_rgb_file = osp.join(
            self.pascal_dir, 'SegmentationClass', id + '.png')
        label_rgb = imread(label_rgb_file, mode='RGB')
        label = self._label_rgb_to_32sc1(label_rgb)
        datum = (img, label)
        # save cache
        self.db.put(str(id), pickle.dumps(datum))
        return datum

    def _label_rgb_to_32sc1(self, label_rgb):
        assert label_rgb.dtype == np.uint8
        label = np.zeros(label_rgb.shape[:2], dtype=np.int32)
        label.fill(-1)
        cmap = fcn.util.labelcolormap(len(self.target_names))
        cmap = (cmap * 255).astype(np.uint8)
        for l, rgb in enumerate(cmap):
            mask = np.all(label_rgb == rgb, axis=-1)
            label[mask] = l
        return label

    def next_batch(self, batch_size, type, indices=None):
        """Generate next batch whose size is the specified batch_size."""
        ids = getattr(self, type)
        if indices is None:
            indices = np.random.randint(0, len(ids), batch_size)
        batch = []
        for id in ids[indices]:
            datum = self._load_datum(id)
            batch.append(datum)
        return batch

    @classmethod
    def img_to_datum(self, img):
        datum = img.astype(np.float32)
        datum = datum[:, :, ::-1]  # RGB -> BGR
        datum -= self.mean_bgr
        datum = datum.transpose((2, 0, 1))
        return datum

    @classmethod
    def datum_to_img(self, blob):
        bgr = blob.transpose((1, 2, 0))
        bgr += self.mean_bgr
        rgb = bgr[:, :, ::-1]  # BGR -> RGB
        rgb = rgb.astype(np.uint8)
        return rgb
