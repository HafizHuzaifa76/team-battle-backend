# Authentication

## Overview

The API uses **JWT (JSON Web Token)** authentication via `djangorestframework-simplejwt`.

- **Header format:** `Authorization: Bearer <access_token>`
- **Access token lifetime:** 1 day
- **Refresh token lifetime:** 7 days
- **Refresh rotation:** enabled (a new refresh token is issued on each refresh)

## Endpoints

### Login (public)

```http
POST /accounts/login/
```

**Request body**

| Field | Type | Required |
|-------|------|----------|
| `email` | string (email) | Yes |
| `password` | string | Yes |

**Response `data` shape**

```json
{
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "PLAYER",
    "team": {
      "id": 2,
      "name": "Thunder Squad",
      "identifier": "thunder_squad",
      "rank": 5
    }
  },
  "tokens": {
    "access": "<jwt-access>",
    "refresh": "<jwt-refresh>"
  }
}
```

`team` is `null` if the user is not assigned to a team.

**Invalid credentials** return HTTP 400 with message `"Invalid credentials"`.

---

### Refresh token

```http
POST /accounts/refresh/
```

**Request body**

```json
{
  "refresh": "<refresh-token>"
}
```

**Response** (standard SimpleJWT — not wrapped in the custom envelope):

```json
{
  "access": "<new-access-token>"
}
```

If rotation is active and blacklist is configured, the response may also include a new `refresh` token. Store whichever tokens the response returns.

---

### Register user (Admin only)

```http
POST /accounts/register/
Authorization: Bearer <admin-access-token>
```

**Request body**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | string | Yes | Display name |
| `email` | string | Yes | Unique |
| `password` | string | Yes | Min length 8 |
| `role` | string | No | `"Admin"`, `"CAPTAIN"`, or `"PLAYER"` (default: `"PLAYER"`) |

**Response `data`**

```json
{
  "user": {
    "id": 5,
    "email": "new@example.com",
    "role": "PLAYER"
  }
}
```

---

## Permission model

| Permission class | Who passes |
|------------------|------------|
| *(none)* | Anyone (login only) |
| `IsAuthenticated` | Any logged-in user with valid JWT |
| `IsAdminRole` | Logged-in user where `user.role === "Admin"` |

Unauthenticated requests to protected endpoints receive **401 Unauthorized**.

Authenticated non-admin requests to admin-only endpoints receive **403 Forbidden**.

---

## Frontend token storage pattern

```typescript
// Example: axios interceptor
import axios from 'axios';

const api = axios.create({ baseURL: 'http://localhost:8000' });

api.interceptors.request.use((config) => {
  const access = localStorage.getItem('access_token');
  if (access) {
    config.headers.Authorization = `Bearer ${access}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const refresh = localStorage.getItem('refresh_token');
      if (refresh) {
        const { data } = await axios.post('/accounts/refresh/', { refresh });
        localStorage.setItem('access_token', data.access);
        error.config.headers.Authorization = `Bearer ${data.access}`;
        return api.request(error.config);
      }
    }
    return Promise.reject(error);
  }
);
```

---

## Role-based UI guidance

| Feature | Admin | Authenticated (non-admin) |
|---------|-------|---------------------------|
| Login | Yes | Yes |
| Register users | Yes | No |
| List all users | Yes | No |
| List/create/edit/delete players | Create/edit/delete: Admin; list/get: Any | List/get only |
| List/create/edit/delete teams | Create/edit/delete: Admin; list/get: Any | List/get only |
| List/create challenges | Any authenticated | Any authenticated |
| Delete challenge | Challenger team member only | Same |
| Submit challenge result | Admin only | No |

Use `data.user.role` from login to gate navigation and actions client-side. The server always re-validates permissions.
