# सरकारी योजना सहायक (Sarkari Yojana Sahayak)

<div align="center">

![Sarkari Yojana Sahayak](https://img.shields.io/badge/Sarkari%20Yojana-Sahayak-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-green?style=flat-square&logo=flask)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow?style=flat-square&logo=javascript)
![License](https://img.shields.io/badge/License-MIT-red?style=flat-square)

**A multilingual, voice-enabled AI assistant for Indian government schemes**

[Features](#features) • [Architecture](#architecture) • [Installation](#installation) • [Usage](#usage) • [API](#api)

</div>

---

## 🎯 Overview

Sarkari Yojana Sahayak is a comprehensive AI-powered web application designed to help users discover and understand Indian government schemes. The application supports **Hindi**, **English**, and **Gujarati** languages with complete voice interaction capabilities, allowing users to speak their queries and receive spoken responses about various government welfare programs.

### 🌟 Key Highlights
- 🗣️ **Voice Recognition & Text-to-Speech** in 3 languages
- 🤖 **AI-Powered Responses** using Groq Mixtral model
- 📊 **Authentic Government Data** from official sources
- 🎨 **Modern Glassmorphism UI** with responsive design
- 🔄 **Dual Input Methods** - Voice and Text input
- 🎯 **Pure Language Responses** - No language mixing

---

## 🚀 Features

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
- **Intelligent Fallback**: Local scheme data takes precedence over AI responses
- **Smart Query Processing**: Advanced keyword matching and categorization

### 💾 Government Schemes Database
- **Authentic Data**: Sourced from official government websites
- **Comprehensive Coverage**: Agriculture, Housing, Health, Women, Social Security, Education
- **Multilingual Content**: Scheme information in all three supported languages
- **Real-time Search**: Instant matching based on keywords and categories

### 🎨 User Interface
- **Glassmorphism Design**: Modern, translucent interface elements
- **Responsive Layout**: Works seamlessly on desktop and mobile devices
- **Dual Input Modes**: Toggle between voice and text input
- **Interactive Elements**: Hover effects, animations, and feedback
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
│  │ Local Schemes   │  │  Language       │                 │
│  │ Database (JSON) │  │  Processing     │                 │
│  └─────────────────┘  └─────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
                              │ External API Call
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    GROQ AI SERVICE                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐                 │
│  │ Mixtral-8x7B    │  │  Language       │                 │
│  │ Language Model  │  │  Generation     │                 │
│  └─────────────────┘  └─────────────────┘                 │
└─────────────────────────────────────────────────────────────┘
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
    ┌─────────┐    ┌─────────────────┐
    │ Local   │───▶│ Scheme Found?   │
    │Database │    │                 │
    │ Search  │    └─────────────────┘
    └─────────┘           │
                         ▼
                    ┌─────────┐
              Yes ◄─│ Match?  │─► No
                    └─────────┘
                         │               │
                         ▼               ▼
                ┌─────────────────┐ ┌─────────────────┐
                │ Return Local    │ │   Call Groq     │
                │ Scheme Data     │ │   AI Service    │
                └─────────────────┘ └─────────────────┘
                         │               │
                         └───────┬───────┘
                                 ▼
                ┌─────────────────────────────────┐
                │     Format Response in          │
                │    Selected Language            │
                └─────────────────────────────────┘
                                 │
                                 ▼
                ┌─────────────────────────────────┐
                │    Text-to-Speech Synthesis     │ ◄──── Voice Selection
                │    (if voice output enabled)    │       Language Matching
                └─────────────────────────────────┘
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
│   ├── Source Indicator
│   └── Speech Controls
└── Sample Questions

Backend Components:
├── Flask Application (app.py)
├── Route Handlers
│   ├── Index Route (/)
│   └── Query Route (/query)
├── Query Processor
│   ├── Language Detection
│   ├── Keyword Matching
│   └── Category Classification
├── Scheme Database Manager
│   ├── JSON Data Loader
│   └── Search Engine
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
   git clone <repository-url>
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
gunicorn>=20.0.0
```

---

## 📱 Usage

### Voice Input Mode
1. **Select Language**: Choose from Hindi, English, or Gujarati
2. **Click Microphone**: Press the microphone button to start recording
3. **Speak Clearly**: Ask your question about government schemes
4. **Listen to Response**: The AI will respond in your selected language
5. **Use Controls**: Stop, replay, or pause the voice response

### Text Input Mode
1. **Switch to Text Mode**: Click the "Text Input" toggle button
2. **Type Question**: Enter your question in the text field
3. **Submit**: Press Enter or click the send button
4. **Read Response**: View the response with voice playback option

### Sample Questions
- **Hindi**: "प्रधानमंत्री आवास योजना के बारे में बताएं"
- **English**: "Tell me about pension schemes for elderly"
- **Gujarati**: "મને સ્વાસ્થ્य યોજનાઓ વિશે જણાવો"

---

## 🔌 API Reference

### POST /query

Submit a query about government schemes.

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
  "response": "योजना का नाम: राष्ट्रीय सामाजिक सहायता कार्यक्रम...",
  "language": "hindi",
  "source": "local"
}
```

**Parameters:**
- `query` (string): User's question about government schemes
- `language` (string): Response language - "english", "hindi", or "gujarati"

**Response Fields:**
- `response` (string): Detailed information about the scheme
- `language` (string): Language of the response
- `source` (string): Data source - "local" for database, "ai" for Groq API

---

## 📊 Government Schemes Database

### Supported Categories
- 🌾 **Agriculture**: Farmer welfare, crop insurance, subsidies
- 🏠 **Housing**: Home construction, urban development
- 🏥 **Health**: Medical insurance, healthcare programs
- 👩 **Women**: Maternity benefits, girl child schemes
- 👴 **Social Security**: Pension schemes, elderly care
- 🎓 **Education**: Scholarships, skill development

### Data Sources
All scheme information is sourced from official government websites:
- Ministry of Rural Development
- Ministry of Health and Family Welfare
- Ministry of Women and Child Development
- Ministry of Agriculture and Farmers Welfare
- Ministry of Housing and Urban Affairs
- Ministry of Education

---

## 🎨 UI/UX Features

### Design Elements
- **Glassmorphism Effects**: Translucent containers with backdrop blur
- **Gradient Backgrounds**: Dynamic color schemes
- **Responsive Typography**: Adaptive font sizes and spacing
- **Interactive Animations**: Hover effects and transitions
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

### Replit Deployment
1. Import the project to Replit
2. Set environment variables in Secrets
3. Click "Deploy" button for public access

### Local Production
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
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

## 📞 Support

For support, questions, or feature requests:

- 📧 Email: support@sarkariyojana.com
- 🐛 Issues: [GitHub Issues](issues)
- 💬 Discussions: [GitHub Discussions](discussions)

---

<div align="center">

**Built with ❤️ for the people of India**

*Empowering citizens with easy access to government scheme information*

</div>