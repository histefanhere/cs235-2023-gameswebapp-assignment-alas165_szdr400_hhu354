from flask import Blueprint, render_template, session, redirect, url_for
import games.profile.services as services

profile_bp = Blueprint('profile_bp', __name__)


@profile_bp.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('auth_bp.login'))
    
    username = session['username']
    user_data = services.get_user_data(username)
    
    return render_template('profile.html', user=user_data)
