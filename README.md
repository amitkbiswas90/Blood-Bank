# 🩸 Blood Bank Management System

A REST API platform connecting blood donors with recipients while enforcing medical safety guidelines. Built with Django REST Framework.


## ✨ Features

### 👤 User Management
| Feature                      | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| 🔐 JWT Authentication        | Secure token-based authentication system                                    |
| 📧 Email Activation          | Verification flow with activation link sent via email                       |
| 👤 Profile Management        | Update personal details and donation preferences                           |
| 📅 Eligibility Tracking       | Automatic calculation of donation eligibility based on last donation date  |
| 🚫 Availability Toggle       | System-managed donor availability status                                   |

### 🩸 Blood Donation System
| Feature                      | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| 🆕 Request Creation          | Create blood requests with required units and hospital details             |
| 🔍 Donor Search              | Filter donors by blood group (A+, B+, O-, etc.)                            |
| ✅ Request Acceptance        | Validate and accept donation requests with eligibility checks              |
| ⏳ Cooldown Enforcement      | Strict 90-day interval between donations                                   |
| 📊 Interactive Dashboard     | Track active requests and donation history                                |

### 🛡️ Safety & Security
| Feature                      | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| 🚫 Self-Acceptance Prevention| Prevent users from accepting their own requests                            |
| 🔒 Role-Based Access         | Granular permissions for different user roles                              |
| ⏲️ Request Expiration        | Auto-expire stale requests after 72 hours                                  |
| 📉 Eligibility Calculations  | Real-time donor eligibility status updates                                |
| 🛡️ Comprehensive Validation  | 10+ validation checks on every donation operation                         |

## 🛠️ Tech Stack

### 📦 Core Components
| Component                  | Version  | Purpose                                  |
|----------------------------|----------|------------------------------------------|
| Python                     | 3.10+    | Base programming language                |
| Django                     | 4.2      | Web framework                            |
| Django REST Framework      | 3.14     | API construction                         |
| PostgreSQL                 | 14+      | Relational database                      |
| Redis                      | 6.2+     | Caching & task queue (optional)          |

### 📚 Key Libraries
```python
djangorestframework-simplejwt==5.2.2  # JWT Authentication
drf-yasg==1.21.4                      # Swagger Documentation
python-dotenv==0.21.0                 # Environment Management
psycopg2==2.9.5                       # PostgreSQL Adapter
django-filter==22.1                   # Query Filtering
celery==5.2.7                         # Async Tasks (optional)