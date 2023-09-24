from flask import Blueprint, render_template, session, redirect, url_for
import games.profile.services as services
from games.authentication.authentication import login_required

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/profile')
@login_required
def profile():
    print(services.get_short_wishlist())
    return render_template(
        'profile.html',
        short_wishlist=services.get_short_wishlist(),
        empty_wishlist=True if len(services.get_short_wishlist()) == 0 else False,
        )
