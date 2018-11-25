from flask import Blueprint
from flask import render_template

from models import Post, Tag

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/')
def index():
	posts_q = Post.query.all()
	return render_template('posts/index.html', posts=posts_q)


@posts.route('<slug>')
def post_detail(slug):
	print(slug)
	post = Post.query.filter(Post.slug == slug).first()
	tags = post.tags
	return render_template('posts/post_detail.html', post=post, tags=tags)

@posts.route('/tag/<slug>')
def tag_detail(slug):
	tag = Tag.query.filter(Tag.slug == slug).first()
	print(tag)
	posts = tag.posts
	return render_template('posts/tag_detail.html', tag = tag, posts = posts)