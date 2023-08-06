from __future__ import absolute_import
import bz2
try:
    import cPickle as pickle_
except ImportError:
    import pickle as pickle_
import os
import collections
from . import report
from . import object as object_
from . import path
from os.path import join
from os.path import isdir

class PickleByName(object):
    """Makes un-pickle-able objects pick-able by setting its un-pickle-able
    attributes as signature only attributes."""
    def __init__(self):
        self._signature_only_attrs = set()

    def set_signature_only_attr(self, attr_name):
        self._signature_only_attrs.add(attr_name)

    def __getstate__(self):
        d = self.__dict__.copy()
        for attr_name in self._signature_only_attrs:
            o = getattr(self, attr_name)

            d[attr_name + '_fullname'] = object_.fullname(o)
            d[attr_name + '_init_dict'] = o.init_dict()
            del d[attr_name]
        return d

    def __setstate__(self, d):
        import importlib

        for attr_name in d['_signature_only_attrs']:
            fn = d[attr_name + '_fullname']
            k = fn.rfind(".")
            module_name, class_name = fn[:k], fn[k+1:]
            init_dict = d[attr_name + '_init_dict']
            mod = importlib.import_module(module_name)
            class_ = getattr(mod, class_name)
            o = class_(**init_dict)
            d[attr_name] = o
            del d[attr_name + '_fullname']
            del d[attr_name + '_init_dict']

        self.__dict__.update(d)

class SlotPickleMixin(object):
    """Top-class that allows mixing of classes with and without slots.

    Takes care that instances can still be pickled with the lowest
    protocol. Moreover, provides a generic `__dir__` method that
    lists all slots.

    """

    # We want to allow weak references to the objects
    __slots__ = ['__weakref__']

    def _get_all_slots(self):
        """Returns all slots as set"""
        all_slots = (getattr(cls, '__slots__', [])
                         for cls in self.__class__.__mro__)
        return set(slot for slots in all_slots for slot in slots)

    def __getstate__(self):
        if hasattr(self, '__dict__'):
            # We don't require that all sub-classes also define slots,
            # so they may provide a dictionary
            statedict = self.__dict__.copy()
        else:
            statedict = {}
        # Get all slots of potential parent classes
        for slot in self._get_all_slots():
            try:
                value = getattr(self, slot)
                statedict[slot] = value
            except AttributeError:
                pass
        # Pop slots that cannot or should not be pickled
        statedict.pop('__dict__', None)
        statedict.pop('__weakref__', None)
        return statedict

    def __setstate__(self, state):
        for key, value in state.items():
            setattr(self, key, value)

    def __dir__(self):
        result = dir(self.__class__)
        result.extend(self._get_all_slots())
        if hasattr(self, '__dict__'):
            result.extend(self.__dict__.keys())
        return result

def pickle(obj, filepath):
    with bz2.open(filepath, 'wb', compresslevel=9) as f:
        pickle_.dump(obj, f, -1)

def unpickle(filepath):
    with bz2.open(filepath, 'rb', compresslevel=9) as f:
        return pickle_.load(f)

def _save_cache(folder, lastmodif_hash):
    fpath = join(folder, '.folder_hash')
    with open(fpath, 'w') as f:
        f.write(lastmodif_hash)

def _get_file_list(folder):
    file_list = []
    for (dir_, _, files) in os.walk(folder):
        if dir_ == folder:
            continue
        for f in files:
            fpath = join(dir_, f)
            if fpath.endswith('pkl') and os.path.basename(fpath) != 'all.pkl':
                file_list.append(fpath)
    return file_list

def _merge(file_list):
    pbar = report.ProgressBar(len(file_list))
    out = dict()
    for (i, fpath) in enumerate(file_list):
        d = unpickle(fpath)
        if isinstance(d, collections.Iterable):
            out.update(d)
        else:
            key = os.path.basename(fpath).split('.')[0]
            out[int(key)] = d
        pbar.update(i+1)
    pbar.finish()
    return out

def pickle_merge(folder):
    """Merges pickle files from the specified folder and save it to `all.pkl`.
    """
    file_list = _get_file_list(folder)

    if len(file_list) == 0:
        print('There is nothing to merge because no file'+
              ' has been found in %s.' % folder)
        return

    with report.BeginEnd('Computing hashes'):
        ha = path.folder_hash(folder, ['all.pkl', '.folder_hash'])

    subfolders = [d for d in os.listdir(folder) if isdir(join(folder, d))]

    with path.temp_folder() as tf:
        for sf in subfolders:
            path.make_sure_path_exists(join(tf, sf))
            path.cp(join(folder, sf), join(tf, sf))
        file_list = _get_file_list(tf)

        with report.BeginEnd('Merging pickles'):
            out = _merge(file_list)

    with report.BeginEnd('Storing pickles'):
        pickle(out, join(folder, 'all.pkl'))
    _save_cache(folder, ha)

    return out
