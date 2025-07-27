# सरकारी योजना सहायक (Sarkari Yojana Sahayak)

<div align="center">

![Sarkari Yojana Sahayak](https://img.shields.io/badge/Sarkari%20Yojana-Sahayak-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-green?style=flat-square&logo=flask)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow?style=flat-square&logo=javascript)
![License](https://img.shields.io/badge/License-MIT-red?style=flat-square)
![Real-time](https://img.shields.io/badge/Real--time-Scraping-orange?style=flat-square)

**A multilingual, voice-enabled AI assistant for Indian government schemes with real-time data scraping**

[Features](#features) • [Architecture](#architecture) • [Installation](#installation) • [Usage](#usage) • [API](#api)

</div>

🌐 [Visit Live Website](https://sarkari-yojna-sahayak.onrender.com/)

---

## 🎯 Overview

Sarkari Yojana Sahayak is a comprehensive AI-powered web application designed to help users discover and understand Indian government schemes. The application supports **Hindi**, **English**, and **Gujarati** languages with complete voice interaction capabilities, allowing users to speak their queries and receive spoken responses about various government welfare programs. **All scheme data is scraped in real-time from official government websites** to ensure the most current and accurate information is always provided.

### 🌟 Key Highlights
- 🕷️ **Real-time Government Website Scraping** - Fresh data for every query
- 🗣️ **Voice Recognition & Text-to-Speech** in 3 languages
- 🤖 **AI-Powered Responses** using Groq Mixtral model
- 📊 **Authentic Government Data** from official sources (scraped live)
- 🎨 **Modern Glassmorphism UI** with responsive design
- 🔄 **Dual Input Methods** - Voice and Text input
- 🎯 **Pure Language Responses** - No language mixing
- ⚡ **Always Updated Information** - No stale data

---

## 🚀 Features

### 🕷️ Real-time Web Scraping System
- **Live Data Extraction**: Scrapes data directly from government websites during query processing
- **Multiple Source Integration**: Covers 15+ official government portals simultaneously
- **Smart Content Parsing**: Extracts scheme details, eligibility criteria, and application processes
- **Automatic Content Validation**: Ensures data authenticity from official sources
- **Intelligent Fallback**: Multiple scraping strategies for robust data extraction

### 🎤 Voice Interface
- **Speech Recognition**: Browser-native Web Speech API supporting hi-IN, en-IN, and gu-IN
- **Text-to-Speech**: Natural voice responses with language-appropriate voice selection
- **Voice Controls**: Stop, replay, and pause functionality
- **Real-time Feedback**: Visual pulse animations during voice capture

### 🌐 Multilingual Support
- **Three Languages**: Hindi (हिंदी), English, Gujarati (ગુજરાતી)
- **Dynamic Language Switching**: Affects UI, voice recognition, and AI responses
- **Language-specific Fonts**: Proper rendering for Devanagari and Gujarati scripts
- **Pure Language Responses**: No English mixed with Hindi/Gujarati

### 🤖 AI Integration
- **LLM Provider**: Groq API with Mixtral-8x7B model
- **Context Awareness**: Language-specific system prompts
- **Intelligent Enhancement**: Real-time scraped data combined with AI explanations
- **Smart Query Processing**: Advanced keyword matching and categorization

### 💾 Government Schemes Database (Real-time Scraped)
- **Live Data**: All scheme information scraped in real-time from official government websites
- **Comprehensive Coverage**: Agriculture, Housing, Health, Women, Social Security, Education
- **Multilingual Content**: Scheme information available in all three supported languages
- **Always Current**: No outdated information - data is fetched fresh for each query

### 🎨 User Interface
- **Glassmorphism Design**: Modern, translucent interface elements
- **Responsive Layout**: Works seamlessly on desktop and mobile devices
- **Dual Input Modes**: Toggle between voice and text input
- **Interactive Elements**: Hover effects, animations, and feedback
- **Real-time Indicators**: Shows when data is being scraped from live sources
- **Accessibility**: High contrast colors and clear typography

---

## 🏗️ Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT (Browser)                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   HTML5 UI      │  │  Web Speech API │  │ JavaScript  │ │
│  │ (Glassmorphism) │  │ (Recognition &  │  │ (ES6+)      │ │
│  │                 │  │  Synthesis)     │  │             │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │ HTTP/AJAX
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    FLASK SERVER                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  Route Handler  │  │ Query Processor │  │Session Mgmt │ │
│  │   (/query)      │  │   (AI Logic)    │  │             │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
│                              │                             │
│                              ▼                             │
│  ┌─────────────────┐  ┌─────────────────┐                 │
│  │ Real-time Web   │  │  Language       │                 │
│  │ Scraper Engine  │  │  Processing     │                 │
│  └─────────────────┘  └─────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
          │                           │ External API Call
          ▼                           ▼
┌──────────────────────┐    ┌─────────────────────────────────┐
│ GOVERNMENT WEBSITES  │    │          GROQ AI SERVICE       │
├──────────────────────┤    ├─────────────────────────────────┤
│ • pmay.gov.in        │    │  ┌─────────────────┐            │
│ • mygov.in           │    │  │ Mixtral-8x7B    │            │
│ • janaushadhi.gov.in │    │  │ Language Model  │            │
│ • nsap.nic.in        │    │  └─────────────────┘            │
│ • pmkisan.gov.in     │    │  ┌─────────────────┐            │
│ • ayushmanbharat.    │    │  │  Language       │            │
│   pm.gov.in          │    │  │  Generation     │            │
│ • mksy.gov.in        │    │  └─────────────────┘            │
│ • 15+ More Sites     │    │                                 │
└──────────────────────┘    └─────────────────────────────────┘
```

### Data Flow Diagram

```
    User Input
        │
        ▼
┌─────────────────┐
│   Voice/Text    │ ◄──── Language Selection
│     Input       │
└─────────────────┘
        │
        ▼
┌─────────────────┐
│ Speech-to-Text  │ ◄──── Web Speech API
│   Conversion    │       (if voice input)
└─────────────────┘
        │
        ▼
┌─────────────────┐
│ Query Processing│ ◄──── Keyword Matching
│   & Analysis    │       Category Detection
└─────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│        REAL-TIME SCRAPING           │
│                                     │
│ 1. Identify relevant gov websites   │
│ 2. Deploy multiple scrapers         │
│ 3. Extract fresh scheme data        │
│ 4. Parse and validate content       │
│ 5. Combine data from all sources    │
└─────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│     AI ENHANCEMENT                  │
│                                     │
│ • Combine scraped data with AI      │
│ • Add context and explanations      │
│ • Format in selected language       │
│ • Provide application guidance      │
└─────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│    Text-to-Speech Synthesis         │ ◄──── Voice Selection
│    (if voice output enabled)        │       Language Matching
└─────────────────────────────────────┘
        │
        ▼
         Display Result
```

### Component Architecture

```
Frontend Components:
├── Language Selector
├── Input Mode Toggle (Voice/Text)
├── Voice Interface
│   ├── Microphone Button
│   ├── Voice Status Display
│   └── Voice Controls (Stop/Replay)
├── Text Interface
│   ├── Text Input Field
│   └── Send Button
├── Response Display
│   ├── AI Response Container
│   ├── Source Indicator (Live Scraped)
│   └── Speech Controls
└── Sample Questions

Backend Components:
├── Flask Application (app.py)
├── Route Handlers
│   ├── Index Route (/)
│   └── Query Route (/query)
├── Real-time Web Scraper Engine
│   ├── Government Website Scrapers
│   ├── Content Parser
│   └── Data Validator
├── Query Processor
│   ├── Language Detection
│   ├── Keyword Matching
│   └── Category Classification
├── AI Integration
│   ├── Groq Client
│   └── Response Formatter
└── Session Management
```

---

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- Modern web browser with Speech API support
- Groq API key

### Quick Start

1. **Clone the repository**
   ```bash
   git clone SimranShaikh20/Sarkari-Yojna-Sahayak
   cd sarkari-yojana-sahayak
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export GROQ_API_KEY="your_groq_api_key_here"
   export SESSION_SECRET="your_session_secret_here"
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

### Dependencies

```
Flask>=2.0.0
groq>=0.4.0
requests>=2.25.0
beautifulsoup4>=4.10.0
lxml>=4.6.0
gunicorn>=20.0.0
```

---

## 📱 Usage

### Voice Input Mode
1. **Select Language**: Choose from Hindi, English, or Gujarati
2. **Click Microphone**: Press the microphone button to start recording
3. **Speak Clearly**: Ask your question about government schemes
4. **Real-time Data**: System scrapes live data from government websites
5. **Listen to Response**: The AI will respond with fresh information in your selected language
6. **Use Controls**: Stop, replay, or pause the voice response

### Text Input Mode
1. **Switch to Text Mode**: Click the "Text Input" toggle button
2. **Type Question**: Enter your question in the text field
3. **Submit**: Press Enter or click the send button
4. **Live Scraping**: Watch as system fetches fresh data from official sources
5. **Read Response**: View the response with live scraped data and voice playback option

### Sample Questions
- **Hindi**: "प्रधानमंत्री आवास योजना के बारे में बताएं"
- **English**: "Tell me about pension schemes for elderly"
- **Gujarati**: "મને સ્વાસ્થ્य યોજનાઓ વિશે જણાવો"

---

## 🔌 API Reference

### POST /query

Submit a query about government schemes (with real-time scraping).

**Request Body:**
```json
{
  "query": "pension scheme information",
  "language": "hindi"
}
```

**Response:**
```json
{
  "response": "योजना का नाम: राष्ट्रीय सामाजिक सहायता कार्यक्रम... (scraped from nsap.nic.in)",
  "language": "hindi",
  "source": "live_scraped",
  "scraped_from": ["nsap.nic.in", "mygov.in"],
  "scraped_at": "2024-01-15T10:30:00Z"
}
```

**Parameters:**
- `query` (string): User's question about government schemes
- `language` (string): Response language - "english", "hindi", or "gujarati"

**Response Fields:**
- `response` (string): Detailed information about the scheme (from live scraped data)
- `language` (string): Language of the response
- `source` (string): "live_scraped" for real-time data, "ai" for AI-enhanced responses
- `scraped_from` (array): List of government websites scraped for the response
- `scraped_at` (string): Timestamp when data was scraped

---

## 📊 Government Schemes Database (Real-time Scraped)

### Supported Categories
- 🌾 **Agriculture**: Farmer welfare, crop insurance, subsidies
- 🏠 **Housing**: Home construction, urban development
- 🏥 **Health**: Medical insurance, healthcare programs
- 👩 **Women**: Maternity benefits, girl child schemes
- 👴 **Social Security**: Pension schemes, elderly care
- 🎓 **Education**: Scholarships, skill development

### Real-time Data Sources
All scheme information is scraped live from official government websites:
- **pmay.gov.in** - Pradhan Mantri Awas Yojana
- **mygov.in** - Central Government Schemes Portal
- **janaushadhi.gov.in** - PM Bharatiya Janaushadhi Pariyojana
- **nsap.nic.in** - National Social Assistance Programme
- **pmkisan.gov.in** - PM-KISAN Farmer Benefit Scheme
- **ayushmanbharat.pm.gov.in** - Ayushman Bharat Health Scheme
- **mksy.gov.in** - Employment Guarantee Schemes
- **Ministry of Rural Development** - Rural development schemes
- **Ministry of Health and Family Welfare** - Healthcare programs
- **Ministry of Women and Child Development** - Women and child welfare
- **Ministry of Agriculture and Farmers Welfare** - Agricultural schemes
- **Ministry of Housing and Urban Affairs** - Housing and urban development
- **Ministry of Education** - Educational schemes and scholarships
- **15+ Additional Official Government Portals**

### Scraping Features
- **Real-time Extraction**: Fresh data scraped for every user query
- **Multi-source Aggregation**: Combines information from multiple official sources
- **Data Validation**: Ensures authenticity by cross-referencing multiple sources
- **Language Processing**: Automatically translates scraped content to user's preferred language
- **Content Parsing**: Intelligently extracts scheme details, eligibility, and application processes

---

## 🎨 UI/UX Features

### Design Elements
- **Glassmorphism Effects**: Translucent containers with backdrop blur
- **Gradient Backgrounds**: Dynamic color schemes
- **Responsive Typography**: Adaptive font sizes and spacing
- **Interactive Animations**: Hover effects and transitions
- **Live Data Indicators**: Visual cues showing real-time scraping status
- **Accessibility**: High contrast modes and screen reader support

### Browser Compatibility
- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+
- ⚠️ Internet Explorer (Not supported)

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Groq API key for AI responses | Yes |
| `SESSION_SECRET` | Flask session secret key | Yes |
| `FLASK_ENV` | Environment mode (development/production) | No |
| `PORT` | Application port (default: 5000) | No |

### Voice Configuration
The application automatically detects and configures the best available voices for each language:

- **Hindi**: Prefers `hi-IN` voices, falls back to `en-IN`
- **Gujarati**: Uses `hi-IN` voices for better pronunciation
- **English**: Prefers `en-IN` voices, falls back to `en-US`

---

## 🚀 Deployment

### Render Deployment
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set the following configuration:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT main:app`
4. Add environment variables in Render dashboard:
   - `GROQ_API_KEY`: Your Groq API key
   - `SESSION_SECRET`: Your session secret key
5. Deploy and get your live URL

### Local Development
```bash
python main.py
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide for Python code
- Use ES6+ features for JavaScript
- Maintain responsive design principles
- Add appropriate comments and documentation
- Test voice features across different browsers
- Ensure web scraping follows ethical practices and respects robots.txt

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Groq AI** for providing the language model API
- **Government of India** for making scheme data publicly available
- **Web Speech API** for enabling voice recognition and synthesis
- **Font Awesome** for beautiful icons
- **Flask Community** for the excellent web framework

---


<div align="center">

**Built with ❤️ for the people of India**

*Empowering citizens with easy access to real-time government scheme information*

</div>