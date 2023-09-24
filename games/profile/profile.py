from flask import Blueprint, render_template, session, redirect, url_for
import games.profile.services as services

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/profile')
def profile():
    username = session.get('username')
    if not username:
        return redirect(url_for('auth_bp.login'))
    
    user_data = services.get_user_data(username)
    if not user_data:
        # Handle the case where user data is not found
        return "User data not found", 404
    
    return render_template('profile.html', user=user_data)
