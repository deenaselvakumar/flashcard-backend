from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import os

flashcards_bp = Blueprint('flashcards', __name__)
client = MongoClient(os.getenv("MONGO_URI"))
db = client.flashcarddb
collection = db.flashcards

@flashcards_bp.route('/api/flashcards', methods=['POST'])
def add_flashcard():
    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')
    if not question or not answer:
        return jsonify({"error": "Missing data"}), 400
    collection.insert_one({'question': question, 'answer': answer})
    return jsonify({"message": "Flashcard added"}), 201

@flashcards_bp.route('/api/flashcards', methods=['GET'])
def get_flashcards():
    flashcards = list(collection.find({}, {'_id': 0}))
    return jsonify(flashcards)
