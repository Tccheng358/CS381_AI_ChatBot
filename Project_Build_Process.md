# Project Build Process: Multi-Brain AI Bot

## 1. Webhook Foundation
* **Goal**: Establish a Flask server as a webhook connected to the LINE Messaging API.
* **Process**: Created a local Python Flask server (port 5555). Used `ngrok` to expose the local server to the public internet and configured the LINE Developer Console with the generated URL.
* **Issue Encountered**: LINE Webhook verification failed.
* **Resolution**: Corrected the webhook URL in the LINE Console to exactly match the active ngrok URL appended with the `/callback` route.

## 2. Primary AI Integration (Google Gemini)
* **Goal**: Replace simple echo logic with AI-generated responses.
* **Process**: Integrated the `google-generativeai` library.
* **Issue Encountered**: API returned a `404 Not Found` error when requesting the `gemini-1.5-flash` model.
* **Resolution**: Updated the model configuration to the supported `gemini-2.5-flash` model version.

## 3. State Management and Memory
* **Goal**: Enable the bot to remember conversation context per user.
* **Process**: Implemented an in-memory Python dictionary (`user_sessions`) mapping the unique LINE `user_id` to individual chat histories. Added a reset command to clear memory.
* **Issue Encountered**: The bot unintentionally cleared memory when the word "reset" was used conversationally.
* **Resolution**: Modified the trigger condition to require an exact programmatic string match (`**reset`).

## 4. Dual-Brain System (OpenAI Integration)
* **Goal**: Add a secondary AI model and allow users to switch between them.
* **Process**: Integrated the `openai` library. Built routing logic using commands (`/openai`, `/gemini`) to toggle the active API within the user's session state.
* **Issue Encountered**: API returned a `401 Unauthorized` error on OpenAI calls.
* **Resolution**: Removed placeholder text from the `OPENAI_API_KEY` string so it contained only the valid API key.

## 5. Cloud Deployment
* **Goal**: Deploy the application to a 24/7 cloud hosting environment.
* **Process**: Migrated the application to Render.com. Generated `requirements.txt` for dependencies and refactored the code to use environment variables (`os.getenv`) instead of hardcoded API keys.
* **Issue Encountered**: The bot stopped responding after deployment.
* **Resolution**: Updated the webhook URL in the LINE Developer Console from the expired `ngrok` URL to the new permanent Render URL (`https://cs381-ai-chatbot.onrender.com/callback`).

---

## Architecture Summary

| Component | Technology |
| :--- | :--- |
| **Backend Framework** | Flask (Python) |
| **Messaging Platform** | LINE Messaging API |
| **Primary AI** | Google Gemini 2.5 Flash |
| **Secondary AI** | OpenAI GPT-3.5 Turbo |
| **State Management** | Python In-Memory Dictionary |
| **Hosting/Deployment** | Render.com |
| **Secrets Management** | Environment Variables |