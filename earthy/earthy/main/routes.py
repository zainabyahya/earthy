from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from matplotlib.pyplot import title
from earthy.models import Post


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    return render_template("home.html", user=current_user, title='Home')


@main.route("/community")
@login_required
def community():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_created.desc()).paginate(page=page, per_page=5)
    return render_template('community.html', posts=posts, user=current_user, title='Community')

@main.route('/FAQ')
def FAQ():
    return render_template("FAQ.html", user=current_user, title='FAQ')

@main.route('/recycle')
def recycle():
    return render_template("recycle.html", user=current_user, title='Recycle')

@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
