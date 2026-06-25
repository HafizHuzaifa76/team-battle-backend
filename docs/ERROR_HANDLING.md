# Error Handling

## Response envelope

All API views (except `/accounts/refresh/`) return a consistent JSON structure.

### Success

```json
{
  "success": true,
  "message": "Teams Fetched Successfully",
  "data": [ ... ],
  "errors": null
}
```

HTTP status is typically **200 OK**, or **201 Created** for resource creation.

### Error

```json
{
  "success": false,
  "message": "Human-readable primary message",
  "errors": { ... }
}
```

Default HTTP status for application errors is **400 Bad Request**. Authentication and permission failures use standard DRF status codes (**401**, **403**, **404**).

---

## Parsing errors in the frontend

Always check `success` first:

```typescript
async function apiCall<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, options);
  const body = await res.json();

  if (!body.success) {
    throw new ApiError(body.message, body.errors, res.status);
  }

  return body.data as T;
}
```

The `errors` field shape varies by error type:

| Source | `errors` shape | Example |
|--------|----------------|---------|
| Validation (field) | Object keyed by field | `{ "email": ["This field is required."] }` |
| Validation (non-field) | Array of strings | `{ "non_field_errors": ["Invalid credentials"] }` |
| Permission | String or object with `detail` | `"You do not have permission..."` |
| Not found | String | `"Team Not Found"` |
| Custom service | String in `message` | `"User with this email already exist"` |

Use `message` for toast/alert text; use `errors` for inline form validation when it is an object.

---

## HTTP status codes

| Code | When |
|------|------|
| 200 | Successful GET, PATCH, DELETE |
| 201 | Successful POST (create) |
| 400 | Validation failure, business rule violation, or unhandled server error |
| 401 | Missing or invalid JWT |
| 403 | Authenticated but insufficient role (e.g. non-admin on admin route) |
| 404 | Resource not found |

---

## Common error messages

### Authentication

| Message | Endpoint | Fix |
|---------|----------|-----|
| `"Invalid credentials"` | Login | Check email/password |
| 401 Unauthorized | Any protected route | Refresh or re-login |

### Players

| Message | Cause |
|---------|-------|
| `"User with this email already exist"` | Duplicate email on create |
| `"Player Not Found"` | Invalid player ID |

### Teams

| Message | Cause |
|---------|-------|
| `"At least one player is required."` | Empty `player_ids` |
| `"Some players already belong to another team."` | Player on another team |
| `"Invalid Players IDs: {ids}"` | Bad or already-assigned player IDs |
| `"Team Not Found"` | Invalid team ID |

### Challenges

| Message | Cause |
|---------|-------|
| `"Challenger Team Not Found"` | Invalid `challenger_id` |
| `"Challenged Team Not Found"` | Invalid `challenged_id` |
| `"Team cannot challenge itself"` | Same team for both sides |
| `"This challenger can only challenge teams with ranks X to Y"` | Rank rules violated |
| `"Challenger/Challenged team already have Challenge on this date"` | Date conflict |
| `"Only challenger can delete his own challenge"` | Delete by non-challenger user |
| `"Only challenges with PENDING_RESULT can be updated"` | Result submitted too early |
| `"Both team scores are required"` | Missing points in result |
| `"Challenge does not exist"` | Invalid challenge ID |

---

## Validation error example

Request:

```http
POST /teams/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "New Team",
  "player_ids": []
}
```

Response (400):

```json
{
  "success": false,
  "message": "Request failed",
  "errors": {
    "player_ids": ["At least one player is required."]
  }
}
```

---

## Permission error example

Non-admin calling `POST /accounts/register/`:

```json
{
  "success": false,
  "message": "You do not have permission to perform this action.",
  "errors": {
    "detail": "You do not have permission to perform this action."
  }
}
```

HTTP status: **403 Forbidden**

---

## Unhandled server errors

Unexpected exceptions are caught by the custom exception handler and returned as:

```json
{
  "success": false,
  "message": "Internal server error",
  "errors": null
}
```

HTTP status: **400** (current implementation). Log the request details client-side and retry only if appropriate.

---

## Refresh token endpoint

`POST /accounts/refresh/` uses **SimpleJWT's native format**, not the custom envelope:

**Success (200)**

```json
{
  "access": "<new-access-token>"
}
```

**Failure (401)**

```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

Handle this endpoint separately from the standard `success`/`data` wrapper.
