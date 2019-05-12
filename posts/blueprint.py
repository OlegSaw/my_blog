from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify
from .forms import PostForm
from models import Post, Tag, Comment, User, Role, roles_users
from app import db
from flask_security import login_required, current_user


posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():
    if current_user.has_role('admin') or current_user.has_role('moder'):
        if request.method == 'POST':
            # title = request.form['title']
            print(request.form)
            title = request.form['title']
            body = request.form['body']
            tags = request.form['tags']
            print("ТЭГЖ", len(tags))
            if len(tags) > 0:
                tags = tags.split(', ')
                print("RAZMER:", len(tags))
            try:
                post = Post(title=title, body=body)
                db.session.add(post)
                db.session.commit()
            except:
                print("Error")
            try:
                for tag in tags:
                    new_tag = Tag(post_id=post.id, name=tag)
                    db.session.add(new_tag)
                    db.session.commit()

            # db.session.add(post)
            # db.session.commit()
            except:
                print("Error")
            return redirect(url_for('posts.index'))

        form = PostForm()
        return render_template('posts/create_post.html', form=form)
    else:
        return redirect(url_for("index"))

@posts.route('/<slug>/edit/', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    if current_user.has_role('admin') or current_user.has_role('moder'):
        post = Post.query.filter(Post.slug == slug).first_or_404()
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            tags = request.form['tags']
            if tags is not None:
                tags = tags.strip().split(',')
            current_tags = [str(tag) for tag in Tag.query.filter(Tag.post_id == post.id).all()]
            new_tags = []
            old_tags = []
            for tag in current_tags:
                if tag not in tags:
                    old_tags.append(tag)
            post.title = title
            post.body = body
            db.session.commit()
            for tag in tags:
                if len(tag) == 0:
                    continue
                if tag.strip() not in current_tags:
                    new_tags.append(tag.strip())
            for old_tag in old_tags:
                print(old_tag)
                Tag.query.filter(Tag.name == old_tag, Tag.post_id == post.id).delete()
                db.session.commit()
            if new_tags:
                for new_tag in new_tags:
                    new_tag = Tag(post_id=post.id, name=new_tag)
                    db.session.add(new_tag)
                    db.session.commit()
            return redirect(url_for("posts.post_detail", slug=post.slug))

        # form = PostForm(obj=post)
        # for foa in form:
        # 	print(foa)
        tags = Tag.query.filter(Tag.post_id == post.id).all()
        # print(type(tags))
        tags = ','.join(str(tag) for tag in tags)
        return render_template('posts/edit_post.html', post=post, tags=tags)
    else:
        return redirect(url_for("index"))

@posts.route('/<slug>/comment/', methods=['GET', 'POST'])
@login_required
def create_comment(slug):
    if request.method == "GET":
    # if request.is_xhr:
        # roles_users = Role.query.filter_by(id=current_user.id).first()
        # return jsonify('posts/create_comment.html', slug=slug)
        return render_template('posts/create_comment.html', slug=slug)
    if request.method == 'POST' or request.form['content']:
        post = Post.query.filter(Post.slug == slug).first_or_404()
        print("i am here")
        if post:
            comment = Comment(body=request.form['body'], post_id=post.id, user_id=current_user.id, role_for_comment=str(current_user.roles))
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
    # posts = Post.query.join(Tag).filter(Post.id == Tag.post_id)
    else:
        posts = Post.query.order_by(Post.created.desc())
    pages = posts.paginate(page=page, per_page=6)
    return render_template('posts/index.html', posts=posts, pages=pages)


@posts.route('<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    tags = Tag.query.filter(Tag.post_id == post.id).all()
    # print(len(tags))
    # if tags is not None:
    # for tag in tags:
        # print(tag.slug, tag.name)
        # print(post.tags)
    # tags = post.tags
    comment_info = db.session.query(Comment, User).filter(Comment.post_id == post.id, Comment.user_id == User.id).all()
    # print(comment_info)
    return render_template('posts/post_detail.html', post=post, tags=tags, comments=comment_info)
    # else:
    #     for tag in tags:
    #         print(tag.slug, tag.name)
    #         # tags = post.tags
    #     comment_info = db.session.query(Comment, User).filter(Comment.post_id == post.id,
    #                                                           Comment.user_id == User.id).all()
    #     print(comment_info)
    #     return render_template('posts/post_detail.html', post=post, tags="Null", comments=comment_info)
#
# def create_comment(slug):
#     if request.method == 'GET':
#         # roles_users = Role.query.filter_by(id=current_user.id).first()
#         return render_template('posts/post_detail.html', slug=slug)
#     if request.method == 'POST':
#         post = Post.query.filter(Post.slug == slug).first_or_404()
#         print('qweqwee111qwe', current_user.roles)
#         print('qweqwee111qwe')
#
#         # roles_user = db.session.query(User, Role).filter(User.role_id == current_user.id).all()
#         # User.query.join(User.roles).filter(User.id == current_user.id).all()
#         # Seroles_users.query.filter_by(id=current_user.id).all()
#         # comment = Comment.query.filter_by(role_id=1).all()
#         print('eeee', )
#         if post:
#             comment = Comment(body=request.form['body'], post_id=post.id, user_id=current_user.id,
#                               role_for_comment=str(current_user.roles))
#             db.session.add(comment)
#             db.session.commit()
#             return redirect(url_for('posts.post_detail', slug=slug))
#         else:
#             return '400', 400


@posts.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    print(tag)
    posts = Post.query.join(Tag).filter(Post.id == Tag.post_id, Tag.slug == slug)
    print(posts)
    # posts = tag.posts
    return render_template('posts/tag_detail.html', tag=tag, posts=posts)

