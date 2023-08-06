"""__author__ = 'Zrush Zhang <mrzhzr2004@sina.com>'"""

from flask import Blueprint

main = Blueprint('main', __name__)

from . import view
