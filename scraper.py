import json
import logging
import os
import requests
from bs4 import BeautifulSoup
import trafilatura

# Configure logging
logging.basicConfig(level=logging.INFO)

def scrape_scheme_with_groq(url, groq_api_key):
    """Use Groq API to extract and structure scheme data from government websites"""
    try:
        # First, get the website content
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return None
            
        text = trafilatura.extract(downloaded)
        if not text or len(text) < 100:
            return None
            
        # Use Groq to structure the extracted content
        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""Extract government scheme information from this content and format it in JSON:

Content: {text[:2000]}

Please extract and return ONLY a JSON object with these fields:
- scheme_name (in Hindi if possible)
- description (brief, in Hindi)
- eligibility (bullet points in Hindi)
- documents_required (bullet points in Hindi)
- apply_steps (numbered steps in Hindi)
- official_link (the original URL: {url})
- keywords (array of relevant search terms in both Hindi and English)

Return only valid JSON, no extra text."""

        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.1,
            "max_tokens": 1500
        }
        
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                               headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            groq_response = result["choices"][0]["message"]["content"]
            
            # Try to parse the JSON response
            import json
            try:
                scheme_data = json.loads(groq_response)
                scheme_data["official_link"] = url  # Ensure URL is correct
                return scheme_data
            except json.JSONDecodeError:
                logging.error(f"Failed to parse Groq JSON response for {url}")
                return None
        else:
            logging.error(f"Groq API error for {url}: {response.status_code}")
            return None
            
    except Exception as e:
        logging.error(f"Error processing {url} with Groq: {e}")
        return None

def scrape_myscheme_data():
    """Scrape scheme data from government websites using Groq for extraction"""
    schemes = []
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if not groq_api_key:
        logging.warning("No Groq API key found, using default schemes only")
        return []
    
    # Government scheme URLs to scrape
    scheme_urls = [
        'https://www.myscheme.gov.in/schemes/pm-kisan',
        'https://www.myscheme.gov.in/schemes/pmay-g', 
        'https://www.myscheme.gov.in/schemes/nsap',
        'https://www.myscheme.gov.in/schemes/pmjay',
        'https://pmkisan.gov.in/',
        'https://pmayg.nic.in/',
        'https://nsap.nic.in/',
        'https://pmjay.gov.in/'
    ]
    
    for url in scheme_urls:
        logging.info(f"Processing with Groq: {url}")
        scheme_data = scrape_scheme_with_groq(url, groq_api_key)
        
        if scheme_data:
            schemes.append(scheme_data)
            logging.info(f"Successfully extracted: {scheme_data.get('scheme_name', 'Unknown')}")
        else:
            logging.warning(f"Failed to extract data from: {url}")
    
    return schemes

def create_default_schemes():
    """Create default scheme data with accurate information"""
    schemes = [
        {
            "scheme_name": "प्रधानमंत्री किसान सम्मान निधि योजना",
            "description": "किसानों के लिए आर्थिक सहायता योजना जिसके तहत प्रति वर्ष 6000 रुपये की राशि दी जाती है।",
            "eligibility": "• भारत का नागरिक होना चाहिए\n• 2 हेक्टेयर तक भूमि होनी चाहिए\n• सरकारी नौकरी में नहीं होना चाहिए",
            "documents_required": "• आधार कार्ड\n• बैंक खाता पासबुक\n• भूमि के कागजात\n• मोबाइल नंबर",
            "apply_steps": "1. PM-KISAN की आधिकारिक वेबसाइट पर जाएं\n2. 'New Farmer Registration' पर क्लिक करें\n3. आधार नंबर और अन्य विवरण भरें\n4. दस्तावेज अपलोड करें\n5. आवेदन जमा करें",
            "official_link": "https://pmkisan.gov.in",
            "keywords": ["किसान", "कृषि", "farmer", "agriculture", "pmkisan"]
        },
        {
            "scheme_name": "प्रधानमंत्री आवास योजना (ग्रामीण)",
            "description": "ग्रामीण क्षेत्रों में गरीब परिवारों के लिए पक्के मकान बनाने की योजना।",
            "eligibility": "• BPL परिवार होना चाहिए\n• ग्रामीण क्षेत्र में निवास\n• कच्चा या अधूरा मकान होना चाहिए\n• पहले से पक्का मकान नहीं होना चाहिए",
            "documents_required": "• आधार कार्ड\n• BPL प्रमाण पत्र\n• आय प्रमाण पत्र\n• निवास प्रमाण पत्र\n• बैंक खाता विवरण",
            "apply_steps": "1. ग्राम पंचायत से संपर्क करें\n2. आवेदन फॉर्म भरें\n3. आवश्यक दस्तावेज जमा करें\n4. सत्यापन की प्रतीक्षा करें",
            "official_link": "https://pmayg.nic.in",
            "keywords": ["आवास", "मकान", "housing", "pmay", "गृह"]
        },
        {
            "scheme_name": "राष्ट्रीय सामाजिक सहायता कार्यक्रम (वृद्धावस्था पेंशन)",
            "description": "60 वर्ष या अधिक आयु के गरीब व्यक्तियों के लिए मासिक पेंशन योजना।",
            "eligibility": "• 60 वर्ष या अधिक आयु\n• BPL परिवार से होना चाहिए\n• कोई नियमित आय नहीं होनी चाहिए",
            "documents_required": "• आयु प्रमाण पत्र\n• आधार कार्ड\n• BPL प्रमाण पत्र\n• आय प्रमाण पत्र\n• बैंक खाता विवरण",
            "apply_steps": "1. जिला कलेक्टर कार्यालय में जाएं\n2. आवेदन फॉर्म भरें\n3. दस्तावेज जमा करें\n4. सत्यापन के बाद पेंशन शुरू होगी",
            "official_link": "https://nsap.nic.in",
            "keywords": ["पेंशन", "वृद्धावस्था", "pension", "elderly", "बुजुर्ग"]
        },
        {
            "scheme_name": "आयुष्मान भारत योजना",
            "description": "गरीब परिवारों के लिए 5 लाख रुपये तक का मुफ्त इलाज।",
            "eligibility": "• SECC-2011 डेटाबेस में नाम होना चाहिए\n• गरीब परिवार से होना चाहिए\n• ग्रामीण या शहरी क्षेत्र में BPL स्थिति",
            "documents_required": "• आधार कार्ड\n• राशन कार्ड\n• मोबाइल नंबर\n• परिवार के सदस्यों का विवरण",
            "apply_steps": "1. नजदीकी CSC सेंटर जाएं\n2. पात्रता की जांच कराएं\n3. गोल्डन कार्ड बनवाएं\n4. सूचीबद्ध अस्पतालों में इलाज कराएं",
            "official_link": "https://pmjay.gov.in",
            "keywords": ["स्वास्थ्य", "इलाज", "health", "ayushman", "medical"]
        }
    ]
    
    return schemes

def generate_schemes_file():
    """Generate schemes.json file with real and default data"""
    try:
        # Try to scrape real data
        logging.info("Attempting to scrape scheme data...")
        scraped_schemes = scrape_myscheme_data()
        
        # Get default schemes
        default_schemes = create_default_schemes()
        
        # Combine scraped and default data
        all_schemes = default_schemes + scraped_schemes
        
        schemes_data = {
            "last_updated": "2025-01-25",
            "total_schemes": len(all_schemes),
            "schemes": all_schemes
        }
        
        # Save to file
        with open('schemes.json', 'w', encoding='utf-8') as f:
            json.dump(schemes_data, f, ensure_ascii=False, indent=2)
        
        logging.info(f"Successfully created schemes.json with {len(all_schemes)} schemes")
        
    except Exception as e:
        logging.error(f"Error generating schemes file: {e}")
        
        # Create minimal fallback data
        fallback_data = {
            "last_updated": "2025-01-25",
            "total_schemes": len(create_default_schemes()),
            "schemes": create_default_schemes()
        }
        
        with open('schemes.json', 'w', encoding='utf-8') as f:
            json.dump(fallback_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    generate_schemes_file()
