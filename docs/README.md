# Team Battle Backend — Frontend Developer Guide

This documentation describes the **Team Battle** REST API for frontend integration. The backend is a Django 6 + Django REST Framework application with JWT authentication.

## Quick links

| Document | Description |
|----------|-------------|
| [Getting Started](./GETTING_STARTED.md) | Base URL, setup, Swagger, and first request |
| [Authentication](./AUTHENTICATION.md) | Login, tokens, refresh, and role-based access |
| [API Reference](./API_REFERENCE.md) | Every endpoint with request/response examples |
| [Data Models & Enums](./DATA_MODELS.md) | Users, teams, challenges, and business rules |
| [Error Handling](./ERROR_HANDLING.md) | Response envelope and common error cases |

## Live API docs (Swagger)

When the server is running locally:

- **Swagger UI:** `http://localhost:8000/api/docs/`
- **OpenAPI schema:** `http://localhost:8000/api/schema/`

Use Swagger for interactive testing. This written guide adds context Swagger does not cover (permissions, business rules, and frontend integration patterns).

## Application overview

Team Battle is a ranked team competition system:

1. **Admins** register users, create players, form teams, and record challenge results.
2. **Players** are users with role `PLAYER`. They belong to at most one team.
3. **Teams** are ranked (lower rank number = higher position). Category is derived from rank.
4. **Challenges** are issued by a lower-ranked team against a higher-ranked team within a 3-rank window. Winning a challenge can swap ranks.

```
┌─────────────┐     belongs to      ┌─────────────┐
│    User     │ ──────────────────► │    Team     │
│ (PLAYER)    │                     │  (ranked)   │
└─────────────┘                     └──────┬──────┘
                                           │
                              initiates / receives
                                           │
                                    ┌──────▼──────┐
                                    │  Challenge  │
                                    └─────────────┘
```

## URL prefix map

All API routes are mounted at the project root (no `/api/` prefix except for schema/docs):

| Prefix | App | Purpose |
|--------|-----|---------|
| `/accounts/` | accounts | Auth (login, register, refresh, list users) |
| `/players/` | accounts | Player CRUD |
| `/teams/` | teams | Team CRUD |
| `/challenge/` | teams_challenge | Challenge CRUD and results |

## Roles

| Role (stored value) | Description |
|---------------------|-------------|
| `Admin` | Full admin access; required for register, user list, player/team mutations, challenge results |
| `CAPTAIN` | Authenticated role (reserved for future captain-specific features) |
| `PLAYER` | Default role for players; can view resources and create/delete own challenges |

## Standard response envelope

Every endpoint returns JSON in this shape:

**Success**

```json
{
  "success": true,
  "message": "Human-readable message",
  "data": { },
  "errors": null
}
```

**Error**

```json
{
  "success": false,
  "message": "Primary error message",
  "errors": { }
}
```

See [Error Handling](./ERROR_HANDLING.md) for status codes and parsing guidance.

## Recommended frontend integration checklist

- [ ] Store `access` and `refresh` tokens from login; attach `Authorization: Bearer <access>` to protected requests.
- [ ] Refresh the access token via `POST /accounts/refresh/` before expiry (access token lifetime: **1 day**).
- [ ] Branch UI by `user.role` from the login response.
- [ ] Use ISO date strings (`YYYY-MM-DD`) for `challenge_date`.
- [ ] Handle validation errors in the `errors` field (may be a string, array, or nested object).

## Tech stack reference

| Layer | Technology |
|-------|------------|
| Framework | Django 6.0 |
| API | Django REST Framework |
| Auth | `rest_framework_simplejwt` (JWT Bearer) |
| Schema | `drf-spectacular` |
| Database | SQLite (development) |
