from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from app.index import start_app
from app.db import db

server = start_app()

migrate = Migrate(server, db)
manager = Manager(server)

manager.add_command('run', Server())
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
