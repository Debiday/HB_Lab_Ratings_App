"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Open homepage."""

    return render_template('homepage.html')


@app.route('/movies')
def movies():
    """Show all movies"""

    movies = crud.get_movies()

    return render_template('all_movies.html', movies=movies)


@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """Show details on a particular movie."""
    movie = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie=movie)


@app.route('/users')
def users():
    """Show all users"""

    users = crud.get_users()

    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def show_user(user_id):
    """show details of user email"""

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)

@app.route('/users', methods = ["POST"])
def register_user():
    """Create a new user."""
    
    #get email and password from hompage.html
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    
    if user:
        flash('Email is already in use. Cannot create an account. Try again')
        
    else: 
        crud.create_user(email, password)
        flash('Account created! Please log in.')

    return redirect('/')


@app.route('/login', methods = ['POST'])
def submit_login_form():
    """Submits the login form."""

    user = crud.get_user_by_email(request.form['email'])

    password = request.form['password']

    if user == None:
        flash('''An account for this email doesn't exist yet. 
                Please create a new account''')
    elif password != user.password:
        flash('Wrong password. Please try again.')
    else:
        flash('Logged in!')
        session['user-id'] = user.user_id

    return redirect('/')


    # # get email from you form data
    # user_email = request.form.get('email')
    # user_password = request.form.get('password')

    # user_login = crud.get_user_by_email('user_email')
    # users_login = crud.get_users()

    # if user_login in users_login:
    #     flash("Logged in!")
    # else:
    #     flash("Login Failed.")
 
    # return redirect('/')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
