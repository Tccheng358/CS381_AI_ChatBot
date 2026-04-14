import os
from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai
from openai import OpenAI  # <-- NEW: The OpenAI Library

app = Flask(__name__)

# ==========================================
# 1. YOUR MASTER KEYS
# ==========================================
# The keys are now pulled from Render's Environment Variables
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# Configure Gemini Brain
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.5-flash') 

# Configure OpenAI Brain
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# ==========================================
# 2. THE MULTI-BRAIN MEMORY BANK
# ==========================================
# This dictionary now stores the active brain choice AND the chat history for both AIs!
user_sessions = {} 

# ==========================================
# 3. THE WEBHOOK 
# ==========================================
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(">> TRACK ERROR: Invalid Signature!")
        abort(400)
    except Exception as e:
        print(f">> TRACK ERROR: Webhook error: {e}")
        abort(500)
        
    return 'OK'

# ==========================================
# 4. THE AI ROUTER & MEMORY LOGIC
# ==========================================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()
    user_id = event.source.user_id 
    
    print(f"\n--- MESSAGE FROM [{user_id}] ---")
    print(f">> USER SAID: {user_text}")

    # ------------------------------------------
    # FEATURE A: MEMORY INITIALIZATION
    # ------------------------------------------
    if user_id not in user_sessions:
        print(">> TRACK: Creating new Multi-Brain memory session...")
        user_sessions[user_id] = {
            'active_brain': 'gemini', # Gemini is the default starting brain
            'gemini_chat': gemini_model.start_chat(history=[]),
            'openai_messages': [{"role": "system", "content": "You are a helpful assistant."}]
        }

    session = user_sessions[user_id]

# ------------------------------------------
    # FEATURE B: THE CONTROL PANEL COMMANDS
    # ------------------------------------------
    # 1. The Kill Switch & Main Menu
    if user_text == "**reset":
        if user_id in user_sessions:
            del user_sessions[user_id] # Wipe their memory
            
        print(">> TRACK: Memory wiped!")
        
        # The new multi-line menu message
        reset_menu = (
            "Memory cleared! 🧹\n"
            "Your chat history has been completely erased.\n\n"
            "🧠 Current Brain: GEMINI (Default)\n\n"
            "To change the AI brain at any time, type:\n"
            "👉 /openai (Switch to ChatGPT)\n"
            "👉 /gemini (Switch to Google Gemini)"
        )
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reset_menu)
        )
        return

    # 2. Switch to Gemini
    if user_text.lower() == "/gemini":
        session['active_brain'] = 'gemini'
        print(">> TRACK: Switched to Gemini")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="🧠 Brain Switched! You are now talking to Google Gemini."))
        return

    # 3. Switch to OpenAI
    if user_text.lower() == "/openai":
        session['active_brain'] = 'openai'
        print(">> TRACK: Switched to OpenAI")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="🧠 Brain Switched! You are now talking to OpenAI ChatGPT."))
        return

    # ------------------------------------------
    # FEATURE C: THE DUAL-BRAIN ROUTER
    # ------------------------------------------
    try:
        if session['active_brain'] == 'gemini':
            print(">> TRACK: Thinking... asking Gemini...")
            ai_response = session['gemini_chat'].send_message(user_text)
            reply_text = ai_response.text
            
        elif session['active_brain'] == 'openai':
            print(">> TRACK: Thinking... asking OpenAI...")
            
            # Step 1: Add the user's message to OpenAI's memory list
            session['openai_messages'].append({"role": "user", "content": user_text})
            
            # Step 2: Send the whole memory list to OpenAI (Using the standard 3.5-turbo model)
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=session['openai_messages']
            )
            reply_text = response.choices[0].message.content
            
            # Step 3: Save OpenAI's answer back into the memory list
            session['openai_messages'].append({"role": "assistant", "content": reply_text})

        print(f">> TRACK: {session['active_brain'].upper()} replied successfully!")
        
        # Send the final response back to LINE
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
        
    except Exception as e:
        print(f">> TRACK ERROR: AI failed: {e}")
        error_msg = f"System Error with {session['active_brain'].upper()}. Check your API limits or type **reset."
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=error_msg))

if __name__ == "__main__":
    app.run(port=5555)
    
# ==========================================
# HW3 REQUIREMENT: RESTful API for History
# ==========================================

# 1. GET API: Retrieve chat history for Postman screenshot
@app.route("/history/<user_id>", methods=['GET'])
def get_history(user_id):
    if user_id in user_sessions:
        session = user_sessions[user_id]
        history_data = []
        
        # Format the history for the JSON response
        # This part depends on the brain used (Gemini vs OpenAI)
        if session.get('active_brain') == 'gemini':
            for message in session['gemini_chat'].history:
                history_data.append({
                    "role": message.role,
                    "content": message.parts[0].text
                })
        else:
            history_data = session['openai_messages']
            
        return jsonify({"user_id": user_id, "history": history_data}), 200
    
    return jsonify({"error": "User not found"}), 404

# 2. DELETE API: Clear history for Postman screenshot
@app.route("/history/<user_id>", methods=['DELETE'])
def delete_history(user_id):
    if user_id in user_sessions:
        # Reset the memory sessions for this specific user
        del user_sessions[user_id]
        return jsonify({
            "message": "History deleted successfully.",
            "user_id": user_id
        }), 200
        
    return jsonify({"error": "User not found"}), 404