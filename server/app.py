import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes (to allow requests from client)
CORS(app)

# Initialize OpenAI client with API key from environment
# Make sure to set OPENAI_API_KEY in your .env file
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    client = None
    print("Warning: Could not initialize OpenAI client. Please check your API key in .env file.")

@app.route('/chat', methods=['POST'])
def chat():
    if not client:
        return jsonify({"error": "OpenAI client is not initialized. Check server configuration."}), 500

    data = request.json
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful and friendly AI assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        # Provide a more generic error to the client, but log the real one
        return jsonify({"error": f"Failed to process request: {str(e)}"}), 500

if __name__ == '__main__':
    # Start the server on port 5000
    print("Starting chatbot server on http://localhost:5000")
    app.run(debug=True, port=5000)
