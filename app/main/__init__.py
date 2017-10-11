# -*- coding: utf-8 -*-
from flask import Blueprint

from .forms import NameForm
from ..models import Permission

main = Blueprint('main', __name__)

from . import view

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)






