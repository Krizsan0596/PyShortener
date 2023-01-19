

import os
import string
import secrets
import pickle
import hashlib
from flask import Flask, request, redirect, render_template, flash, request


app = Flask(__name__)
chars = string.ascii_letters + string.digits + '-'
length = 8


if os.path.exists('links.pkl'):
    with open('links.pkl', 'rb') as file:
        links = pickle.load(file)
else:
    links = {}

def hash(input):
    hash_obj = hashlib.md5()
    hash_obj.update(bytes(input))
    hashed = hash_obj.hexdigest()
    return hashed

@app.route('/', methods=['GET', 'POST'])
def generate_link():
    if request.method == 'POST':
        link = request.form['input_link']
        if len(str(link)) > 2000:
            flash("Url too long. Perhaps try a shorter one.")
            return redirect(request.url)
        is_custom_link = request.form['custom_link_box']
        if is_custom_link:
            custom_link = request.form['custom_link']
            if hash(custom_link) in links:
                flash("Custom link already in use.")
                return redirect(request.url)
            else:
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
