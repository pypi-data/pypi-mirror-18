# -*- coding:utf-8 -*-

import json
import yaml
from torcms.handlers.info_handler import InfoHandler


class MetaExtHander(InfoHandler):
    def extra_data(self, ext_dict, data_dic):
        if 'def_cat_uid' in data_dic and data_dic['def_cat_uid'].startswith('22'):
            ext_dict['ext_yaml'] =  data_dic['extra_yaml']
            ext_dict['def_json'] = json.dumps(yaml.load(ext_dict['ext_yaml']))
        elif 'def_cat_uid' in data_dic and data_dic['def_cat_uid'].startswith('24'):
            ext_dict['def_uid'] = data_dic['extra_uid']
        elif 'def_cat_uid' in data_dic and data_dic['def_cat_uid'].startswith('23'):
            ext_dict['def_uid'] = data_dic['extra_uid']
        else:
            pass
        return ext_dict
