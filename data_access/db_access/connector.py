
from assistments_workbench.config_reader import config
import sqlsoup

username = config.get('postgres', 'username')
password = config.get('postgres', 'password')
db_url = config.get('postgres', 'db_url')
port = config.get('postgres', 'port')


db_str = 'postgresql://%s:%s@%s:%s/assistment_production' % \
    (username, password, db_url, port)

db = sqlsoup.SQLSoup(db_str)
session = db.session
