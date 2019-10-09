#
# https://www.google.com/search?q=flask+migrate+create+table+columns&rlz=1C1CHBF_enUS820US820&oq=flask+migrate+create+table+columns&aqs=chrome..69i57.18237j0j7&sourceid=chrome&ie=UTF-8#kpvalbx=_r6qUXda8Ne2FggeK-KuwCg24
#
# drop table "Show";
# drop table "Artist";
# drop table "Venue";
# commit
#
# DELETE FROM public."Artist" WHERE id=nextval('"Artist_id_seq"'::regclass);
# DELETE FROM public."Show" WHERE id=nextval('"Show_id_seq"'::regclass);
# DELETE FROM public."Venue" WHERE id=nextval('"Venue_id_seq"'::regclass);
#

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import initAppDb

i = CgetAppDb()
app, db = i.getAppDb()

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()