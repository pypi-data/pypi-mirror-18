from models import Bank


def get_bank_list():
	"""
    :return a list including all banks

    :param
    :return: a list of banks
    """

	# if not city and not name and not address:
	banks = Bank.query.all()

	return banks
