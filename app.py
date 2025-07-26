from flask import Flask, render_template, request, session, jsonify
import random, uuid, time

app = Flask(__name__)
app.secret_key = 'your secret key'

viewers = {} # Store game participants
# store words
word_list = [
    "Jungle",
    "Beach",
    "Space",
    "Boat",
    "Office",
    "North Pole",
    "Hospital",
    "Cinema",
    "Forest",
    "Restaurant",
    "Mountains",
    "Zoo",
    "Farm",
    "Mall",
    "School",
    "Park",
    "Library",
    "Airport",
    "Stadium",
    "Castle",
    "Aquarium",
    "Museum",
    "Factory",
    "Concert Hall",
    "Subway Station",
    "Island",
    "Canyon",
    "Desert",
    "Pub",
    "Café",
    "Bank",
    "Grocery Store",
    "Hotel",
    "Warehouse",
    "Garage",
    "Laboratory",
    "Theater",
    "Playground",
    "Gym",
    "Salon",
    "Spa",
    "Bus",
    "Airplane",
    "Jurassic Park"
]

bag = []

# Bag of words to reduce redraw
def init_bag():
    global bag
    bag = list(set(word_list.copy()))
    random.shuffle(bag)

# Draw word and remove from bag
def draw_word():
    global bag
    if not bag:
        init_bag()
    return bag.pop()

# store game status, word, and chameleon
game = {
    'started' : False,
    'word' : None,
    'chameleon' : None,
    'words' : bag
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

# Registers player, removes inactive players, returns current playercount
@app.route('/status')
def status():
    register_viewer()
    cutoff = time.time() - 30
    for sid, info in list(viewers.items()):
        if info['last_seen'] < cutoff:
            viewers.pop(sid)
    # Only return count now
    return jsonify(count=len(viewers))

# Start game
@app.route('/start', methods=['POST'])
def start_game():
  if not game['started'] and viewers:
    sids = list(viewers.keys())
    game['chameleon'] = random.choice(sids)
    game['word'] = draw_word()
    game['started'] = True
  return jsonify({'status': 'ok'})

# Get game statet
@app.route('/game_state')
def game_state():
  register_viewer()
  sid = session.get('sid')
  payload = {
    'started': game['started'],
    'word': game['word'] if sid != game['chameleon'] else None,
    'you_chameleon': sid == game['chameleon']
  }
  return jsonify(payload)

# Quit/restart
@app.route('/reset', methods=['POST'])
def reset_game():
  game.update({'started': False, 'word': None, 'chameleon': None})
  return jsonify({'status': 'reset'})


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
  init_bag()
  app.run(debug=True)