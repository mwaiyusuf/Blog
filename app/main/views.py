from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from .forms import PitchForm,CommentForm,UpdateProfile
from ..models import User,Blog,Comment
from .. import db,photos
import markdown2
from flask_login import login_required, current_user
import datetime
from ..requests import random_post


# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    # blogs =blogs.query.order_by(blog.date.desc()).all()
    # title = "My Blog -- Home"
    # pop = random_post()
    # quote = pop["quote"]
    # quote_author = pop ["author"]
    return render_template('index.html')


@main.route('/blogs/<category>')
def blogs_category(category):

    '''
    View function that returns blogs by category
    '''
    title = f'My Blog -- {category.upper()}'
    if category == "all":
        blogs = blogs.query.order_by(blog.time.desc())
    else:
        blogs = blog.query.filter_by(category=category).order_by(blog.time.desc()).all()

    return render_template('blogs.html',title = title,blogs = blogs)


@main.route('/<uname>/new/blog', methods=['GET','POST'])
@login_required
def new_blog(uname):
    form = blogForm()

    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    title_page = "My Blog -- Add New Post"

    if form.validate_on_submit():

        title=form.title.data
        content=form.content.data
        category=form.category.data
        date = datetime.datetime.now()
        time = str(date.time())
        time = time[0:5]
        date = str(date)
        date = date[0:10]
        blog = blog(title=title,
                      content=content,
                      category=category,
                      user=current_user,
                      date = date,
                      time = time)

        db.session.add(pitch)
        db.session.commit()

        return redirect(url_for('main.blogs_category',category = category))

    return render_template('new_blog.html', title=title_page, form=form)


@main.route("/<uname>/blog/<blog_id>/new/comment", methods = ["GET","POST"])
@login_required
def new_comment(uname,blog_id):
    user = User.query.filter_by(username = uname).first()
    blog = blog.query.filter_by(id = blog_id).first()

    form = CommentForm()
    title_page = "My Blog -- Comment Blog"

    if form.validate_on_submit():
        title = form.title.data
        comment = form.comment.data
        date = datetime.datetime.now()
        time = str(date.time())
        time = time[0:5]
        date = str(date)
        date = date[0:10]
        new_comment = Comment(post_comment = comment, user = user, blog = blog,time = time, date = date )

        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for("main.display_comments", blog_id=blog.id))
    return render_template("new_comment.html", title = title_page,form = form,blog = blog)


@main.route("/<blog_id>/comments")
@login_required
def display_comments(blog_id):
    # user = User.query.filter_by(username = current_user).first()
    pitch = blog.query.filter_by(id = blog_id).first()
    title = "My Blog -- Comments"
    comments = Comment.get_comments(blog_id)

    return render_template("display_comments.html", comments = comments,blog = blog,title = title)



@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)



@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
