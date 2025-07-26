# Sarkari Yojana Sahayak (सरकारी योजना सहायक)

## Overview

Sarkari Yojana Sahayak is a multilingual, voice-enabled AI assistant web application designed to help users discover and understand Indian government schemes. The application supports Hindi, English, and Gujarati languages with complete voice interaction capabilities, allowing users to speak their queries and receive spoken responses about various government welfare programs.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a simple client-server architecture with a Flask backend serving a single-page application (SPA) frontend. The system integrates multiple APIs and services to provide a seamless multilingual voice experience.

### Frontend Architecture
- **Technology Stack**: Vanilla JavaScript, HTML5, CSS3
- **Voice Integration**: Web Speech API for both speech recognition and text-to-speech
- **UI Framework**: Custom CSS with responsive design and glassmorphism effects
- **Language Support**: Dynamic language switching with appropriate font support for Devanagari and Gujarati scripts

### Backend Architecture
- **Framework**: Flask (Python)
- **API Structure**: RESTful endpoints for scheme queries and AI responses
- **Session Management**: Flask sessions with configurable secret key
- **Logging**: Python logging module for debugging and monitoring

## Key Components

### 1. Voice Interface
- **Speech Recognition**: Browser-native Web Speech API supporting hi-IN, en-IN, and gu-IN
- **Text-to-Speech**: SpeechSynthesisUtterance for natural voice responses
- **Recording Management**: Visual feedback with pulse animations during voice capture

### 2. Language System
- **Multi-language Support**: Complete language switching affecting UI, voice recognition, and AI responses
- **Dynamic Content**: Language-specific sample questions and system prompts
- **Font Support**: Appropriate font stacks for different scripts

### 3. AI Integration
- **LLM Provider**: Groq API with Mixtral model
- **Context Awareness**: Language-specific system prompts for accurate responses
- **Fallback Strategy**: Local scheme data takes precedence over AI responses

### 4. Scheme Database
- **Data Source**: Local JSON file (schemes.json) containing government scheme information
- **Schema Structure**: Standardized fields including scheme_name, description, eligibility, benefits, how_to_apply, official_link, and category
- **Categories**: agriculture, housing, health, women, social_security, education

## Data Flow

1. **User Interaction**: User selects language and initiates voice input
2. **Speech Processing**: Web Speech API converts voice to text in selected language
3. **Query Processing**: Backend receives query and checks local scheme database first
4. **AI Processing**: If no local match, query is sent to Groq API with language-specific system prompt
5. **Response Generation**: AI generates response in requested language
6. **Voice Output**: Frontend converts text response to speech using appropriate voice

## External Dependencies

### APIs and Services
- **Groq API**: Primary AI service for generating intelligent responses about government schemes
- **Web Speech API**: Browser-native API for voice recognition and synthesis

### Frontend Libraries
- **Font Awesome**: Icon library for UI elements
- **Google Fonts**: Potential integration for better multilingual typography

### Python Packages
- **Flask**: Web framework for backend API
- **Groq**: Official client library for Groq API integration
- **Requests**: HTTP library for potential external API calls

## Deployment Strategy

### Environment Configuration
- **API Keys**: Groq API key stored in environment variables
- **Session Security**: Configurable session secret key
- **Development Mode**: Flask debug mode enabled for development

### Hosting Requirements
- **Python Runtime**: Flask application requiring Python 3.7+
- **Static File Serving**: CSS, JavaScript, and JSON files served through Flask
- **Port Configuration**: Configurable port (default 5000) with host binding

### Security Considerations
- **API Key Management**: Environment-based API key storage
- **Session Management**: Secure session handling with proper secret key
- **CORS**: May require CORS configuration for production deployment

### Scalability Considerations
- **Stateless Design**: Application designed to be stateless for easy horizontal scaling
- **Local Data**: Scheme data stored locally to reduce external API dependencies
- **Caching Strategy**: Potential for implementing response caching to improve performance

The application is designed to be easily deployable on platforms like Replit, Heroku, or similar cloud platforms with minimal configuration requirements.