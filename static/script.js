// Global variables
let recognition;
let isRecording = false;
let currentLanguage = 'english';
let synthesis = window.speechSynthesis;
let currentUtterance = null;

// Language configurations
const LANGUAGES = {
    'hindi': {
        'code': 'hi-IN',
        'voice_lang': 'hi-IN',
        'name': 'हिंदी'
    },
    'english': {
        'code': 'en-IN',
        'voice_lang': 'en-IN', 
        'name': 'English'
    },
    'gujarati': {
        'code': 'gu-IN',
        'voice_lang': 'gu-IN',
        'name': 'ગુજરાતી'
    }
};

// Sample questions by language
const SAMPLE_QUESTIONS = {
    'hindi': [
        'मुझे पीएम किसान योजना की जानकारी चाहिए',
        'विधवा पेंशन योजना क्या है',
        'किसानों के लिए कौन सी सरकारी योजनाएं हैं',
        'आयुष्मान भारत योजना के बारे में बताइए',
        'गर्भवती महिलाओं के लिए योजना',
        'मकान बनाने के लिए सरकारी सहायता'
    ],
    'english': [
        'Tell me about PM Kisan scheme',
        'What is widow pension scheme',
        'Government schemes for farmers',
        'Scholarships for girls education',
        'Housing schemes for poor families',
        'Health insurance schemes'
    ],
    'gujarati': [
        'પીએમ કિસાન યોજના વિશે જણાવો',
        'વિધવા પેન્શન યોજના શું છે',
        'ખેડૂતો માટે સરકારી યોજનાઓ',
        'આયુષ્માન ભારત વિશે માહિતી',
        'ગર્ભવતી મહિલાઓ માટે યોજના',
        'ગરીબ પરિવારો માટે મકાન યોજના'
    ]
};

// DOM elements
const micBtn = document.getElementById('mic-btn');
const recordingIndicator = document.getElementById('recording-indicator');
const voiceStatus = document.getElementById('voice-status');
const languageSelect = document.getElementById('language-select');
const userMessage = document.getElementById('user-message');
const userText = document.getElementById('user-text');
const aiMessage = document.getElementById('ai-message');
const aiText = document.getElementById('ai-text');
const sourceIndicator = document.getElementById('source-indicator');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('error-message');
const errorText = document.getElementById('error-text');
const speakBtn = document.getElementById('speak-btn');
const sampleButtons = document.querySelectorAll('.sample-btn');

// Initialize speech recognition
function initSpeechRecognition() {
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;
        
        recognition.onstart = function() {
            isRecording = true;
            micBtn.classList.add('recording');
            recordingIndicator.classList.add('show');
            voiceStatus.textContent = getLocalizedText('listening');
            hideError();
        };
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            handleVoiceInput(transcript);
        };
        
        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            showError(getLocalizedText('speechError'));
            stopRecording();
        };
        
        recognition.onend = function() {
            stopRecording();
        };
        
    } else {
        showError('Speech recognition is not supported in this browser. Please use Chrome or Edge.');
        micBtn.disabled = true;
    }
}

// Get localized text
function getLocalizedText(key) {
    const texts = {
        'listening': {
            'hindi': 'सुन रहा हूं...',
            'english': 'Listening...',
            'gujarati': 'સાંભળી રહ્યો છું...'
        },
        'clickToSpeak': {
            'hindi': 'बोलने के लिए माइक्रोफोन दबाएं',
            'english': 'Click the microphone to ask about government schemes',
            'gujarati': 'સરકારી યોજનાઓ વિશે પૂછવા માટે માઇક્રોફોન દબાવો'
        },
        'speechError': {
            'hindi': 'आवाज पहचानने में समस्या है। कृपया फिर कोशिश करें।',
            'english': 'Speech recognition error. Please try again.',
            'gujarati': 'અવાજ ઓળખવામાં સમસ્યા છે. કૃપા કરીને ફરીથી પ્રયાસ કરો.'
        },
        'processing': {
            'hindi': 'आपके प्रश्न को संसाधित कर रहे हैं...',
            'english': 'Processing your question...',
            'gujarati': 'તમારા પ્રશ્નને પ્રક્રિયા કરી રહ્યા છીએ...'
        },
        'localSource': {
            'hindi': 'स्थानीय डेटा से जानकारी',
            'english': 'Information from local data',
            'gujarati': 'સ્થાનિક ડેટામાંથી માહિતી'
        },
        'aiSource': {
            'hindi': 'AI सहायक से जानकारी',
            'english': 'Information from AI assistant',
            'gujarati': 'AI સહાયકમાંથી માહિતી'
        }
    };
    
    return texts[key] ? texts[key][currentLanguage] : texts[key]?.['english'] || key;
}

