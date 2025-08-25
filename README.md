# Flask Talken Chatbot

A conversational AI chatbot built with Flask and DeepSeek's API, featuring a modern web interface.



## Features

- Modern chat interface with message history
- Integration with DeepSeek's AI API
- Environment-based configuration
- Responsive design for all devices
- Secure session management

## Prerequisites

- Python 3.8+
- Flask 2.0+
- DeepSeek API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/flask_deepseek_chatbot.git
   cd flask_deepseek_chatbot
Create and activate virtual environment:

bash
python -m venv envv
source envv/bin/activate  # Linux/Mac
.\envv\Scripts\activate  # Windows
Install dependencies:

bash
pip install -r requirements.txt
Configure environment:

bash
cp .env.example .env
Edit .env with your DeepSeek API key.

**Usage**
Run the development server:

bash
flask run
Access the chatbot at:
http://localhost:5000

**Project Structure**
flask_deepseek_chatbot/
├── app.py               # Main application
├── requirements.txt     # Dependencies
├── .env.example         # Environment template
├── .gitignore           # Git ignore rules
├── static/              # Static files (CSS, JS)
│   └── style.css
└── templates/           # HTML templates
    └── index.html
