// Global state
let currentUserType = null;
let currentCreator = null;
let chatHistory = [];
let sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);

// Creator data
const CREATORS = [
    { id: 1, name: "Marques Brownlee", specialty: "\"MKBHD\"", avatar: "photos/Marques_Brownlee.jpg", description: "Tech reviewer and YouTuber known for in-depth smartphone and gadget reviews." },
    { id: 2, name: "Austin Evans", specialty: "\"Austin Evans\"", avatar: "photos/AustinEvans.jpeg", description: "Tech YouTuber specializing in PC builds, gaming hardware, and tech reviews." },
    { id: 3, name: "Justine Ezarik", specialty: "\"iJustine\"", avatar: "photos/justine-ezarik.jpg", description: "Tech YouTuber and Apple enthusiast known for unboxing videos and tech reviews." },
    { id: 4, name: "Zack Nelson", specialty: "\"JerryRigEverything\"", avatar: "photos/Zack Nelson.jpeg", description: "Tech YouTuber famous for durability tests and smartphone teardowns." },
    { id: 5, name: "Lewis George Hilsenteger", specialty: "\"Unbox Therapy\"", avatar: "photos/Lewis George Hilsenteger.jpg", description: "Tech YouTuber known for unboxing videos and tech product reviews." }
];

// DOM elements
let homePage, creatorPage, chatPage;
let creatorSearch, searchSuggestions, creatorsGrid;
let messageInput, sendMessageBtn, chatMessages, loadingOverlay;

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM loaded, initializing app...');
    
    // Get DOM elements
    homePage = document.getElementById('homePage');
    creatorPage = document.getElementById('creatorPage');
    chatPage = document.getElementById('chatPage');
    creatorSearch = document.getElementById('creatorSearch');
    searchSuggestions = document.getElementById('searchSuggestions');
    creatorsGrid = document.getElementById('creatorsGrid');
    messageInput = document.getElementById('messageInput');
    sendMessageBtn = document.getElementById('sendMessageBtn');
    chatMessages = document.getElementById('chatMessages');
    loadingOverlay = document.getElementById('loadingOverlay');
    
    // Verify all elements exist
    const elements = { homePage, creatorPage, chatPage, creatorSearch, searchSuggestions, creatorsGrid, messageInput, sendMessageBtn, chatMessages, loadingOverlay };
    for (const [name, element] of Object.entries(elements)) {
        if (!element) {
            console.error(`❌ Element not found: ${name}`);
        } else {
            console.log(`✅ Element found: ${name}`);
        }
    }
    
    // Initialize app
    initializeApp();
});

function initializeApp() {
    console.log('🔧 Initializing app...');
    
    // Show home page by default
    showPage('home');
    
    // Set up event listeners
    setupEventListeners();
    
    // Populate creators grid
    populateCreatorsGrid();
    
    // Make functions globally accessible
    window.showPage = showPage;
    window.selectRole = selectRole;
    window.selectCreator = selectCreator;
    window.sendMessage = sendMessage;
    window.populateCreatorsGrid = populateCreatorsGrid;
    
    console.log('✅ App initialized successfully');
}

