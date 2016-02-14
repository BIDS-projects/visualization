from flask import Blueprint, g, render_template


public = Blueprint('public', __name__)


@public.route('/')
def home():
    return render_template('index.html')
