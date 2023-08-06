#!/usr/bin/python3.5

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import create_app, db
from models import Bank

# from migrate3 import Migrate,COMMANDS

#
# if os.path.exists('.env'):
#     print('Importing environment from .env...')
#     for line in open('.env'):
#         var = line.strip().split('=')
#         if len(var) == 2:
#             os.environ[var[0]] = var[1]

# app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
	return dict(app=app, db=db, Bank=Bank)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


# @manager.command
# def profile(length=25, profile_dir=None):
#     """Start the application under the code profiler."""
#     from werkzeug.contrib.profiler import ProfilerMiddleware
#     app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length], profile_dir=app.config['PROJECT_DIR'])
#     app.run()
#
#

@manager.command
def deploy():
	"""Run deployment tasks."""
	from flask_migrate import upgrade
	from models import Bank

	# migrate database to latest revision
	upgrade()

	# create user roles
	db.create_all();
	Bank.generate_fake()


# @manager.command
# def selenium_test():
# 	"""Run selenium to test"""
# 	test = test_selenium.SeleniumTestCase(app=app)
# 	if test:
# 		try:
# 			test.setUpClass()
# 			test.get_banks()
# 			test.tearDownClass()
# 		except:
# 			test.setUp()
# 	return



if __name__ == '__main__':
	manager.run()
