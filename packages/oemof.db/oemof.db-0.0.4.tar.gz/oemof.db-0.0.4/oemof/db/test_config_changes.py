import oemof.db as db

db.connection(config_file='asda')

db.connection(section='oedb', config_file='asd')

# cfg.load_config('config_misc')
db.cfg.load_config('/home/guido/rli_local/dingo/dingo/config/config_misc')

geo = db.cfg.get("geo", "srid")

print(geo)