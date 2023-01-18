

import os
import string
import secrets
import pickle
from flask import Flask, request, redirect, render_template


app = Flask(__name__)

if os.path.exists('links.pkl'):
    with open('links.pkl', 'rb') as file:
        links = pickle.load(file)
else:
    links = {}

chars = string.ascii_letters
length = 8

@app.route('/', methods=['GET', 'POST'])
def generate_link():
    if request.method == 'POST':
        link = request.form['input_link']
        is_custom_link = request.form['custom_link_box']
        if is_custom_link:
            custom_link = request.form['custom_link']
            short = custom_link
        else:
            short = ''.join(secrets.choice(chars) for i in range(length))
        if not link.startswith(("http://", "https://")):
            link = "http://" + link
        links[hash(short)] = link
        print(short)
        return link + '\\\\' + short
    return render_template('index.html')


@app.route('/<link>')
def main(link):
    if hash(link) in links:
        return redirect(links[hash(link)])
    else:
        return "Short link does not exists, are you sure you entered the right one?"


try:
    if __name__ == '__main__':
        app.run(port=8181, debug=True)
except KeyboardInterrupt:
    with open("links.pkl", "wb") as file:
        pickle.dump(links, file)
