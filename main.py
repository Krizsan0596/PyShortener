

import os
import string
import secrets
import pickle
import hashlib
import atexit
from urllib.parse import urlsplit
from flask import Flask, request, redirect, render_template, flash, request


app = Flask(__name__)
chars = string.ascii_letters + string.digits + '-'
length = 8
format = 'utf-8'
app.secret_key = ''.join(secrets.choice(chars) for i in range(length))

def save_links():
    with open("links.pkl", "wb") as file:
        pickle.dump(links, file)
atexit.register(save_links)

if os.path.exists('links.pkl'):
    with open('links.pkl', 'rb') as file:
        links = pickle.load(file)
else:
    links = {}

def hash(input):
    hash_obj = hashlib.md5()
    hash_obj.update(bytes(input, format))
    hashed = hash_obj.hexdigest()
    return hashed

@app.route('/', methods=['GET', 'POST'])
def generate_link():
    if request.method == 'POST':
        link = request.form['input_link']
        if len(str(link)) > 2000:
            return "Url too long. Perhaps try a shorter one."
        try:
            is_custom_link = request.form['custom_link_box']
        except KeyError:
            is_custom_link = False
        if is_custom_link:
            custom_link = request.form['custom_link']
            if hash(custom_link) in links:
                return "Custom link already in use."
            else:
                short = custom_link
        else:
            short = ''.join(secrets.choice(chars) for i in range(length))
        parsed_link = urlsplit(link)
        if parsed_link.scheme == '':
            link = 'https://' + link
        elif parsed_link.scheme != 'http' and parsed_link.scheme != 'https':
            return 'Invalid link. Only \'http(s)\' links are supported.'
        links[hash(short)] = link
        print(short)
        return link + '\\\\ Your short link is: ' + short
    return render_template('index.html')


@app.route('/<link>')
def main(link):
    if hash(link) in links:
        return redirect(links[hash(link)])
    else:
        return "Short link does not exists, are you sure you entered the right one?"


if __name__ == '__main__':
    app.run(port=8181, debug=True)
