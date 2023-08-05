"""Simple reconstruction algorithms.

This module defines a base class, ``Reconstruction``.
"""
import numpy as np
import pandas as pd     # noqa

from km3pipe.dataclasses import ArrayTaco, KM3DataFrame     # noqa
from km3pipe.tools import azimuth, zenith
from km3pipe import Module


class Reconstruction(Module):
    """Reconstruction base class.

    Parameters
    ----------
    hit_sel: str, default='Hits'
        Blob key of the hits to run the fit on.
    key_out: str, default='PrimFit'
        Key to write into.
    """

    def __init__(self, **kwargs):
        super(Reconstruction, self).__init__(**kwargs)
        self.hit_sel = self.get('hit_sel') or 'Hits'
        self.key_out = self.get('key_out') or 'PrimFit'

    def process(self, blob):
        hits = blob[self.hit_sel].serialise(to='pandas')
        reco = self.fit(hits)
        if reco is not None:
            blob[self.key_out] = KM3DataFrame.deserialise(
                reco, h5loc='/reco', fmt='dict')
        return blob

    def fit(self, hits):
        return


class PrimFitter(Reconstruction):
    """Primitive Linefit using Singular Value Decomposition.

    Parameters
    ----------
    hit_sel: str, default='Hits'
        Blob key of the hits to run the fit on.
    key_out: str, default='PrimFit'
        Key to write into.
    """
    def __init__(self, **kwargs):
        super(PrimFitter, self).__init__(**kwargs)
        self.hit_sel = self.get('hit_sel') or 'Hits'
        self.key_out = self.get('key_out') or 'PrimFit'

    def fit(self, hits):
        out = {}
        dus = np.unique(hits['dom_id'])
        n_dus = len(dus)

        if n_dus < 8:
            return

        pos = hits[['pos_x', 'pos_y', 'pos_z']]
        center = pos.mean(axis=0)

        _, _, v = np.linalg.svd(pos - center)

        reco_dir = np.array(v[0])
        reco_pos = center
        out = {
            'pos_x': reco_pos['pos_x'],
            'pos_y': reco_pos['pos_y'],
            'pos_z': reco_pos['pos_z'],
            'dir_x': reco_dir[0],
            'dir_y': reco_dir[1],
            'dir_z': reco_dir[2],
            'phi': azimuth(reco_dir),
            'theta': zenith(reco_dir),
        }
        return out
