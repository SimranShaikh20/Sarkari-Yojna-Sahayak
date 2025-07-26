import os
import json
import logging
from flask import Flask, render_template, request, jsonify
from groq import Groq
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY", "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")
if not groq_api_key:
    logging.error("GROQ_API_KEY not found in environment variables")
    groq_client = None
else:
    groq_client = Groq(api_key=groq_api_key)

# Load schemes data
def load_schemes():
    try:
        with open('schemes.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning("schemes.json not found, using empty schemes data")
        return {"schemes": []}
    except Exception as e:
        logging.error(f"Error loading schemes: {e}")
        return {"schemes": []}

schemes_data = load_schemes()

# Language configurations
LANGUAGES = {
    'hindi': {
        'code': 'hi-IN',
        'voice_lang': 'hi-IN',
        'name': 'हिंदी',
        'system_prompt': 'Answer in Hindi language only. Provide detailed information about government schemes.'
    },
    'english': {
        'code': 'en-IN',
        'voice_lang': 'en-IN', 
        'name': 'English',
        'system_prompt': 'Answer in English language only. Provide detailed information about government schemes.'
    },
    'gujarati': {
        'code': 'gu-IN',
        'voice_lang': 'gu-IN',
        'name': 'ગુજરાતી',
        'system_prompt': 'Answer in Gujarati language only. Provide detailed information about government schemes.'
    }
}

def search_local_schemes(query, language='english'):
    """Search for schemes in local data"""
    query_lower = query.lower()
    matching_schemes = []
    
    # Define scheme-specific keywords for better matching
    scheme_keywords = {
        'kisan': ['kisan', 'farmer', 'agriculture', 'किसान', 'खेती'],
        'awas': ['awas', 'housing', 'house', 'home', 'मकान', 'आवास'],
        'ayushman': ['ayushman', 'health', 'medical', 'insurance', 'स्वास्थ्य', 'आयुष्मान'],
        'matru': ['matru', 'pregnant', 'mother', 'maternity', 'गर्भवती', 'मातृ'],
        'pension': ['pension', 'elderly', 'widow', 'disability', 'पेंशन', 'बुजुर्ग', 'विधवा'],
        'beti': ['beti', 'girl', 'daughter', 'education', 'बेटी', 'लड़की', 'शिक्षा'],
        'fasal': ['fasal', 'crop', 'insurance', 'फसल', 'बीमा']
    }
    
    query_words = [word for word in query_lower.split() if len(word) > 3]
    
    for scheme in schemes_data.get('schemes', []):
        # Search in scheme name and key fields
        searchable_text = f"{scheme.get('scheme_name', '')} {scheme.get('description', '')} {scheme.get('category', '')}".lower()
        
        # Check for exact scheme name matches first
        scheme_name_lower = scheme.get('scheme_name', '').lower()
        if any(word in scheme_name_lower for word in query_words):
            matching_schemes.append(scheme)
            continue
            
        # Check for category-specific keyword matches
        category = scheme.get('category', '')
        for key_category, keywords in scheme_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                if category in ['agriculture', 'housing', 'health', 'women', 'social_security', 'education']:
                    if (category == 'agriculture' and any(k in keywords for k in ['kisan', 'farmer', 'fasal', 'crop'])) or \
                       (category == 'housing' and any(k in keywords for k in ['awas', 'housing', 'house'])) or \
                       (category == 'health' and any(k in keywords for k in ['ayushman', 'health', 'medical'])) or \
                       (category == 'women' and any(k in keywords for k in ['matru', 'beti', 'girl', 'pregnant'])) or \
                       (category == 'social_security' and any(k in keywords for k in ['pension', 'elderly', 'widow'])):
                        matching_schemes.append(scheme)
                        break
    
    # Remove duplicates
    seen = set()
    unique_schemes = []
    for scheme in matching_schemes:
        scheme_id = scheme.get('scheme_name', '')
        if scheme_id not in seen:
            seen.add(scheme_id)
            unique_schemes.append(scheme)
    
    return unique_schemes

def get_groq_response(query, language='english'):
    """Get response from Groq API"""
    try:
        if not groq_client:
            error_messages = {
                'hindi': 'खुशी है कि आपने पूछा। कृपया API कुंजी जांच लें और फिर से कोशिश करें।',
                'english': 'Sorry, AI service is not available. Please check API configuration and try again.',
                'gujarati': 'માફ કરશો, AI સેવા ઉપલબ્ધ નથી. કૃપા કરીને API કરાર જોઈ ફરીથી પ્રયાસ કરો.'
            }
            return error_messages.get(language, error_messages['english'])
            
        lang_config = LANGUAGES.get(language, LANGUAGES['english'])
        
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"{lang_config['system_prompt']} You are a helpful assistant specializing in Indian government schemes and programs. Provide accurate, helpful information about eligibility, benefits, and application processes."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            model="llama3-8b-8192",
            temperature=0.3,
            max_tokens=1000
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        logging.error(f"Error getting Groq response: {e}")
        error_messages = {
            'hindi': 'खुशी है कि आपने पूछा। कृपया फिर से कोशिश करें या अपना प्रश्न दूसरे तरीके से पूछें।',
            'english': 'Sorry, I encountered an error processing your request. Please try again or rephrase your question.',
            'gujarati': 'માફ કરશો, તમારી વિનંતી પર પ્રક્રિયા કરતી વખતે મને ભૂલ આવી. કૃપા કરીને ફરીથી પ્રયાસ કરો.'
        }
        return error_messages.get(language, error_messages['english'])

@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES)

@app.route('/query', methods=['POST'])
def handle_query():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        language = data.get('language', 'english')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
            
        # First, search local schemes
        local_schemes = search_local_schemes(query, language)
        
        if local_schemes:
            # Format local scheme response
            scheme = local_schemes[0]  # Return first match
            response_templates = {
                'hindi': f"योजना का नाम: {scheme.get('scheme_name', 'N/A')}\n\nपात्रता: {scheme.get('eligibility', 'जानकारी उपलब्ध नहीं')}\n\nलाभ: {scheme.get('benefits', 'जानकारी उपलब्ध नहीं')}\n\nआवेदन कैसे करें: {scheme.get('how_to_apply', 'जानकारी उपलब्ध नहीं')}",
                'english': f"Scheme Name: {scheme.get('scheme_name', 'N/A')}\n\nEligibility: {scheme.get('eligibility', 'Information not available')}\n\nBenefits: {scheme.get('benefits', 'Information not available')}\n\nHow to Apply: {scheme.get('how_to_apply', 'Information not available')}",
                'gujarati': f"યોજનાનું નામ: {scheme.get('scheme_name', 'N/A')}\n\nપાત્રતા: {scheme.get('eligibility', 'માહિતી ઉપલબ્ધ નથી')}\n\nફાયદા: {scheme.get('benefits', 'માહિતી ઉપલબ્ધ નથી')}\n\nઅરજી કેવી રીતે કરવી: {scheme.get('how_to_apply', 'માહિતી ઉપલબ્ધ નથી')}"
            }
            
            response = response_templates.get(language, response_templates['english'])
            
            return jsonify({
                'response': response,
                'source': 'local',
                'language': language
            })
        
        # If no local match, use Groq API
        response = get_groq_response(query, language)
        
        return jsonify({
            'response': response,
            'source': 'ai',
            'language': language
        })
        
    except Exception as e:
        logging.error(f"Error handling query: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
