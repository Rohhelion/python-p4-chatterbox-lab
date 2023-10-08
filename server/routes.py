# server/routes.py

from flask import Blueprint, request, jsonify
from .models import db, Message

messages_bp = Blueprint('messages', __name__)

# GET all messages
@messages_bp.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at).all()
    message_list = [{"id": message.id, "body": message.body, "username": message.username, "created_at": message.created_at} for message in messages]
    return jsonify(message_list)

# POST a new message
@messages_bp.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({"message": "Message created successfully!"})

# PATCH/update a message by ID
@messages_bp.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({"error": "Message not found"}), 404
    data = request.get_json()
    message.body = data['body']
    db.session.commit()
    return jsonify({"message": "Message updated successfully!"})

# DELETE a message by ID
@messages_bp.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({"error": "Message not found"}), 404
    db.session.delete(message)
    db.session.commit()
    return jsonify({"message": "Message deleted successfully!"})
