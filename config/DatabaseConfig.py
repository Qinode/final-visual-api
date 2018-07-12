class BaseConfig:
    port = '8086'
    pass


class DevConfig(BaseConfig):
    url = '146.169.47.32'
    username = 'zq17'
    password = '*'
    database = 'winery_data'


class ProdConfig(BaseConfig):
    url = '146.169.46.131'
    username = 'readdata'
    passwrod = 'DATAREADER123'
    database = 'LocalizationData'
