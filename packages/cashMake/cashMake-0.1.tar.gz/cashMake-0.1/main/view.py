from flask import render_template, current_app, request, abort
from flask_sqlalchemy import get_debug_queries
from . import main


@main.route('/', methods=['GET'])
def index():
	# form = PostForm()
	# if current_user.can(Permission.WRITE_ARTICLES) and \
	#         form.validate_on_submit():
	#     post = Post(body=form.body.data,author=current_user._get_current_object())
	#     db.session.add(post)
	#     return redirect(url_for('.index'))
	# page = request.args.get('page', 1, type=int)
	# show_followed = False
	# if current_user.is_authenticated:
	#     show_followed = bool(request.cookies.get('show_followed', ''))
	# if show_followed:
	#     query = current_user.followed_posts
	# else:
	#     query = Post.query
	# pagination = query.order_by(Post.timestamp.desc()).paginate(
	#     page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
	#     error_out=False)
	# posts = pagination.items
	return render_template('operations/bank.html')


@main.route('/shutdown')
def server_shutdown():
	if not current_app.testing:
		abort(404)
	shutdown = request.environ.get('werkzeug.server.shutdown')
	if not shutdown:
		abort(500)
	shutdown()
	return 'Shutting down...'


@main.after_app_request
def after_request(response):
	for query in get_debug_queries():
		if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
			print("Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" % query.statement, query.parameter,
					query.duration, query.context)
	return response
