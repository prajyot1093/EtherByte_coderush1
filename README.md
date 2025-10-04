# CMT - AI-Powered Research Paper Detection

A sophisticated Conference Management Toolkit (CMT) that uses AI to detect plagiarism, AI-generated content, and stylometric inconsistencies in academic papers.

## Features

- 🤖 **AI Content Detection**: Advanced entropy and perplexity analysis
- 📝 **Plagiarism Detection**: Cross-linguistic plagiarism detection
- ✍️ **Stylometric Analysis**: Per-student writing style fingerprinting
- 🌙 **Dark Mode**: Elegant light/dark theme switching
- 📱 **Mobile Responsive**: Works seamlessly on all devices
- 🔐 **User Authentication**: Secure JWT-based login system
- 📊 **Real-time Analytics**: Live dashboard with statistics
- 🎨 **Beautiful UI**: Modern animated interface with glassmorphism

## Live Demo

Visit: [Your deployed URL will be here]

## Technology Stack

- **Backend**: Flask, SQLAlchemy, JWT Authentication
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite
- **Deployment**: Railway/Heroku

## Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python backend/main.py`
4. Open: `http://localhost:5000`

## Usage

1. **Register**: Create a new account
2. **Login**: Access the dashboard
3. **Upload**: Submit papers for analysis
4. **Analyze**: Get AI detection, plagiarism, and style analysis
5. **Review**: View detailed reports and statistics

## API Endpoints

- `POST /register` - User registration
- `POST /login` - User authentication
- `POST /analyze-text` - Analyze submitted content
- `GET /stats` - Get analytics dashboard data
- `GET /recent` - Get recent submissions

## License

MIT License - Feel free to use for academic and research purposes.