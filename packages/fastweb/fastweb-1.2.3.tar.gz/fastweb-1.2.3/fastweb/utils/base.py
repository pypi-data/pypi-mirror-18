# coding:utf-8

import re
import uuid
import ConfigParser

def uniqueid(bit=64):
   """获取64位requesid"""

   return uuid.uuid1().int>>bit


class Base(object):

    @staticmethod
    def enum(**enums):
        return type('Enum',(),enums)

    @staticmethod
    def check_arguments(keys,essential_keys):
        keys = set(keys)
        essential_keys = set(essential_keys)
        
        if keys == essential_keys:
            return False

        if keys == essential_keys:
            return False

        if keys.issuperset(essential_keys):
            return True
        else:
            return False

    @staticmethod
    def isset(v):
        try:
            type(eval(v))

        except:
            print False
            return False
        else:
            print True
    
            return True
    @staticmethod
    def empty(s):
        return True if 0 == len(s) else False

    @staticmethod
    def md5(s):
        md = hashlib.md5()
        md.update(s)
        return md.hexdigest()

class Configer(object):

    def __init__(self,ini_path = ''):
        self.reset(ini_path)

    def reset(self,ini_path):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(ini_path)
        
        config_dict = {}
        
        for section in self.cf.sections():
            options_list = self.cf.items(section)

            config_dict[section] = {}

            for option_tuple in options_list:
                key = option_tuple[0]
                value = option_tuple[1]
                config_dict[section][key] = value

        self.config_dict = config_dict

    def get_components(self,component):
        components_dict = {}
        component_exp = r'(%s):(\w*)' % component

        exp = re.compile(component_exp)

        for section in self.cf.sections():
            match = exp.match(section)
            
            if match:
                components_dict[section] = {'component':match.group(1),'object':match.group(2)}
    
        return components_dict      

    @property
    def config(self):
            return self.config_dict
