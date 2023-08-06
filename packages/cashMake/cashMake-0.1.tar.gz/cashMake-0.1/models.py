# from datetime import datetime
# import hashlib
# from werkzeug.security import generate_password_hash, check_password_hash
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from markdown import markdown
# import bleach
# from flask import current_app, request, url_for
# from flask_login import UserMixin, AnonymousUserMixin
# from app.exceptions import ValidationError
# from . import db, login_manager

from app import db


#
#
# class Permission:
#     FOLLOW = 0x01
#     COMMENT = 0x02
#     WRITE_ARTICLES = 0x04
#     MODERATE_COMMENTS = 0x08
#     ADMINISTER = 0x80
#

class MethodsMixin(object):
	# This class mixes in some common Class table functions like delete and save

	def save(self):
		db.session.add(self)
		db.session.commit()
		return self.id

	def update(self):
		db.session.commit()
		return self.id

	def delete(self):
		ret = self.id
		db.session.delete(self)
		db.session.commit()
		return ret


class Bank(MethodsMixin, db.Model):
	"""
	store the bank information that is used in cash project

	"""
	__tablename__ = 'bank'
	id = db.Column(db.Integer, primary_key=True)
	city = db.Column(db.String(20), nullable=True)
	name = db.Column(db.String(20), nullable=True)
	address = db.Column(db.String(200))

	def __init__(self, bankCity, bankName, bankAddr, **kwargs):

		super(Bank, self).__init__(**kwargs)
		self.city = bankCity
		self.name = bankName
		self.address = bankAddr

	def get_bankname(self, bankAddr):

		"""
        return the bank full name through the address

        :param:  address
        :return: the name of bank
        :rtype: basestring
        """
		data=""

		bank = Bank.query.filter(Bank.address == bankAddr).first()
		if bank:
			data = bank.name

	def get_bankaddr(self, bankName):

		"""
        return the bank address through the bank name

        :param bankName:  the name of bank
        :return: the address of bank
        :rtype: basestring
        """
		data = ""

		bank = Bank.query.filter(Bank.address == bankName).first()
		if bank:
			data = bank.address

		return data

	@staticmethod
	def generate_fake():

		bank1 = Bank(bankName="zhangzian", bankCity="Beijing", bankAddr="YouAnmen")
		bank2 = Bank(bankName="zhangzian1", bankCity="Beijing2", bankAddr="YouAnmen2")

		db.session.add(bank1)
		db.session.add(bank2)
		db.session.commit()

		return
