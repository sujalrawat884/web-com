# MLSC MGMCOET Community Website

A modern, responsive website for the Microsoft Learn Student Community at MGMCOET, built with FastAPI and TailwindCSS.

## 🚀 Features

- **Modern Design**: Clean, responsive design with TailwindCSS
- **Fast Performance**: Built with FastAPI for optimal speed
- **Dynamic Content**: Event and team data loaded from JSON files
- **Mobile Friendly**: Fully responsive design for all devices
- **SEO Optimized**: Proper meta tags and semantic HTML structure
- **Accessible**: Following web accessibility best practices

## 📋 Pages

- **Home**: Hero section with community overview and next event preview
- **Events**: Comprehensive events listing with upcoming and past events
- **About Us**: Leadership team and member profiles organized by teams

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Jinja2 Templates + TailwindCSS
- **Styling**: Custom CSS with TailwindCSS utility classes
- **Icons**: Font Awesome
- **Data**: JSON files for events and team information

## 📁 Project Structure

```
MLSC/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── README.md              # Project documentation
│
├── routers/               # API route handlers
│   ├── __init__.py
│   ├── home.py           # Home page routes
│   ├── events.py         # Events page routes
│   └── about.py          # About page routes
│
├── templates/             # Jinja2 HTML templates
│   ├── base.html         # Base template with navbar/footer
│   ├── home.html         # Home page template
│   ├── events.html       # Events page template
│   └── about.html        # About page template
│
├── static/                # Static assets
│   ├── css/
│   │   └── style.css     # Custom CSS styles
│   ├── js/
│   │   └── main.js       # JavaScript functionality
│   └── img/              # Images and media files
│       └── README.md     # Instructions for adding images
│
└── data/                  # JSON data files
    ├── events.json       # Events data
    └── team.json         # Team members data
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**:
   ```bash
   
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

5. **Open your browser** and navigate to:
   ```
   http://localhost:8000
   ```

## 📝 Configuration

#### Events

Edit `data/events.json` to add or modify events:

```json
{
  "upcoming": [
    {
      "title": "Workshop Title",
      "date": "2025-10-15",
      "time": "2:00 PM - 4:00 PM",
      "venue": "Computer Lab 1, MGMCOET",
      "description": "Workshop description...",
      "registration_link": "https://forms.microsoft.com/...",
      "image": "workshop-image.jpg"
    }
  ],
  "past": [
    // Past events...
  ]
}
```

#### Team Members

Edit `data/team.json` to update team information:

```json
{
  "leadership": [
    {
      "name": "Member Name",
      "role": "Position",
      "photo": "member-photo.jpg",
      "bio": "Brief bio...",
      "linkedin": "https://linkedin.com/in/member"
    }
  ],
  "teams": {
    "Team Name": [
      // Team members...
    ]
  }
}
```

### Adding Images

1. Add team member photos to `static/img/team/`
2. Add event images to `static/img/events/`
3. Add the MLSC logo as `static/img/mlsc-logo.png`

## 🎨 Customization

### Colors

The website uses a custom color scheme defined in CSS variables:
- Primary Blue: `#0078d4`
- Dark Blue: `#005a9f`
- Light Blue: `#40e0d0`

### Styling

- Main styles are in `static/css/style.css`
- TailwindCSS classes are used throughout templates
- Custom animations and effects are defined in CSS

### JavaScript

Interactive features are handled in `static/js/main.js`:
- Mobile menu functionality
- Smooth scrolling
- Image lazy loading
- Countdown timers for events

## 🚀 Deployment

### Local Development

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Deployment

1. **Set environment variables**:
   ```bash
   set DEBUG=False
   ```

2. **Run with Gunicorn** (Linux/Mac) or **uvicorn** (Windows):
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

3. **Deploy to cloud platforms**:
   - **Heroku**: Add `Procfile` with `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Azure**: Use Azure App Service with Python runtime
   - **AWS**: Deploy using Elastic Beanstalk or EC2
   - **DigitalOcean**: Use App Platform or Droplet

## 📱 Features

### Responsive Design
- Mobile-first approach
- Adaptive layouts for all screen sizes
- Touch-friendly navigation

### Performance
- Optimized images and assets
- Minimal JavaScript
- Fast page load times

### Accessibility
- Semantic HTML structure
- Proper ARIA labels
- Keyboard navigation support
- High contrast support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For any questions or issues:
- **Email**: mlsc@mgmcoet.edu.in
- **GitHub Issues**: Create an issue in the repository
- **WhatsApp**: Join our community group

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🙏 Acknowledgments

- Microsoft Learn Student Community
- MGMCOET Faculty and Students
- TailwindCSS and FastAPI communities
- Font Awesome for icons

---

**Built with ❤️ by MLSC MGMCOET Web Development Team**
