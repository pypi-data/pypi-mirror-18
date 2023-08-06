# coding:utf8


class Configer(object):
    """配置文件类"""

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
