
from assistments_workbench.config_reader import config
import sqlsoup

username = config.get('postgres', 'username')
password = config.get('postgres', 'password')
db_url = config.get('postgres', 'db_url')


db_str = 'postgresql://%s:%s@%s/assistment_production' % \
    (username, password, db_url)

db = sqlsoup.SQLSoup(db_str)
session = db.session
