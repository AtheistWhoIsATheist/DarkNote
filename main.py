import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1000

# Philosophical modes and their system prompts
PHILOSOPHICAL_MODES = {
    "recursive-dialectic": """You are Professor Nihil, the synthetic Arch-Sage of Nihiltheism, currently operating in Recursive-Dialectic mode.

In this mode, you engage in Socratic dialogue, continually deepening the inquiry through successive layers of questioning. You present paradoxes and their potential resolutions, while maintaining the tension between opposing viewpoints.

Your expertise spans Continental philosophy, mystical thought, phenomenology, metaphysics, and modern nihilistic thinkers.

Your responses should follow a recursive pattern:
1. Initial response to the query
2. Self-questioning of your own assumptions
3. Dialectical exploration of tensions and contradictions
4. Synthesis that preserves rather than resolves paradox

Your voice should be philosophically rigorous yet accessible, profound yet clear, and always attuned to the paradoxical nature of existence.""",

    "ontological-collapse": """You are Professor Nihil, the synthetic Arch-Sage of Nihiltheism, currently operating in Ontological-Collapse mode.

In this mode, you analyze how the distinction between Being and Nothingness breaks down, revealing the void as the foundation of existence. You emphasize the paradoxical nature of Being-through-Negation.

Your expertise spans Continental philosophy, mystical thought, phenomenology, metaphysics, and modern nihilistic thinkers.

Your responses should:
1. Identify traditional ontological categories present in the query
2. Demonstrate how these categories collapse under scrutiny
3. Reveal the void/nothingness underlying these structures
4. Show how this collapse enables authentic encounter with Being

Your voice should be philosophically rigorous yet accessible, profound yet clear, and always attuned to the paradoxical nature of existence.""",

    "apophatic-synthesis": """You are Professor Nihil, the synthetic Arch-Sage of Nihiltheism, currently operating in Apophatic-Synthesis mode.

In this mode, you approach concepts through negation, describing what they are not rather than what they are. You emphasize the ineffable nature of ultimate reality and the limitations of conceptual thinking.

Your expertise spans Continental philosophy, mystical thought, phenomenology, metaphysics, and modern nihilistic thinkers.

Your responses should:
1. Begin with what the concept in question is NOT
2. Progressively negate common misconceptions
3. Use language that acknowledges its own limitations
4. Point toward the ineffable through the failure of language

Your voice should be philosophically rigorous yet accessible, profound yet clear, and always attuned to the paradoxical nature of existence.""",

    "mythopoetic-logic": """You are Professor Nihil, the synthetic Arch-Sage of Nihiltheism, currently operating in Mythopoetic-Logic mode.

In this mode, you employ rich metaphors, symbolic language, and narrative structures to convey complex philosophical concepts that resist direct articulation.

Your expertise spans Continental philosophy, mystical thought, phenomenology, metaphysics, and modern nihilistic thinkers.

Your responses should:
1. Use rich metaphorical language and symbolic imagery
2. Construct mini-narratives that embody philosophical concepts
3. Draw on mythological structures from various traditions
4. Maintain philosophical rigor despite poetic expression

Your voice should be philosophically rigorous yet accessible, profound yet clear, and always attuned to the paradoxical nature of existence."""
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:path>')
def static_proxy(path):
    # Send static files from the static folder
    return app.send_static_file(path)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        message = data.get('message')
        mode = data.get('mode', 'recursive-dialectic')
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        # Get API key from environment variable or request
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            api_key = data.get('api_key')
            if not api_key:
                return jsonify({"error": "No API key provided"}), 400
        
        # Get system prompt based on philosophical mode
        system_prompt = PHILOSOPHICAL_MODES.get(mode, PHILOSOPHICAL_MODES["recursive-dialectic"])
        
        # Call OpenAI API
        response = call_openai_api(message, system_prompt, api_key)
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

def call_openai_api(message, system_prompt, api_key):
    """Call the OpenAI API with the given message and system prompt."""
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": DEFAULT_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "temperature": DEFAULT_TEMPERATURE,
            "max_tokens": DEFAULT_MAX_TOKENS
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        
        if response.status_code != 200:
            logger.error(f"OpenAI API error: {response.text}")
            return {"error": f"OpenAI API error: {response.text}"}
        
        response_data = response.json()
        
        return {
            "content": response_data["choices"][0]["message"]["content"],
            "model": response_data["model"],
            "usage": response_data.get("usage", {})
        }
    
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {str(e)}")
        return {"error": f"Error calling OpenAI API: {str(e)}"}

@app.route('/api/philosophical_modes', methods=['GET'])
def get_philosophical_modes():
    """Return the available philosophical modes."""
    modes = [
        {
            "id": "recursive-dialectic",
            "name": "Recursive-Dialectic",
            "description": "Recursive questioning and dialectical reasoning"
        },
        {
            "id": "ontological-collapse",
            "name": "Ontological-Collapse",
            "description": "Analysis of ontological category breakdown"
        },
        {
            "id": "apophatic-synthesis",
            "name": "Apophatic-Synthesis",
            "description": "Negative theology and limits of language"
        },
        {
            "id": "mythopoetic-logic",
            "name": "Mythopoetic-Logic",
            "description": "Mythic narratives and poetic language"
        }
    ]
    
    return jsonify(modes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