// Start recording
function startRecording() {
    if (recognition && !isRecording) {
        recognition.lang = LANGUAGES[currentLanguage].code;
        try {
            recognition.start();
        } catch (error) {
            console.error('Error starting recognition:', error);
            showError(getLocalizedText('speechError'));
        }
    }
}

// Stop recording
function stopRecording() {
    isRecording = false;
    micBtn.classList.remove('recording');
    recordingIndicator.classList.remove('show');
    voiceStatus.textContent = getLocalizedText('clickToSpeak');
}

// Handle voice input
function handleVoiceInput(transcript) {
    console.log('Voice input:', transcript);
    displayUserMessage(transcript);
    processQuery(transcript);
}

// Display user message
function displayUserMessage(text) {
    userText.textContent = text;
    userMessage.style.display = 'block';
    scrollToBottom();
}

// Process query
async function processQuery(query) {
    showLoading();
    hideError();
    
    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                language: currentLanguage
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        hideLoading();
        
        if (data.error) {
            showError(data.error);
        } else {
            displayAIResponse(data.response, data.source);
        }
        
    } catch (error) {
        hideLoading();
        console.error('Error processing query:', error);
        showError('Failed to process your query. Please try again.');
    }
}

// Display AI response
function displayAIResponse(response, source) {
    aiText.textContent = response;
    
    // Update source indicator
    const sourceText = source === 'local' ? getLocalizedText('localSource') : getLocalizedText('aiSource');
    sourceIndicator.textContent = `📍 ${sourceText}`;
    
    aiMessage.style.display = 'block';
    scrollToBottom();
    
    // Auto-speak the response with a slight delay to ensure DOM is ready
    setTimeout(() => {
        speakText(response);
    }, 500);
}

// Text-to-speech function
function speakText(text) {
    console.log('Attempting to speak text:', text);
    console.log('Current language:', currentLanguage);
    
    // Stop any current speech
    if (synthesis.speaking) {
        synthesis.cancel();
    }
    
    if (text && text.trim()) {
        // Wait a moment for voices to be available
        setTimeout(() => {
            currentUtterance = new SpeechSynthesisUtterance(text);
            currentUtterance.lang = LANGUAGES[currentLanguage].voice_lang;
            currentUtterance.rate = 0.8;
            currentUtterance.pitch = 1;
            currentUtterance.volume = 1;
            
            // Get all available voices
            const voices = synthesis.getVoices();
            console.log('Available voices:', voices.length);
            
            const targetLang = LANGUAGES[currentLanguage].voice_lang;
            console.log('Target language:', targetLang);
            
            // Try to find the best voice for the language
            let voice = null;
            
            // First try exact match
            voice = voices.find(v => v.lang === targetLang);
            
            // If no exact match, try language prefix (e.g., 'hi' from 'hi-IN')
            if (!voice) {
                const langPrefix = targetLang.split('-')[0];
                voice = voices.find(v => v.lang.startsWith(langPrefix));
            }
            
            // If still no match, try to find any voice that contains the language
            if (!voice) {
                const langPrefix = targetLang.split('-')[0];
                voice = voices.find(v => v.lang.toLowerCase().includes(langPrefix));
            }
            
            // For Hindi, also try 'en-IN' as fallback
            if (!voice && currentLanguage === 'hindi') {
                voice = voices.find(v => v.lang === 'en-IN' || v.lang.startsWith('en'));
            }
            
            // Default to any available voice if none found
            if (!voice && voices.length > 0) {
                voice = voices[0];
            }
            
            if (voice) {
                currentUtterance.voice = voice;
                console.log('Selected voice:', voice.name, voice.lang);
            } else {
                console.log('No suitable voice found, using default');
            }
            
            currentUtterance.onstart = function() {
                console.log('Speech started');
                speakBtn.innerHTML = '<i class="fas fa-stop"></i>';
                speakBtn.title = 'Stop speaking';
            };
            
            currentUtterance.onend = function() {
                console.log('Speech ended');
                speakBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
                speakBtn.title = 'Listen to response';
            };
            
            currentUtterance.onerror = function(event) {
                console.error('Speech error:', event.error);
                speakBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
                speakBtn.title = 'Listen to response';
            };
            
            // Try to speak
            try {
                synthesis.speak(currentUtterance);
                console.log('Speech synthesis started');
            } catch (error) {
                console.error('Error starting speech synthesis:', error);
            }
        }, 100);
    } else {
        console.log('No text to speak');
    }
}

