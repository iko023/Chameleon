from flask import Flask, render_template, request, session, jsonify
import random, uuid, time

app = Flask(__name__)
app.secret_key = 'your secret key'

viewers = {} # Store game participants
# store words
word_list = [
    'apple',
    'banana',
    'cherry',
    'dragon',
    'elephant'
]
# store game status, word, and chameleon
game = {
    'started' : False,
    'word' : None,
    'chameleon' : None
}

# register viewer or participant on erery status poll
def register_viewer():
  sid = session.get('sid')
  if not sid:
    sid = str(uuid.uuid4())
    session['sid'] = sid
  viewers[sid] = {
    'ip': request.remote_addr,
    'last_seen': time.time()
  }




@app.route('/')
def index():
    return render_template('index.html')