from datetime import datetime

from flask import jsonify, current_app


def get_version():
	"""
	This returns the version, that is displayed in the WebUI and
	self service portal.
	"""
	version = current_app.config.get('CASHMAKE_VERSION')
	return "CashMake {0!s}".format(version)


def send_result(obj, rid=1, total=0, status=False, details=None):
	"""
	sendResult - return an json result document

	:param total: the amount of dealing with data
	:param status: success for True, failed for false
	:param obj: simple result object like dict, sting or list
	:type obj: dict or list or string/unicode
	:param rid: id value, for future versions
	:type rid: int
	:param details: optional parameter, which allows to provide more detail
	:type  details: None or simple type like dict, list or string/unicode

	:return: json rendered sting result
	:rtype: string
	"""
	res = {
		"jsonrpc": "1.00",
		"total": total,
		"result": {
				"status": status,
				"value": obj
				},
		"version": get_version(),
		"id": rid,
		"time": datetime.utcnow()
		}

	if details is not None and len(details) > 0:
		res["detail"] = details

	return jsonify(res)
