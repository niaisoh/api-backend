import yaml
from yaml.loader import SafeLoader

# Open the file and load the file
with open('settings.yml') as f:
    cfg = yaml.load(f, Loader=SafeLoader)

# db mongo
database = cfg.get('database')

rabbitmq = cfg.get('rabbitmq')
