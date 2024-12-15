from flask import Flask, render_template, request, jsonify
import openai
import os
from config import Config
import logging
import time

# Initialize Flask app
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object(Config)

# Set the OpenAI API key from the config
openai.api_key = app.config["OPENAI_API_KEY"]

# Set up logging
logging.basicConfig(level=logging.INFO)  # Set to ERROR for less verbosity
logger = logging.getLogger(__name__)

@app.route("/")
def home():
    """ Render the homepage with the query input form """
    return render_template("index.html")  # Serve the HTML page

@app.route("/ask", methods=["POST"])
def ask_question():
    """ Handle the user's question and communicate with OpenAI API """
    user_query = request.form["query"]

    retries = 3  # Set the number of retry attempts
    for attempt in range(retries):
        try:
            logger.info(f"User query: {user_query}")

            # Send the user query to OpenAI's API and fetch the response
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Choose GPT-4 model or gpt-3.5-turbo
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_query}
                ],
                max_tokens=150  # Optional: Limit the response length
            )

            # Extract and clean the response text
            model_response = response.choices[0].message["content"].strip()

            # Return the response as JSON to the frontend
            return jsonify({"response": model_response})

        except openai.error.RateLimitError:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                return jsonify({"error": "API rate limit exceeded. Please try again later."})
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")  # Log error details
            return jsonify({"error": str(e)})

if __name__ == "__main__":
    # Run the app in development mode (debug=True allows automatic reloading of the app)
    app.run(debug=True)