// Show loading
function showLoading() {
    loading.style.display = 'block';
    loading.querySelector('span').textContent = getLocalizedText('processing');
    scrollToBottom();
}

// Hide loading
function hideLoading() {
    loading.style.display = 'none';
}

// Show error
function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'flex';
    scrollToBottom();
}

// Hide error
function hideError() {
    errorMessage.style.display = 'none';
}

// Scroll to bottom
function scrollToBottom() {
    setTimeout(() => {
        window.scrollTo({
            top: document.body.scrollHeight,
            behavior: 'smooth'
        });
    }, 100);
}

// Update sample questions based on language
function updateSampleQuestions() {
    const questions = SAMPLE_QUESTIONS[currentLanguage];
    sampleButtons.forEach((btn, index) => {
        if (questions[index]) {
            btn.setAttribute('data-question', questions[index]);
            // Update button text (keep icon, update text)
            const icon = btn.querySelector('i');
            const iconClass = icon.className;
            btn.innerHTML = `<i class="${iconClass}"></i>${questions[index]}`;
        }
    });
}

// Event listeners
micBtn.addEventListener('click', () => {
    if (isRecording) {
        recognition.stop();
    } else {
        startRecording();
    }
});

languageSelect.addEventListener('change', (e) => {
    currentLanguage = e.target.value;
    voiceStatus.textContent = getLocalizedText('clickToSpeak');
    updateSampleQuestions();
    
    // Update recognition language if recording
    if (recognition) {
        recognition.lang = LANGUAGES[currentLanguage].code;
    }
});

speakBtn.addEventListener('click', () => {
    if (synthesis.speaking) {
        synthesis.cancel();
    } else {
        const text = aiText.textContent;
        if (text) {
            speakText(text);
        }
    }
});

// Sample question buttons
sampleButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const question = btn.getAttribute('data-question');
        if (question) {
            displayUserMessage(question);
            processQuery(question);
        }
    });
});

// Initialize voices for TTS
function initializeVoices() {
    const voices = synthesis.getVoices();
    console.log('Initializing voices. Available:', voices.length);
    
    if (voices.length === 0) {
        // Voices not loaded yet, wait for them
        if (synthesis.onvoiceschanged !== undefined) {
            synthesis.onvoiceschanged = () => {
                const newVoices = synthesis.getVoices();
                console.log('Voices loaded:', newVoices.length);
                if (newVoices.length > 0) {
                    console.log('Voice samples:', newVoices.slice(0, 5).map(v => `${v.name} (${v.lang})`));
                }
            };
        }
    } else {
        console.log('Voice samples:', voices.slice(0, 5).map(v => `${v.name} (${v.lang})`));
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    initSpeechRecognition();
    updateSampleQuestions();
    initializeVoices();
    
    // Set initial status
    voiceStatus.textContent = getLocalizedText('clickToSpeak');
});

// Handle page visibility changes (pause speech when tab is hidden)
document.addEventListener('visibilitychange', () => {
    if (document.hidden && synthesis.speaking) {
        synthesis.pause();
    } else if (!document.hidden && synthesis.paused) {
        synthesis.resume();
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Space bar to start/stop recording
    if (e.code === 'Space' && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
        e.preventDefault();
        if (isRecording) {
            recognition.stop();
        } else {
            startRecording();
        }
    }
    
    // Escape to stop speech
    if (e.code === 'Escape' && synthesis.speaking) {
        synthesis.cancel();
    }
});
