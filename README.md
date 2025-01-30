# Website Building Platform

This project is a website building platform that allows customers to rent a Dockerized Ghost instance on an Oracle server. The platform processes payments using Stripe and features a frontend developed with jQuery and a backend built with Python Django.

## Project Structure

```
website-building-platform
├── backend                # Django backend
│   ├── manage.py         # Command-line utility for managing the Django project
│   ├── requirements.txt   # Python packages required for the backend
│   ├── Dockerfile         # Docker image instructions for the Django backend
│   ├── app                # Django application
│   │   ├── __init__.py    # Marks the directory as a Python package
│   │   ├── settings.py     # Configuration settings for the Django application
│   │   ├── urls.py         # URL patterns for the Django application
│   │   ├── wsgi.py         # Entry point for WSGI-compatible web servers
│   │   └── views.py        # View functions for handling requests and responses
├── frontend               # Frontend application
│   ├── index.html         # Main HTML file for the frontend
│   ├── styles             # CSS styles for the frontend
│   │   └── main.css       # Styles defining the visual appearance
│   ├── scripts            # JavaScript code for the frontend
│       └── main.js        # jQuery code for user interactions and AJAX requests
├── ghost                  # Ghost instance
│   ├── Dockerfile         # Docker image instructions for the Ghost instance
│   └── config.production.json # Configuration settings for the Ghost instance
├── docker-compose.yml     # Defines services, networks, and volumes for Docker containers
├── package.json           # Configuration file for npm
└── README.md              # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd website-building-platform
   ```

2. **Backend Setup:**
   - Navigate to the `backend` directory.
   - Install the required Python packages:
     ```
     pip install -r requirements.txt
     ```
   - Build the Docker image:
     ```
     docker build -t django-backend .
     ```

3. **Frontend Setup:**
   - Navigate to the `frontend` directory.
   - Install npm dependencies:
     ```
     npm install
     ```

4. **Ghost Setup:**
   - Navigate to the `ghost` directory.
   - Build the Docker image:
     ```
     docker build -t ghost-instance .
     ```

5. **Run the application:**
   - Use Docker Compose to start all services:
     ```
     docker-compose up
     ```

## Usage

- Access the frontend at `http://localhost:3000`.
- The backend API can be accessed at `http://localhost:8000/api`.
- Manage Ghost instances through the provided interface.

## License

This project is licensed under the MIT License. See the LICENSE file for details.