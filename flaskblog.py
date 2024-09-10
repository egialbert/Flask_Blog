from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '620819eaca9f61ef6c9ba9d8df4c0903'


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

