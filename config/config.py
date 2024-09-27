from configparser import ConfigParser

def load_config(filename='./config/requirements.ini', section='login'):
    parser = ConfigParser()
    parser.read(filename)
    # get section
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config

def load_sql_config(filename='./config/requirements.ini', section='sql'):
    parser = ConfigParser()
    parser.read(filename)
    # get section
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return config