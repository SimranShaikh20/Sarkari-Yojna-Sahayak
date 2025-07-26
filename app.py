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
        'system_prompt': '''आप एक विशेषज्ञ सरकारी योजना सलाहकार हैं। केवल हिंदी में उत्तर दें। भारत सरकार और राज्य सरकारों की सभी योजनाओं के बारे में विस्तृत, सटीक जानकारी प्रदान करें।

निम्नलिखित जानकारी शामिल करें:
1. योजना का पूरा नाम
2. पात्रता मापदंड
3. लाभ और राशि
4. आवेदन की प्रक्रिया
5. आवश्यक दस्तावेज
6. आधिकारिक वेबसाइट (यदि पता हो)

केंद्र और राज्य सरकार की योजनाओं को कवर करें जैसे कि:
- कृषि योजनाएं (PM-KISAN, फसल बीमा, मिट्टी हेल्थ कार्ड)
- आवास योजनाएं (PMAY, IAY)
- स्वास्थ्य योजनाएं (आयुष्मान भारत, जननी सुरक्षा)
- शिक्षा योजनाएं (छात्रवृत्ति, बेटी बचाओ बेटी पढ़ाओ)
- रोजगार योजनाएं (MGNREGA, स्किल इंडिया)
- पेंशन योजनाएं (APY, NSAP)
- व्यापार योजनाएं (मुद्रा, स्टार्टअप इंडिया)

सटीक और व्यावहारिक जानकारी दें।'''
    },
    'english': {
        'code': 'en-IN',
        'voice_lang': 'en-IN', 
        'name': 'English',
        'system_prompt': '''You are an expert Government Scheme Advisor. Answer only in English. Provide detailed, accurate information about ALL Indian government schemes - both central and state government schemes.

Include the following information:
1. Full scheme name
2. Eligibility criteria  
3. Benefits and amounts
4. Application process
5. Required documents
6. Official website (if known)

Cover central and state government schemes including:
- Agriculture schemes (PM-KISAN, Crop Insurance, Soil Health Card)
- Housing schemes (PMAY, IAY, Awas Plus)
- Health schemes (Ayushman Bharat, Janani Suraksha, RSBY)
- Education schemes (Scholarships, Beti Bachao Beti Padhao, Mid-Day Meal)
- Employment schemes (MGNREGA, Skill India, PMKVY)
- Pension schemes (APY, NSAP, Employees Pension)
- Business schemes (Mudra, Startup India, Stand-up India)
- Social Security schemes (PDS, LPG Subsidy, Ration Card)

Provide accurate, practical, and actionable information.'''
    },
    'gujarati': {
        'code': 'gu-IN',
        'voice_lang': 'gu-IN',
        'name': 'ગુજરાતી',
        'system_prompt': '''તમે એક નિષ્ણાત સરકારી યોજના સલાહકાર છો। ફક્ત ગુજરાતીમાં જવાબ આપો। ભારત સરકાર અને રાજ્య સરકારોની તમામ યોજનાઓ વિશે વિગતવાર, સચોટ માહિતી આપો।

નીચેની માહિતી સામેલ કરો:
1. યોજનાનું સંપૂર્ણ નામ
2. પાત્રતાના માપદંડો
3. લાભો અને રકમ
4. અરજીની પ્રક્રિયા
5. જરૂરી કાગળો
6. સત્તાવાર વેબસાઇટ (જો ખબર હોય)

કેન્દ્ર અને રાજ્ય સરકારની યોજનાઓ આવરો જેમ કે:
- કૃષિ યોજનાઓ (PM-KISAN, પાક વીમો, માટી આરોગ્ય કાર્ડ)
- આવાસ યોજનાઓ (PMAY, IAY)
- આરોગ્ય યોજનાઓ (આયુષ્માન ભારત, જનની સુરક્ષા)
- શિક્ષણ યોજનાઓ (શિષ્યવૃત્તિ, બેટી બચાઓ બેટી પઢાઓ)
- રોજગાર યોજનાઓ (MGNREGA, સ્કિલ ઇન્ડિયા)
- પેન્શન યોજનાઓ (APY, NSAP)
- વ્યાપાર યોજનાઓ (મુદ્રા, સ્ટાર્ટઅપ ઇન્ડિયા)

સચોટ અને વ્યાવહારિક માહિતી આપો.'''
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
        
        # Enhanced query with specific instructions
        enhanced_query = f"""Please provide comprehensive information about: {query}

If this is about a specific government scheme, include:
- Complete official scheme name
- Current eligibility criteria
- Exact benefit amounts
- Step-by-step application process
- Required documents list
- Official website/portal link
- Contact information if available

If this is a general query about a category (like agriculture, health, education), list multiple relevant schemes with brief details.

Provide accurate, up-to-date information for 2024-2025."""

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": lang_config['system_prompt']
                },
                {
                    "role": "user",
                    "content": enhanced_query
                }
            ],
            model="llama3-8b-8192",
            temperature=0.2,  # Lower for more factual responses
            max_tokens=1500   # Increased for comprehensive answers
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
            
        # Primary: Use AI for comprehensive coverage of all schemes
        ai_response = get_groq_response(query, language)
        
        # Check if AI gave a good response
        if ai_response and len(ai_response.strip()) > 50:
            return jsonify({
                'response': ai_response,
                'source': 'ai',
                'language': language
            })
        
        # Fallback: Search local schemes if AI fails
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
            
            return jsonify({
                'response': response,
                'source': 'local',
                'language': language
            })
        
        # If both AI and local search fail, return the AI response anyway (error message)
        response = ai_response or "Sorry, I couldn't find information about this scheme."
        
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
