from app import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, LoginForm, PostForm
from app.models import User, Address, Post
from flask import Flask

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/posts')
def posts():
    return 'These are the posts'

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    print("FORM DATA:", form.data)
    if form.validate_on_submit():
        print('Form Submitted and Validated!')
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        confirm_pass = form.confirm_pass.data
        print(first_name, last_name, email, username, password, confirm_pass)
        check_user = User.query.filter( (User.username == username) | (User.email == email)).all()
        if check_user:
            flash('A user with that email already exists', 'danger')
            return redirect(url_for('signup'))
        new_user = User(
            first_name=first_name, 
            last_name=last_name, 
            email=email, 
            username=username, 
            password=password
            )
        flash(f'Thank you {new_user.first_name} {new_user.last_name} for signing up!', 'success')
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Form validated!')
        username = form.username.data
        password = form.password.data
        print(username, password)
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f"{user.username} is now logged in", "warning")
            return redirect(url_for('index'))
        else:
            flash("Incorrect username and/or password", "danger")
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", "warning")
    return redirect(url_for('index'))

@app.route('/create-new-address', methods=['GET', 'POST'])
@login_required
def create_new_address():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data 
        address = form.address.data
        phone_number = form.phone_number.data
        new_address = Post(title=title, address=address, phone_number=phone_number, user_id=current_user.id)
        # print(address, phone_number, current_user)
        flash(f"{new_address.address} has been created", "success")
        return redirect(url_for('index'))

    return render_template('create.html', form=form)

@app.route('/posts/<int:post_id>')
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash(f"A post with id {post_id} does not exist", "danger")
        return redirect(url_for('index'))
    return render_template('post.html', post=post)

@app.route('/posts/<post_id>/edit', methods=["GET, POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash(f"A post with id {post_id} does not exist", "danger")
        return redirect(url_for('index'))
    if post.author != current_user:
        flash("You do not have permission to edit this post", "danger")
        return redirect(url_for('index'))
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        address = form.address.data
        phone_number = form.phone_number.data
        post.update(title, address, phone_number)
        flash(f"{post.title} has been updated!", "success")
        return redirect(url_for('get_post', post_id=post.id))
    if request.method == 'GET':
        form.title.data = post.title
        form.address.data = post.body
    return render_template('edit_post.html', post=post, form=form)

@app.route('/posts/<post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash(f"A post with id {post_id} does not exist", "danger")
        return redirect(url_for('index'))
    if post.author != current_user:
        flash("You do not have permission to delete this post", "danger")
        return redirect(url_for('index'))
    post.delete()
    flash(f"{post.title} has been deleted", "info")
    return redirect(url_for('index'))
