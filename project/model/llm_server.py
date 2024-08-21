from flask import Flask, request, jsonify
import os
import google.auth
import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession

app = Flask(__name__)

# Google Cloud 프로젝트 설정
PROJECT_ID = os.getenv('PROJECT_ID')
LOCATION = os.getenv('LOCATION', 'asia-northeast3')

# Google Cloud 인증 설정
credentials, project = google.auth.default()

# Vertex AI 초기화
vertexai.init(project=PROJECT_ID, location=LOCATION)
model = GenerativeModel(model_name="gemini-1.0-pro-002")
chat = model.start_chat(response_validation=False)

def get_chat_response(chat: ChatSession, prompt: str) -> str:
    text_response = []
    responses = chat.send_message(prompt, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    return "".join(text_response)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        app.logger.debug(f"Received data: {data}")
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        response_text = get_chat_response(chat, prompt)
        app.logger.debug(f"Generated response: {response_text}")
        return jsonify({'generated_text': response_text})
    except Exception as e:
        app.logger.error(f"Error during text generation: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
