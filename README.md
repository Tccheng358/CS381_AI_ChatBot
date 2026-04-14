# CS381_AI_ChatBot

BOT Basic ID: @213xfnjr

A powerful LINE Chatbot built with Python and Flask that dynamically switches between multiple AI "brains": **Google Gemini** and **OpenAI (ChatGPT)**. The bot assigns an independent memory session to every user, allowing it to remember conversation history natively based on the chosen AI.

## Features & Supported APIs (The "Brains")

This chatbot natively supports the following APIs and AI models:
*   **Google Gemini API**: Utilizing the `gemini-2.5-flash` model. (Default Brain)
*   **OpenAI API**: Utilizing the `gpt-3.5-turbo` model.
*   **LINE Messaging API**: For the chatbot interface and webhook integrations.

## How to Use the Chatbot

Once the chatbot is running and connected to your LINE app, you can start chatting immediately. By default, the bot initializes with the **Google Gemini** brain. It remembers the context of your conversation as long as the session corresponds to your unique LINE User ID.

### Menus and Keywords

You can control the chatbot's memory and active brain using the following commands anywhere in the chat:

*   `**reset`
    *   **Action**: Completely wipes your persistent chat history and memory. 
    *   **Response**: Displays a main control menu and confirms that your memory has been cleared.
*   `/gemini`
    *   **Action**: Switches the chatbot's active brain to **Google Gemini**.
    *   **Response**: *"🧠 Brain Switched! You are now talking to Google Gemini."*
*   `/openai`
    *   **Action**: Switches the chatbot's active brain to **OpenAI ChatGPT**.
    *   **Response**: *"🧠 Brain Switched! You are now talking to OpenAI ChatGPT."*

## Setup and Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Tccheng358/CS381_AI_ChatBot.git
    cd CS381_AI_ChatBot
    ```

2.  **Install Requirements**:
    Ensure you have Python installed, then run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Keys**:
    Open `app.py` and replace the placeholder master keys with your actual credentials:
    *   `CHANNEL_ACCESS_TOKEN` (LINE Developer Console)
    *   `CHANNEL_SECRET` (LINE Developer Console)
    *   `GEMINI_API_KEY` (Google AI Studio)
    *   `OPENAI_API_KEY` (OpenAI Platform)

    *(Note: For production environments, it is highly recommended to use environment variables (`os.environ.get(...)`) to store these keys securely rather than hardcoding them in `app.py`.)*

4.  **Run the Server**:
    Start the local Flask app, which runs on port `5555`:
    ```bash
    python app.py
    ```

5.  **Connect the Webhook**:
    Use a proxy tool like `ngrok` (e.g., `ngrok http 5555`) to expose your local server to the internet. Then, add the resulting `.ngrok.app/callback` URL in your LINE Developer Console under the Webhook settings.

---

## 🛠️ Local Setup & Deployment Precautions

### 1. Virtual Environment (`.venv`)
Use a virtual environment to prevent dependency conflicts between projects:
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 2. Dependencies
Install the exact library versions used during development:
```bash
pip install -r requirements.txt
```

### 3. API Keys & Security
Never hardcode API keys (Gemini, OpenAI, LINE) in the source code.
* **Local:** Use a `.env` file and ensure it is added to `.gitignore`.
* **Deployment:** Set environment variables in your cloud hosting dashboard (e.g., Render, Heroku).

### 4. Webhook Configuration
The LINE Messaging API requires a valid HTTPS Webhook URL ending in `/callback` (e.g., `https://your-domain.com/callback`).
* **Local Testing:** If using a tunneling service like **ngrok**, remember to update the Webhook URL in the LINE Developer Console every time the service restarts.

### 5. Cloud Hosting Cold Starts
If deployed on free-tier cloud services (like Render), the server may sleep after periods of inactivity. The initial request to wake the server may take 30–60 seconds to process.


