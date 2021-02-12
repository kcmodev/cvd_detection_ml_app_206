from flask import Flask, render_template, request

app = Flask(__name__)

user = {'name': 'Steve'}


@app.route('/')
@app.route('/index')
def index():
    index_title = 'Home'
    return render_template('index.html', name=user['name'], title=index_title)


# @app.route('/about')
# def about():
#     about_title = 'About Me'
#     return render_template('about.html', name=user['name'], title=about_title)


@app.route('/data')
def dashboard():
    dashboard_title = 'Data'
    return render_template('data.html', name=user['name'], title=dashboard_title)

    # if request.method == 'POST':
    #     # form_data = request.form
    #     return render_template('data.html', name=user['name'], title=dashboard_title)
    # else:
    #     return render_template('data.html', name=user['name'], title=dashboard_title)


if __name__ == '__main__':
    app.run(debug=True)
