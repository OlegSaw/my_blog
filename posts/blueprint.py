from flask import Blueprint
from flask import render_template, request, redirect, url_for
from .forms import PostForm
from models import Post, Tag, Comment, User, Role
from app import db
from flask_security import login_required, current_user

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():
	if request.method == 'POST':
		title = request.form['title']
		body = request.form['body']
		#tag = request.form['tag']

		try:
			post = Post(title=title, body=body)
			db.session.add(post)
			db.session.commit()
		except:
			print("Error")
		return redirect(url_for('posts.index'))

	form = PostForm()
	return render_template('posts/create_post.html', form=form)

@posts.route('/<slug>/edit/', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
	post = Post.query.filter(Post.slug == slug).first_or_404()
	if request.method == 'POST':
		form = PostForm(formdata=request.form, odj=post)
		form.populate_obj(post)
		db.session.commit()

		return redirect(url_for("posts.post_detail", slug=post.slug))

	form = PostForm(obj=post)
	return render_template('posts/edit_post.html', post=post, form=form)

@posts.route('/<slug>/comment/', methods=['GET', 'POST'])
@login_required
def create_comment(slug):
    if request.method == 'GET':
        return render_template('posts/create_comment.html', slug=slug)
    if request.method == 'POST':
        post = Post.query.filter(Post.slug == slug).first_or_404()
        if post:
            comment = Comment(body=request.form['body'], post_id= post.id, user_id=current_user.id)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('posts.post_detail', slug=slug))
        else:
            return '400', 400

@posts.route('/')
def index():

	q = request.args.get('q')

	page = request.args.get('page')

	if page and page.isdigit():
		page = int(page)
	else:
		page = 1

	print("qweqwe: ", page)

	if q:
		posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
	else:
		posts = Post.query.order_by(Post.created.desc())

	pages = posts.paginate(page=page, per_page=5)

	return render_template('posts/index.html', posts=posts, pages=pages)


@posts.route('<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    tags = post.tags
    comment_info = db.session.query(Comment, User).filter(Comment.post_id == post.id, Comment.user_id == User.id).all()
    return render_template('posts/post_detail.html', post=post, tags=tags, comments=comment_info)


@posts.route('/tag/<slug>')
def tag_detail(slug):
	tag = Tag.query.filter(Tag.slug == slug).first_or_404()
	print(tag)
	posts = tag.posts
	return render_template('posts/tag_detail.html', tag = tag, posts = posts)