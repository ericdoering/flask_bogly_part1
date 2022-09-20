"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = connect_db(app)
app.secret_key = "password8989$"

@app.route("/")
def list_users():
    """List all users that have setup an account"""
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/users/<user_id>", methods=['GET', 'POST'])
def get_user_by_id(user_id):
    """List all users that have setup an account"""
    if request.method == 'POST':
        print("THIS WORKED")
        obj = User.query.filter_by(user_id).one()
        db.delete(obj)
        db.commit()
        return render_template("users.html", user=user)
    else:
        user = User.query.get(user_id)
        return render_template("user_profile.html", user=user)


@app.route("/users/new", methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        print(form_data.get('first_name'))
        # # Insert user
        # new_user = User(first_name=form_data.get('first_name'), last_name=form_data.get('last_name'), image_url=form_data.get('image_url'))
        new_user = User(
        first_name=request.form['first-name'],
        last_name=request.form['last-name'],
        image_url=request.form['url'] or None)

        db.session.add(new_user)
        db.session.commit()
        return redirect('/')

    else:
        """List all users that have setup an account"""
        return render_template("add_user.html")


@app.route("/users/<user_id>/edit", methods=['GET', 'POST'])
def edit_user(user_id):
    """List all users that have setup an account"""
    user = User.query.get(user_id)
    return render_template("edit_user.html", user=user)


@app.route("/users/<user_id>/delete", methods=['POST'])
def delete_user(user_id):
    """List all users that have setup an account"""
    user = User.query.get(user_id)
    return True