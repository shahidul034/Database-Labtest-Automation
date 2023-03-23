from flask import Flask, render_template, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'my_secret_key'  # used to sign session cookies


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    # simulate a login attempt
    success = False
    if success:
        flash('Login successful!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Invalid username or password.', 'error')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
