from flask import Flask, render_template, request, redirect, url_for, session
import wikipedia

app = Flask(__name__)
# Set the secret key. Keep this really secret:
app.secret_key = 'IT@JCUA0Zr98j/3yXa R~XHH!jmN]LWX/,?RT'


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        session['search_term'] = request.form['search']
        return redirect(url_for('results'))
    return render_template("search.html")


@app.route('/results')
def results():
    search_term = session.get('search_term', '')
    page = get_page(search_term)
    return render_template("results.html", page=page)


def get_page(search_term):
    try:
        page = wikipedia.page(search_term)
    except wikipedia.exceptions.PageError:
        page = wikipedia.page(wikipedia.random())
    except wikipedia.exceptions.DisambiguationError as e:
        page_titles = e.options
        if len(page_titles) > 1:
            page = wikipedia.page(page_titles[1])
        else:
            page = wikipedia.page(wikipedia.random())
    return page


if __name__ == '__main__':
    app.run(debug=True)
