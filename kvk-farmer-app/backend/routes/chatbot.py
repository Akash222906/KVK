from flask import Blueprint, jsonify, request
import os

chatbot_bp = Blueprint('chatbot', __name__)

SYSTEM_PROMPT = """You are KrishiBot, an expert agricultural assistant for West Bengal farmers, created by KVK (Krishi Vigyan Kendra) under ICAR.

You have deep expertise in:
- West Bengal crops: Rice (Aman/Boro/Aus), Jute, Potato, Mustard, Vegetables, Maize
- Local crop varieties: MTU-7029, Swarna, Kufri Jyoti, Kufri Chandramukhi
- West Bengal districts and their agro-climatic zones
- Government schemes: PM-KISAN, Krishak Bandhu (WB state scheme), KCC, PMFBY, PM-KUSUM
- Pest and disease management for WB conditions
- Soil health, fertilizer recommendations per ICAR guidelines
- Market prices and MSP (Minimum Support Price)
- Organic farming and modern techniques

Guidelines:
- Respond in the same language the user writes in (English, Bengali, or Hindi)
- Be practical, specific, and actionable
- Give precise quantities and timings when recommending treatments
- Always mention safety precautions for pesticides
- Refer to local market names and varieties farmers will recognize
- Keep responses concise but complete (3-5 sentences for simple queries, more for complex ones)
- When asked in Bengali, respond fully in Bengali script
"""

def fallback_response(message):
    msg = message.lower()
    if any(w in msg for w in ['rice', 'paddy', 'ধান']):
        return "For rice cultivation in West Bengal, ensure proper water management during transplanting. Apply 80-90 kg N, 40-50 kg P, and 40-50 kg K per hectare. Monitor for Brown Plant Hopper especially during monsoon season."
    if any(w in msg for w in ['potato', 'আলু']):
        return "Potato cultivation in West Bengal: plant October-November. Apply Kufri Jyoti or Kufri Chandramukhi varieties. Watch for late blight in foggy weather — apply Mancozeb 75 WP @ 2g/L as preventive spray."
    if any(w in msg for w in ['scheme', 'subsidy', 'pm-kisan', 'krishak bandhu']):
        return "Key schemes for WB farmers: PM-KISAN gives ₹6,000/year in 3 installments. Krishak Bandhu gives ₹10,000/acre/year + ₹2 lakh death benefit. KCC provides credit up to ₹3 lakh at 4% interest. Apply at your nearest BDO office or CSC center."
    if any(w in msg for w in ['pest', 'insect', 'disease', 'fungus']):
        return "For pest management: identify the pest first before applying chemicals. Contact your nearest KVK for free diagnosis. Use IPM approach — cultural, biological controls before chemical. Always wear protective gear when applying pesticides."
    if any(w in msg for w in ['weather', 'rain', 'temperature']):
        return "West Bengal has 4 agro-seasons: Kharif (Jun-Oct), Rabi (Nov-Feb), Summer (Mar-May), and Zaid. Plan your crops according to the season. Use the Dashboard for current weather data for your district."
    return "Namaste! I am KrishiBot, your farming assistant. Please set your GROQ_API_KEY in the .env file for full AI-powered responses. I can help with crop advice, pest management, government schemes, and market information."

@chatbot_bp.route('/message', methods=['POST'])
def message():
    data    = request.json
    msg     = data.get('message', '')
    history = data.get('history', [])
    api_key = os.environ.get('GROQ_API_KEY', '')

    if not api_key or api_key == 'your_groq_api_key_here':
        return jsonify({'response': fallback_response(msg), 'source': 'fallback'})

    try:
        from groq import Groq
        client = Groq(api_key=api_key)

        messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]
        for h in history[-10:]:
            messages.append({'role': h['role'], 'content': h['content']})
        messages.append({'role': 'user', 'content': msg})

        chat = client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        response_text = chat.choices[0].message.content
        return jsonify({'response': response_text, 'source': 'groq'})

    except Exception as e:
        return jsonify({'response': fallback_response(msg) + f' [Error: {str(e)}]', 'source': 'fallback'})
