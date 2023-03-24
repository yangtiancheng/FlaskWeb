import functools
import logging

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

logger = logging.getLogger(__name__)

bp = Blueprint('auth',__name__, url_prefix='/auth')

@bp.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        db = get_db()
        error=None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not password2:
            error = 'Comfirm password is required.'
        elif password != password2:
            error = 'Password and confirm password don\'t match.'
        
        if error is None:
            try:
                db.execute(
                    "insert into user(username, password) values (?, ?)", (username,generate_password_hash(password)),
                    )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template('auth/register.j2')

@bp.route('/login', methods=('GET','POST'))
def login():
    logger.warning('Enter to Login!')
    if request.method == 'POST':
        logger.warning('Enter to Login - Post!')
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'select * from user where username=?;',(username,)
            ).fetchone()
        
        if user is None:
            error = "Incorrect Username."
        elif not check_password_hash(user['password'], password):
            error = "Incorrect Password."
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    else:
        logger.warning('Enter to Login - Get!')
    return render_template('auth/login.j2')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'select * from user where id = ?',(user_id,)
            ).fetchone()
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

