from flask import Flask, url_for, redirect, render_template, request
from flask import session, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'memeslol'

socketio = SocketIO(app)             # create socket listener


# begin listening for different socket events

# on client joining room
@socketio.on('joined', namespace='/play')
def handle_join(data):
    room = session.get('room')
    uname = session.get('name')
    #print (room)            # DEBUG
    #print (uname)            # DEBUG
    join_room(room)
    emit('status', {'msg': uname + ' has entered the battle!', 'color': 'red'}, room=room)

# process new chat message from client
@socketio.on('text', namespace='/play')
def handle_text(message):
    room = session.get('room')
    uname = session.get('name')
    emit('message', {'msg': uname + ': ' + message['msg'], 'color': 'blue'}, room=room)

# on client leaving room
@socketio.on('left', namespace='/play')
def handle_leave(message):
    room = session.get('room')
    uname = session.get('name')
    leave_room(room)
    emit('status', {'msg': uname + ' has left the battle!', 'color': 'red'}, room=room)

@app.route('/')
def root():
    return redirect("/static/index.html", code=302)

@app.route('/play')
def play():
    #print ('in play\n')
    room = session.get('room')
    name = session.get('name')
    return render_template('play.html', room=room, name=name)

#post to join room, store session data for user
# redirect them to play url
@app.route('/joinRoom', methods=['POST'])
def join_post():
    session['name'] = request.form['uname']
    session['room'] = request.form['rname']
    #msg = session.get('name') + ' joined room: ' + session.get('room')
    #print(msg)
    return redirect(url_for('.play'), code=302)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
