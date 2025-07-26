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
                if (category == 'agriculture' and any(k in query_lower for k in ['kisan', 'farmer', 'fasal', 'crop', 'किसान', 'खेती', 'फसल'])) or \
                   (category == 'housing' and any(k in query_lower for k in ['awas', 'housing', 'house', 'makan', 'आवास', 'मकान'])) or \
                   (category == 'health' and any(k in query_lower for k in ['ayushman', 'health', 'medical', 'स्वास्थ्य', 'आयुष्मान'])) or \
                   (category == 'women' and any(k in query_lower for k in ['matru', 'beti', 'girl', 'pregnant', 'मातृ', 'बेटी', 'गर्भवती'])) or \
                   (category == 'social_security' and any(k in query_lower for k in ['pension', 'elderly', 'widow', 'पेंशन', 'बुजुर्ग', 'विधवा'])):
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
            # Format local scheme response in selected language only
            scheme = local_schemes[0]  # Return first match
            
            if language == 'hindi':
                scheme_name = scheme.get('scheme_name_hindi', scheme.get('scheme_name', 'N/A'))
                eligibility = scheme.get('eligibility_hindi', 'जानकारी उपलब्ध नहीं')
                benefits = scheme.get('benefits_hindi', 'जानकारी उपलब्ध नहीं')
                how_to_apply = scheme.get('how_to_apply_hindi', 'जानकारी उपलब्ध नहीं')
                response = f"योजना का नाम: {scheme_name}\n\nपात्रता: {eligibility}\n\nलाभ: {benefits}\n\nआवेदन कैसे करें: {how_to_apply}"
            elif language == 'gujarati':
                scheme_name = scheme.get('scheme_name_gujarati', scheme.get('scheme_name', 'N/A'))
                eligibility = scheme.get('eligibility_gujarati', 'માહિતી ઉપલબ્ધ નથી')
                benefits = scheme.get('benefits_gujarati', 'માહિતી ઉપલબ્ધ નથી')
                how_to_apply = scheme.get('how_to_apply_gujarati', 'માહિતી ઉપલબ્ધ નથી')
                response = f"યોજનાનું નામ: {scheme_name}\n\nપાત્રતા: {eligibility}\n\nફાયદા: {benefits}\n\nઅરજી કેવી રીતે કરવી: {how_to_apply}"
            else:  # English
                response = f"Scheme Name: {scheme.get('scheme_name', 'N/A')}\n\nEligibility: {scheme.get('eligibility', 'Information not available')}\n\nBenefits: {scheme.get('benefits', 'Information not available')}\n\nHow to Apply: {scheme.get('how_to_apply', 'Information not available')}"
            
            response_templates = {
                'hindi': response if language == 'hindi' else None,
                'english': response if language == 'english' else None,
                'gujarati': response if language == 'gujarati' else None
            }
            
            final_response = response
            
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
