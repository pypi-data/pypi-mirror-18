# -*- coding: utf-8 -*-
#
# http://www.baidu.com
# (c) Zrush Zhang
#
# 'date'    'username'  'user_email'
#
# This code is free software; you can redistribute it and/or
# modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
# License as published by the Free Software Foundation;
#
# This code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU AFFERO GENERAL PUBLIC LICENSE for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

__doc__ = """ This the api for dealing with bank information """

from flask import request
import lib.operations.bank
from lib.utils import send_result
from models import Bank
from . import operations


@operations.route('/bank', methods=['POST'])
def create_new_banks():
	"""
	Create a new bank information

	**Example request**:

	.. sourcecode:: http

	POST /bank
	city=
	name=
	address=

	Host: localhost
	Accept: application/json
	"""

	city = request.form.get('bankCity', '')
	name = request.form.get('bankName', '')
	address = request.form.get('bankAddress', '')
	info = dict(city=city, name=name, address=address)
	# print(info)
	bank = Bank(city, name, address)
	res = bank.save()
	# print('res=%d' % res)
	return send_result(info, res, status="True")


@operations.route('/bank', methods=['GET'])
def get_banks():
	"""
	get a new bank object and details

	**Example request**:

	..sourcecode:: http

	POST /bank
	city=
	name=
	address=
	Host: localhost
	Accept: application/json
	"""

	bank_list = []
	bank_obj = lib.operations.bank.get_bank_list()

	for obj in bank_obj:
		checkbox = "<div class='checkbox'>" \
		           "<label><input name='checkbox' type='checkbox' id='bankBox' value='{id}'></label>" \
		           "</div>".format(id=obj.id)
		btn_group = "<div class='btn-group'>" \
		    "<button type='button' id='bankAdd' class='btn btn-success btn-flat' onclick='loadModal(this,{idCol})'>" \
		            "<i class='fa fa-plus'></i>" \
		            "</button>" \
		            "<button type='button' id='bankDel' class='btn btn-danger btn-flat'><i class='fa fa-trash'></i>" \
		            "</button>" \
		            "<button type='button' id='bankRef' class='btn btn-warning btn-flat'><i class='fa fa-refresh'></i>" \
		            "</button>" \
		            "<button type='button' id='bankUpd' class='btn btn-info btn-flat' onclick='loadModal(this,{idCol})'>" \
		            "<i class='fa fa-reply'></i>" \
		            "</button></div>".format(idCol=obj.id)
		row = dict(checkbox=checkbox, id=obj.id, name=obj.name, city=obj.city, address=obj.address, options=btn_group)
		bank_list.append(row)

	return send_result(bank_list, status="True", total=len(bank_obj))


@operations.route('/bank', methods=['DELETE'])
def delete_banks():
	"""
	delete a bank information from bank store
	**Example request**:

	.. sourcecode:: http

	DELETE /bank
	id=

	Host: localhost
	Accept: application/json
	"""

	res = None
	request_str = "request url: {0}?{1}".format(request.url, request.get_data().decode('utf8'))
	# print("request url: %s" % request_str)
	req_param = request_str.split('?')[-1]
	for id_param in req_param.split('&'):
		id_value = id_param.split('=')[1]
		print("id=%s" % id_value)
		res = Bank.query.filter(Bank.id == id_value).delete()

	return send_result(obj="", status="True", rid=res)


@operations.route('/bank/<bank_id>', methods=['PUT'])
def update_banks(bank_id):
	"""
	delete a bank information from bank store
	**Example request**:

	.. sourcecode:: http
		DELETE /bank
		:param bank_id=
		Host: localhost
		Accept: application/json
	"""

	city = request.form.get('bankCity', '')
	name = request.form.get('bankName', '')
	address = request.form.get('bankAddress', '')

	info = dict(id=bank_id, city=city, name=name, address=address)
	print(info)
	bank = Bank.query.filter_by(id=bank_id).first()

	if bank:
		bank.name = name
		bank.city = city
		bank.address = address
		bank.update()

	print('res: %s, bank: %s' % (bank_id, bank))

	return send_result(obj=info, status="True", rid=bank_id)
