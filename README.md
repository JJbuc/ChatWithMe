# chud.ai - AI Creator Platform

A modern web application that allows users to chat with AI creators powered by AWS Bedrock (Claude-3-Sonnet).

## Features

- 🏠 **Home Page**: Choose your role (User or Creator)
- 👥 **Creator Selection**: Browse and search through AI creators
- 💬 **Chat Interface**: Real-time chat with AI creators
- 🔍 **Smart Search**: Type-ahead search with suggestions
- 🎨 **Modern UI**: Beautiful gradient design with animations
- 🤖 **AWS Bedrock Integration**: Powered by Claude-3-Sonnet
- 📱 **Responsive Design**: Works on desktop and mobile

## Quick Start

1. **Install Dependencies**:
   ```bash
   conda activate base
   pip install -r requirements.txt
   ```

2. **Start the Server**:
   ```bash
   python server.py
   ```

3. **Open in Browser**:
   ```
   http://localhost:5001
   ```

## How to Use

1. **Choose Role**: Click "I'm a User" on the home page
2. **Select Creator**: Browse creators or use the search bar
3. **Start Chatting**: Click on any creator to start a conversation
4. **Type Messages**: Use the chat input to send messages
5. **Get AI Responses**: Receive intelligent responses from your chosen creator

## Available Creators

- 🤖 **Alex Chen** - AI & Machine Learning Expert
- ✍️ **Sarah Johnson** - Creative Writing Specialist  
- 💼 **Marcus Rodriguez** - Business Strategy Consultant
- 📊 **Emma Wilson** - Data Science Expert
- 💻 **David Kim** - Software Development Specialist

## API Endpoints

- `GET /` - Main application
- `POST /api/chat` - Chat with AI creators
- `GET /api/health` - Health check
- `GET /api/creators` - Get creators list

## Technical Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Flask (Python)
- **AI**: AWS Bedrock (Claude-3-Sonnet)
- **Styling**: Custom CSS with gradients and animations

## Deployment

The application is ready for deployment on:
- AWS S3 + CloudFront
- AWS EC2
- AWS Amplify
- Heroku
- Any Python hosting platform

## Debugging

Open browser console (F12) to see detailed logs and use `debugApp()` function for debugging information.

## License

MIT License