function setupEventListeners() {
    console.log('🎧 Setting up event listeners...');
    
    // Search functionality
    if (creatorSearch) {
        creatorSearch.addEventListener('input', handleCreatorSearch);
        creatorSearch.addEventListener('focus', () => {
            if (creatorSearch.value.length > 0) {
                searchSuggestions.style.display = 'block';
            }
        });
        creatorSearch.addEventListener('blur', () => {
            setTimeout(() => {
                searchSuggestions.style.display = 'none';
            }, 200);
        });
    }
    
    // Message input
    if (messageInput) {
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
    
    // Send message button
    if (sendMessageBtn) {
        sendMessageBtn.addEventListener('click', sendMessage);
    }
    
    console.log('✅ Event listeners set up');
}

function showPage(pageName) {
    console.log(`🔄 Showing page: ${pageName}`);
    
    // Hide all pages
    const pages = [homePage, creatorPage, chatPage];
    pages.forEach(page => {
        if (page) {
            page.classList.remove('active');
        }
    });
    
    // Show selected page
    let targetPage;
    switch(pageName) {
        case 'home':
            targetPage = homePage;
            break;
        case 'creator':
            targetPage = creatorPage;
            break;
        case 'chat':
            targetPage = chatPage;
            break;
        default:
            console.error(`❌ Unknown page: ${pageName}`);
            return;
    }
    
    if (targetPage) {
        targetPage.classList.add('active');
        console.log(`✅ Page shown: ${pageName}`);
        
        // Special handling for creator page
        if (pageName === 'creator') {
            setTimeout(() => {
                populateCreatorsGrid();
            }, 100);
        }
    } else {
        console.error(`❌ Target page not found: ${pageName}`);
    }
}

function selectRole(role) {
    console.log(`🎯 Role selected: ${role}`);
    currentUserType = role;
    
    if (role === 'user') {
        showPage('creator');
    } else if (role === 'creator') {
        alert('Creator mode coming soon!');
    }
}

function selectCreator(creatorId) {
    console.log(`🎯 Creator selected: ${creatorId}`);
    
    // Find creator
    const creator = CREATORS.find(c => c.id === creatorId);
    if (!creator) {
        console.error(`❌ Creator not found: ${creatorId}`);
        alert('Creator not found!');
        return;
    }
    
    currentCreator = creator;
    console.log(`✅ Creator found: ${creator.name}`);
    
    // Reset session for new creator conversation
    sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    console.log(`🆕 New session started: ${sessionId}`);
    
    // Update chat interface
    updateChatInterface(creator);
    
    // Navigate to chat page
    showPage('chat');
    
    // Focus on message input
    setTimeout(() => {
        if (messageInput) {
            messageInput.focus();
        }
    }, 100);
}

function updateChatInterface(creator) {
    console.log(`🔄 Updating chat interface for: ${creator.name}`);
    
    // Update creator info in chat header
    const creatorAvatar = document.getElementById('creatorAvatar');
    const creatorName = document.getElementById('creatorName');
    const creatorSpecialty = document.getElementById('creatorSpecialty');
    const welcomeCreatorName = document.getElementById('welcomeCreatorName');
    const welcomeSpecialty = document.getElementById('welcomeSpecialty');
    
    if (creatorAvatar) {
        const avatarImg = creatorAvatar.querySelector('.avatar-img');
        if (avatarImg) {
            avatarImg.src = creator.avatar;
            avatarImg.alt = creator.name;
        }
    }
    if (creatorName) creatorName.textContent = creator.name;
    if (creatorSpecialty) creatorSpecialty.textContent = creator.specialty;
    if (welcomeCreatorName) welcomeCreatorName.textContent = creator.name;
    if (welcomeSpecialty) welcomeSpecialty.textContent = creator.specialty;
    
    // Clear previous chat messages except welcome
    if (chatMessages) {
        const welcomeMessage = chatMessages.querySelector('.welcome-message');
        chatMessages.innerHTML = '';
        if (welcomeMessage) {
            chatMessages.appendChild(welcomeMessage);
        }
    }
    
    // Reset chat history
    chatHistory = [];
    
    console.log('✅ Chat interface updated');
}

function populateCreatorsGrid() {
    console.log('🔄 Populating creators grid...');
    
    if (!creatorsGrid) {
        console.error('❌ Creators grid not found');
        return;
    }
    
    const creatorsHTML = CREATORS.map(creator => `
        <div class="creator-card" onclick="selectCreator(${creator.id})" data-creator-id="${creator.id}">
            <div class="creator-card-header">
                <div class="creator-card-avatar">
                    <img src="${creator.avatar}" alt="${creator.name}" class="creator-avatar-img">
                </div>
                <div class="creator-card-info">
                    <h3>${creator.name}</h3>
                    <p>${creator.specialty}</p>
                </div>
            </div>
        </div>
    `).join('');
    
    creatorsGrid.innerHTML = creatorsHTML;
    console.log(`✅ Creators grid populated with ${CREATORS.length} creators`);
}

function handleCreatorSearch() {
    const query = creatorSearch.value.toLowerCase().trim();
    console.log(`🔍 Searching for: "${query}"`);
    
    if (query.length === 0) {
        searchSuggestions.style.display = 'none';
        return;
    }
    
    // Filter creators
    const filteredCreators = CREATORS.filter(creator => 
        creator.name.toLowerCase().includes(query) ||
        creator.specialty.toLowerCase().includes(query) ||
        creator.description.toLowerCase().includes(query)
    );
    
    if (filteredCreators.length === 0) {
        searchSuggestions.innerHTML = '<div class="suggestion-item">No creators found</div>';
    } else {
        searchSuggestions.innerHTML = filteredCreators.map(creator => 
            `<div class="suggestion-item" onclick="selectCreator(${creator.id})">${creator.name}</div>`
        ).join('');
    }
    
    searchSuggestions.style.display = 'block';
}

function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;
    
    console.log(`💬 Sending message: "${message}" with session: ${sessionId}`);
    
    // Add user message to chat
    addMessageToChat('user', message);
    
    // Clear input
    messageInput.value = '';
    
    // Show loading
    showLoading();
    
    // Call API with conversation context
    callBedrockAPI(message, currentCreator)
        .then(response => {
            console.log('✅ API response received with context');
            addMessageToChat('ai', response);
        })
        .catch(error => {
            console.error('❌ API error:', error);
            addMessageToChat('ai', 'Sorry, I encountered an error. Please try again.');
        })
        .finally(() => {
            hideLoading();
        });
}

