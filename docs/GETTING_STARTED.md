# Getting Started

## Prerequisites

- Python 3.10+
- Virtual environment (recommended)

## Run the backend locally

From the project root (`teambattlebackend/`):

```bash
# Create and activate virtual environment (if not already done)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies (adjust if your team uses a requirements file)
pip install django djangorestframework djangorestframework-simplejwt drf-spectacular

# Apply migrations
python manage.py migrate

# Create a superuser (Admin) for first login
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Default base URL: **`http://localhost:8000`**

## First API call — login

```http
POST /accounts/login/
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "your-password"
}
```

Example response:

```json
{
  "success": true,
  "message": "Login successfully",
  "data": {
    "user": {
      "id": 1,
      "name": "Admin User",
      "email": "admin@example.com",
      "role": "Admin",
      "team": null
    },
    "tokens": {
      "refresh": "<refresh-token>",
      "access": "<access-token>"
    }
  },
  "errors": null
}
```

Use the access token on subsequent requests:

```http
GET /teams/
Authorization: Bearer <access-token>
```

## Interactive documentation

| URL | Description |
|-----|-------------|
| `http://localhost:8000/api/docs/` | Swagger UI — browse and try endpoints |
| `http://localhost:8000/api/schema/` | Raw OpenAPI 3 schema (JSON/YAML) |

In Swagger, click **Authorize** and enter: `Bearer <your-access-token>`.

## CORS note

The backend does **not** currently configure `django-cors-headers`. If your frontend runs on a different origin (e.g. `http://localhost:3000`), you will need the backend team to add CORS settings, or use a dev proxy.

Example proxy (Vite `vite.config.js`):

```js
export default {
  server: {
    proxy: {
      '/accounts': 'http://localhost:8000',
      '/players': 'http://localhost:8000',
      '/teams': 'http://localhost:8000',
      '/challenge': 'http://localhost:8000',
    },
  },
};
```

## Content type

All request bodies should use:

```http
Content-Type: application/json
```

Responses are always `application/json`.

## Date and time

- Dates: `YYYY-MM-DD` (e.g. `"2026-06-21"`)
- Timestamps in responses: ISO 8601 UTC (e.g. `"2026-06-21T14:30:00Z"`)

The server timezone is **UTC**.
