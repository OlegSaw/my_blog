class Configuration(object):
	DEBUG = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/test1'
	SECRET_KEY = 'secret'
	OAUTH_CREDENTIALS = {'facebook': {'id': '340405026758994', 'secret': '1abf33e965f3b6ed92e0b440fcdbf355'}}
###user settings
	SECURITY_PASSWORD_SALT = "salt"
	SECURITY_PASSWORD_HASH = "sha512_crypt"

###ouath
