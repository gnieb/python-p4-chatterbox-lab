from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = [m.to_dict() for m in Message.query.order_by('created_at').all()]
        return make_response(messages, 200)
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body=data['body'],
            username=data['username']
        )
        db.session.add(new_message)
        db.session.commit()
        return make_response(new_message.to_dict(), 201)

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    if request.method == 'PATCH':
        message = Message.query.filter_by(id=id).first()
        if not message:
             return make_response({"error":"message not found!"}, 404)
        
        data = request.get_json()
        for key in data.keys():
            setattr(message, key, data[key])
        db.session.add(message)
        db.session.commit()
        return make_response(message.to_dict(), 200)

    elif request.method =='DELETE':
        message = Message.query.filter_by(id=id).first()
        if not message:
            return make_response({"error":"message not found!"}, 404)
        db.session.delete(message)
        db.session.commit()
        return make_response({}, 202)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
