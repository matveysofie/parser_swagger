from configparser import ConfigParser
import configparser

from common.dir_config import PROFILEPATH


class HandleConfig(object):

    def __init__(self, file_path, encoding="utf-8"):
        self.file_path = file_path
        self.conf = configparser.ConfigParser()
        self.encoding = encoding
        self.conf.read(self.file_path, encoding=self.encoding)

    def get_value(self, section, option):
        return self.conf.get(section, option, raw=True)

    def get_boolean(self, section, option):
        return self.conf.getboolean(section, option)

    def get_int(self, section, option):
        return self.conf.getint(section, option)

    def get_float(self, section, option):
        return self.conf.getfloat(section, option)

    def set_section_value(self, section, option, value):
        if not self.conf.has_section(section):
            self.conf.add_section(section)
            self.conf.set(section, option, value)
            self.conf.write(open(self.file_path, "w"))
        else:
            self.conf.set(section, option, value)
            self.conf.write(open(self.file_path, "w"))

    def remove_section(self, section, option):
        if section in self.conf.sections():
            self.remove_option(section, option)
            self.conf.remove_section(section)
            self.conf.write(open(self.file_path, "r+"))
        else:
            print("{} not in ！".format(section))

    def remove_option(self, section, option):
        print(self.conf.sections())
        if section in self.conf.sections():
            if option in self.conf.options(section):
                self.conf.remove_option(section, option)
                self.conf.write(open(self.file_path, "r+"))
            else:
                print("{}not in ！".format(option))
        else:
            print("{}not in ！".format(section))


class SimplerConfig(ConfigParser):
    def __init__(self, config_file, encoding="utf-8"):
        super().__init__()
        self.config_file = config_file
        self.encoding = encoding
        self.read(self.config_file, encoding=self.encoding)


conf = HandleConfig(file_path=PROFILEPATH)

if __name__ == '__main__':
    conf = SimplerConfig(config_file=PROFILEPATH)
    text = conf.get("logger", "level")
    print(text)