function addMessageToChat(role, content) {
    console.log(`📝 Adding ${role} message to chat`);
    
    if (!chatMessages) {
        console.error('❌ Chat messages container not found');
        return;
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    
    const avatar = role === 'user' ? 'U' : (currentCreator ? currentCreator.avatar : 'AI');
    
    if (role === 'user') {
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <button class="message-avatar-btn">U</button>
            </div>
            <div class="message-content">
                <p>${content}</p>
            </div>
        `;
    } else {
        // Get initials from creator name
        const initials = currentCreator ? currentCreator.name.split(' ').map(n => n[0]).join('') : 'AI';
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <button class="message-avatar-btn">${initials}</button>
            </div>
            <div class="message-content">
                <div class="formatted-content">${formatMarkdown(content)}</div>
            </div>
        `;
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Add to chat history
    chatHistory.push({ role, content });
}

function formatMarkdown(text) {
    // Convert markdown to HTML
    return text
        // Links [text](url) - must be first before other formatting
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
        // Bold text **text** or __text__
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/__(.*?)__/g, '<strong>$1</strong>')
        // Italic text *text* or _text_
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/_(.*?)_/g, '<em>$1</em>')
        // Code `text`
        .replace(/`(.*?)`/g, '<code>$1</code>')
        // Line breaks
        .replace(/\n/g, '<br>')
        // Lists - convert * to bullet points
        .replace(/^\* (.+)$/gm, '<li>$1</li>')
        // Wrap consecutive list items in ul
        .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
        // Headers # ## ###
        .replace(/^### (.+)$/gm, '<h3>$1</h3>')
        .replace(/^## (.+)$/gm, '<h2>$1</h2>')
        .replace(/^# (.+)$/gm, '<h1>$1</h1>');
}

function callBedrockAPI(message, creator) {
    console.log(`🌐 Calling Groq API for creator: ${creator.name} with session: ${sessionId}`);
    
    const systemPrompt = `You are ${creator.name}, a ${creator.specialty} expert. ${creator.description}. Respond as this character would, being helpful and knowledgeable in your field. Remember our conversation context and refer to previous messages when relevant.`;
    
    return fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: message,
            creator: creator.name,
            systemPrompt: systemPrompt,
            sessionId: sessionId  // Include session ID for conversation context
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        console.log(`💬 Context: ${data.messageCount} messages in session ${data.sessionId}`);
        return data.response;
    });
}

function showLoading() {
    console.log('⏳ Showing loading...');
    if (loadingOverlay) {
        loadingOverlay.classList.add('active');
    }
}

function hideLoading() {
    console.log('✅ Hiding loading...');
    if (loadingOverlay) {
        loadingOverlay.classList.remove('active');
    }
}

// Debug functions
window.debugApp = function() {
    console.log('🐛 Debug Info:');
    console.log('Current user type:', currentUserType);
    console.log('Current creator:', currentCreator);
    console.log('Chat history:', chatHistory);
    console.log('DOM elements:', {
        homePage: !!homePage,
        creatorPage: !!creatorPage,
        chatPage: !!chatPage,
        creatorsGrid: !!creatorsGrid,
        messageInput: !!messageInput
    });
};

console.log('📜 Script loaded successfully');
