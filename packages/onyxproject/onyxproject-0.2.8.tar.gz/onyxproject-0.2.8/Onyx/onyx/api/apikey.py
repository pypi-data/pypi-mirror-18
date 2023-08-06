from flask import request, redirect , url_for
from functools import wraps


def require_appkey(view_function):
	@wraps(view_function)
	def decorated_function(*args, **kwargs):
		if request.args.get('key') and request.args.get('key') == 'APPKEY_HERE':
			return view_function(*args, **kwargs)
		else:
			return redirect(url_for('core.index'))
		return decorated_function
