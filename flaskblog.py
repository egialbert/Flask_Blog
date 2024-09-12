from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import RegistrationForm, LoginForm

app = Flask(__name__)



app.config['SECRET_KEY'] = '620819eaca9f61ef6c9ba9d8df4c0903'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app) # creating database instance

with app.app_context():
    db.create_all()

# Models
# User Model 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False )
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    """Users will author a post: This is a one to many relationship, 
    because one user can have multiple posts and a post can have only one author
    -> post attribute has a relationship with the Post model
    -> backref is similar to adding another Column to the Post model.
    It allows us to use author to get who created the post.
    -> the lazy augurment, defines when SQLAlchemy loads the data from the database.
    True means that SQLAlchemy will load the data as neccessary in one go
    """
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"



posts = [

    {

        'author':'Albert Egi',
        'title':'Blog post 1',
        'content':'First post content',
        'date_posted':'April 20, 2025'
    },
    {

        'author':'Ebube Nwandioku',
        'title':'Blog post 2',
        'content':'Second post content',
        'date_posted':'April 21, 2025'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts = posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm() # Create an instance of registration form that will be sent to our application. pass the instance into a template
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if Registration is successful redirect by the home function to the home page.
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm() # Create an instance of login form that will be sent to our application. pass the instance into a template
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('you have been logged in!', 'success')
            return redirect(url_for('home')) 
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

