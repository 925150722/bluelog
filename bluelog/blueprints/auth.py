
from flask import Blueprint, current_app


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('')
def login():
    pass


@auth_bp.route('')
def logout():
    pass
