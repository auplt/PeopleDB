import yaml


class ProjectConfig:
    """Класс считывает базовые настройки из файла config.yaml"""

    def __init__(self):
        with open('config.yaml') as f:
            config = yaml.safe_load(f)
            self.dbfilepath = config['dbfilepath']
            self.dbtableprefix = config['dbtableprefix']


if __name__ == "__main__":
    x = ProjectConfig()
    # print(x.dbfilepath)
