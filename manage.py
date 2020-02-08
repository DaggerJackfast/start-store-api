from flask_script import Manager, prompt_bool
from flask_migrate import MigrateCommand
from app import socketio, app, db

print(app.config['SQLALCHEMY_DATABASE_URI'])
manager = Manager(app, with_default_commands=False)

manager.add_command('db', MigrateCommand)
@manager.command
def hello():
    "Test command"
    print('hello')


@manager.command
def runserver():
    "Run server"
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)


@manager.command
def drop():
    "Drops database tables"
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()


@manager.command
def create():
    "Creates database tables from sqlalchemy models"
    db.create_all()


@manager.command
def recreate(default_data=True, sample_data=False):
    "Recreates database tables (same as issuing 'drop' and then 'create')"
    drop()
    create()




if __name__ == "__main__":
    manager.run()
