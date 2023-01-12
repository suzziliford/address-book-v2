from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm
from app.models import User

@app.route('/')
def index():
    return render_template('index.html', name = 'Brian')

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
        check_user = User.query.filter( (User.email == email)).all()
        if check_user:
            flash('A user with that email already exists', 'danger')
            return redirect(url_for('signup'))
        new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        flash(f'Thank you {new_user.first_name} {new_user.last_name} for signing up!', 'success')
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)
