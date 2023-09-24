from flask import Blueprint, render_template, session, redirect, url_for
import games.profile.services as services
from games.authentication.authentication import login_required

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/profile')
@login_required
def profile():
    username = session.get('username')
    user_data = services.get_user_data(username)
    return render_template('profile.html', user=user_data)
