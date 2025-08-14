# app.py

import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

# Load environment variables first
from dotenv import load_dotenv
import os

load_dotenv()  # must come first
API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1")

if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY is missing. Please check your .env file.")


print("Loaded API key:", API_KEY)

# Absolute project root (folder that contains this file)
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Explicit template/static folders using absolute paths
TEMPLATE_FOLDER = os.path.join(PROJECT_ROOT, "templates")
STATIC_FOLDER = os.path.join(PROJECT_ROOT, "static")

print("PROJECT_ROOT:", PROJECT_ROOT)
print("TEMPLATE_FOLDER:", TEMPLATE_FOLDER)
print("STATIC_FOLDER:", STATIC_FOLDER)
print("Templates exist:", os.path.isdir(TEMPLATE_FOLDER))
print("Files in templates:", os.listdir(TEMPLATE_FOLDER) if os.path.isdir(TEMPLATE_FOLDER) else "TEMPLATE FOLDER MISSING")

# Initialize Flask
app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)


@app.route("/")
def home():
    index_path = os.path.join(TEMPLATE_FOLDER, "index.html")
    if not os.path.isfile(index_path):
        return (
            "<h2>index.html not found in templates folder</h2>"
            f"<p>Expected at: {index_path}</p>"
            f"<pre>Templates dir listing: {os.listdir(TEMPLATE_FOLDER) if os.path.isdir(TEMPLATE_FOLDER) else 'missing'}</pre>"
        ), 500
    return render_template("index.html")


@app.route("/_debug/list")
def debug_list():
    tpl_list = os.listdir(TEMPLATE_FOLDER) if os.path.isdir(TEMPLATE_FOLDER) else []
    static_list = os.listdir(STATIC_FOLDER) if os.path.isdir(STATIC_FOLDER) else []
    return jsonify({
        "project_root": PROJECT_ROOT,
        "template_folder": TEMPLATE_FOLDER,
        "static_folder": STATIC_FOLDER,
        "templates": tpl_list,
        "static": static_list
    })


@app.errorhandler(Exception)
def handle_all_exceptions(e):
    code = e.code if isinstance(e, HTTPException) else 500
    return jsonify({
        "error": "internal_server_error" if code == 500 else "http_error",
        "detail": str(e)
    }), code


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        user_message = data.get("message", "").strip()
        if not user_message:
            return jsonify({"error": "message_required"}), 400

        if not API_KEY:
            return jsonify({"error": "api_key_missing"}), 500

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-4o-mini",  # OpenRouter-compatible model
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 1024
        }

        resp = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload, timeout=30)

        print("OPENROUTER status code:", resp.status_code)
        print("OPENROUTER response text:", resp.text)

        if resp.status_code != 200:
            return jsonify({
                "error": "upstream_api_error",
                "status_code": resp.status_code,
                "detail": resp.text
            }), resp.status_code

        resp_json = resp.json()
        choices = resp_json.get("choices", [])
        content = choices[0].get("message", {}).get("content") if choices else "No response from OpenRouter."

        return jsonify({"response": content})

    except requests.exceptions.RequestException as req_err:
        print("RequestException in /chat:", req_err)
        return jsonify({"error": "network_error", "detail": str(req_err)}), 502
    except Exception as e:
        print("Exception in /chat:", e)
        return jsonify({"error": "internal_server_error", "detail": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
