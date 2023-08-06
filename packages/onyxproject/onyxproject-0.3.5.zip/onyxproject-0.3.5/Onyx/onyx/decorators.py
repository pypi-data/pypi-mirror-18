from flask import request , redirect , url_for , flash , g
from functools import wraps

def admin_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if g.user.admin == 0:
      return redirect(url_for('core.index'))
    return f(*args, **kwargs)
  return decorated