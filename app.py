from logging import debug
from flask import Flask,jsonify,request,render_template,redirect,url_for
from flask_socketio import SocketIO,join_room

app=Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


users=[
    {'id':2,'name':'Anne','age':20},
    {'id':1,'name':'Cathy','age':21},
    {'id':3,'name':'Bill','age':19}
]

# @app.route('/hello')
# def hello():
#     return "Hello World "
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    username=request.args.get('username')
    roomNo=request.args.get('roomNo')
    if username and roomNo:
        return render_template('chat.html',username=username,roomNo=roomNo)
    else:
        return render_template(url_for('index'))

@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("%s has joined room %s",data['username'],data['roomNo'])
    join_room(data['username'])
    socketio.emit('Join_room_announcement',data)


@socketio.on('send')
def handle_send_msg(data):
    print(data)
    app.logger.info("%s has send msg %s from %s",data['username'],data['message'],data['roomNo'])
    socketio.emit('receive',data,)

@app.route('/users')
def getUsers():
    print(users)
    return jsonify(users)

@app.route('/users/<id>')
def getUser(id):
    # result = [u for u in users if str(u['id'])==id]
    result=list(filter(lambda u: str(u['id'])==id,users))
    return jsonify(result)



if __name__=="__main__":
    socketio.run(app,debug=True)

#####################################
###### Before Adding SocketIO #######
#####################################

# from flask import Flask,jsonify,request

# app=Flask(__name__)

# users=[
#     {'id':2,'name':'Anne','age':20},
#     {'id':1,'name':'Cathy','age':21},
#     {'id':3,'name':'Bill','age':19}
# ]

# # @app.route('/hello')
# # def hello():
# #     return "Hello World "
# @app.route('/')
# def index():
#     #TODO
#     return app.send_static_file('index.html')

# @app.route('/users')
# def getUsers():
#     print(users)
#     return jsonify(users)

# @app.route('/users/<id>')
# def getUser(id):
#     # result = [u for u in users if str(u['id'])==id]
#     result=list(filter(lambda u: str(u['id'])==id,users))
#     return jsonify(result)



# if __name__=="__main__":
#     app.run()