
# 📡 API Monitor Client

API Monitor Client is a comprehensive solution for real-time log ingestion, analysis, and visualization of API requests and responses. Built using **Django**, **MongoDB**, and **React**, this project ensures seamless monitoring and insights into API behaviors with a clean and intuitive UI.

---

## 🎯 Objective
The goal of this project is to:
- Monitor and analyze API requests and responses.
- Provide real-time insights for developers and DevOps teams.
- Enable detailed analytics and error tracking with an interactive dashboard.

---

## 🛠️ Features
✅ Log ingestion with structured data.  
✅ Real-time API analytics and monitoring.  
✅ Interactive dashboard to visualize API performance.  
✅ Encryption/Decryption of sensitive data for security.  
✅ Configurable middleware for request/response tracking.  
✅ Granular permission and role-based access control.  

---

## ⚙️ Architecture
```
/api_monitor_client/
├── /api_monitor_client/                  # Main Django Project 
│   ├── /settings/
│   │   ├── __init__.py
│   │   ├── base.py                   # Common settings
│   │   ├── local.py                  # Local/Dev settings
│   │   └── production.py             # Production settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py
│   └── wsgi.py
├── /apps/
│   ├── /logs/                        # App for Log Ingestion
│   │   ├── /migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── /analytics/                   # App for Log Analytics & Dashboard
│   │   ├── /migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   └── /core/                        # Core App for Common Utilities
│       ├── __init__.py
│       ├── encryption.py             # Encryption/Decryption Logic
│       ├── middleware.py             # Custom Middleware
│       ├── permissions.py            # Custom Permissions
│       ├── utils.py                  # Reusable Utilities
│       └── validators.py             # Input Validators
├── /config/                          # Configurations for Docker, CI/CD, etc.
│   ├── /nginx/
│   │   └── nginx.conf
│   └── /gunicorn/
│       └── gunicorn.conf.py        
├── /docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .env                              # Environment Variables
├── .gitignore                        # Git Ignore File
├── manage.py                         # Django CLI
└── README.md                         # Project Documentation
```

---

## 🚀 Tech Stack
- **Backend:** Django, Django REST Framework, MongoDB
- **Frontend:** React (for API visualization - planned)
- **Security:** Keycloak (for IAM) or django auth (planned), Encryption/Decryption (AES256)
- **Task Queue:** Celery + Redis (optional)
- **Web Server:** Nginx + Gunicorn
- **Containerization:** Docker, Docker Compose

---

## 🛑 Pre-requisites
Make sure you have the following installed:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Python 3.10+  
- MongoDB 6.0+  
- Node.js 18+ (if using React)

---

## 📦 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/username/api_monitor_client.git
cd api_monitor_client
```

---

### 2. Set Up Environment Variables
Create a `.env` file in the root directory:
```
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
MONGO_URI=mongodb://mongo:27017/api_logs
ALLOWED_HOSTS=*
```

---

### 3. Configure MongoDB
```bash
# Pull MongoDB Docker image
docker pull mongo:6.0

# Run MongoDB container
docker run -d --name mongo -p 27017:27017 -v mongo_data:/data/db mongo:6.0
```

---

### 4. Build and Run Docker Containers
```bash
cd /docker
# Build and start containers
docker-compose up --build
```

---

## 🔥 API Endpoints

### 1. Log Ingestion
```
POST /api/logs/
```
- Ingests API logs into MongoDB.

### 2. Analytics & Insights
```
GET /api/analytics/
```
- Retrieves analytics data for logs.

---

## 🔐 Authentication & Security
- Integrated **Keycloak** for IAM (Identity and Access Management).
- Role-based access control (RBAC).
- AES-256 encryption for sensitive data.

---

## 📝 Docker & Deployment

### Dockerfile
- Configured to use `gunicorn` to serve the Django application.
- Static files served by `nginx` for better performance.

### docker-compose.yml
- Configured to run:
  - `Django + Gunicorn` for backend
  - `Nginx` as a reverse proxy
  - `MongoDB` for storage

### Nginx Configuration
`/config/nginx/nginx.conf`
- Configured to route requests to the Django backend via Gunicorn.

---

## 📚 Documentation
- Swagger documentation available at:
```
http://localhost:8000/swagger/
```

---

## 🎨 Future Enhancements
- ✅ API Visualization with React Dashboard
- ✅ Celery for Async Task Queuing
- ✅ Error Alerting System via Webhooks
- ✅ Multi-tenancy with MongoDB Aggregation

---

## 👨‍💻 Contributing
We welcome contributions! Please follow these steps:
1. Fork the repo.
2. Create a feature branch:
```bash
git checkout -b feature-branch
```
3. Commit your changes:
```bash
git commit -m "Add new feature"
```
4. Push to your branch:
```bash
git push origin feature-branch
```
5. Submit a pull request.

---

## 📧 Contact
For any queries or assistance, feel free to reach out at:
- 📩 Email: [ritheshraov016@gmail.com](mailto:ritheshraov016@gmail.com)
- 🐙 GitHub Issues: [Create Issue](https://github.com/username/api_monitor_client/issues)

---
## 📝 Author

Developed by [Ritesh x ChatGPT](https://github.com/RiteshRaoV)

---

✅ **Ready to Monitor APIs Like a Pro!** 🎯
