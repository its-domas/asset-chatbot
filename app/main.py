from flask import Flask, render_template, request, jsonify, session
#from app.config import Config
from chatbot_logic import conversational_rag_chain
import uuid
import os

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
    #app.config.from_object(Config)

    @app.route('/')
    def index():
        if 'session_id' in session:
            session.clear()  # Clear existing session data
        new_session_id = str(uuid.uuid4())
        session['session_id'] = new_session_id
        
        return render_template('index.html')

    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': 'No message provided.'}), 400

        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())

        session_id = session['session_id']
        
        try:
            response = conversational_rag_chain.invoke(
            {"input": user_message},
            {"configurable": {"session_id": session_id}}
            )
            answer = response['answer']

            return jsonify({'response': answer}), 200
        except Exception as e:
            app.logger.error(f"Error processing message: {e}")
            return jsonify({'error': 'An error occurred while processing your request.'}), 500
    


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)
