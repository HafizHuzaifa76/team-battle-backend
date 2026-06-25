# API Reference

Base URL: `http://localhost:8000` (development)

All successful responses use the [standard envelope](./README.md#standard-response-envelope) unless noted.

---

## Accounts

### Login

| | |
|---|---|
| **Method / URL** | `POST /accounts/login/` |
| **Auth** | None |
| **Body** | `{ "email": string, "password": string }` |

---

### Refresh token

| | |
|---|---|
| **Method / URL** | `POST /accounts/refresh/` |
| **Auth** | None |
| **Body** | `{ "refresh": string }` |
| **Response** | SimpleJWT format (not wrapped) — see [Authentication](./AUTHENTICATION.md) |

---

### Register user

| | |
|---|---|
| **Method / URL** | `POST /accounts/register/` |
| **Auth** | Admin |
| **Body** | `{ "name": string, "email": string, "password": string, "role"?: string }` |
| **Status** | `201 Created` |

---

### List all users

| | |
|---|---|
| **Method / URL** | `GET /accounts/users/` |
| **Auth** | Admin |

**Response `data`** — array of:

```json
{
  "id": 1,
  "name": "Jane Admin",
  "email": "jane@example.com",
  "role": "Admin"
}
```

---

## Players

Players are users with `role: "PLAYER"`. Base path: `/players/`

### List players

| | |
|---|---|
| **Method / URL** | `GET /players/` |
| **Auth** | Authenticated |

**Response `data`** — array of:

```json
{
  "id": 3,
  "name": "Alex Player",
  "email": "alex@example.com",
  "role": "PLAYER",
  "team": {
    "id": 1,
    "name": "Fire Hawks",
    "identifier": "fire_hawks",
    "rank": 2
  }
}
```

`team` is `null` if the player is unassigned.

---

### Create player

| | |
|---|---|
| **Method / URL** | `POST /players/` |
| **Auth** | Admin |
| **Status** | `201 Created` |

**Request body**

| Field | Type | Required |
|-------|------|----------|
| `name` | string | Yes |
| `email` | string | Yes |

The server assigns `role: "PLAYER"` and a default password (`player123`). Communicate credentials to the player through your app flow.

**Duplicate email** returns HTTP 400 with message `"User with this email already exist"`.

---

### Get player by ID

| | |
|---|---|
| **Method / URL** | `GET /players/{id}/` |
| **Auth** | Authenticated |

---

### Update player

| | |
|---|---|
| **Method / URL** | `PATCH /players/{id}/` |
| **Auth** | Admin |
| **Body** | Partial — any of `name`, `email` |

---

### Delete player

| | |
|---|---|
| **Method / URL** | `DELETE /players/{id}/` |
| **Auth** | Admin |

**Response `data`:** `null`

---

## Teams

Base path: `/teams/`

> **URL note:** Team detail uses **no trailing slash**: `/teams/1` (not `/teams/1/`).

### List teams

| | |
|---|---|
| **Method / URL** | `GET /teams/` |
| **Auth** | Authenticated |

**Response `data`** — array of:

```json
{
  "id": 1,
  "name": "Fire Hawks",
  "identifier": "fire_hawks",
  "rank": 2,
  "category": "Gold",
  "players": [
    {
      "id": 3,
      "name": "Alex Player",
      "email": "alex@example.com",
      "role": "PLAYER"
    }
  ]
}
```

`player_ids` is write-only and never appears in responses.

---

### Create team

| | |
|---|---|
| **Method / URL** | `POST /teams/` |
| **Auth** | Admin |
| **Status** | `201 Created` |

**Request body**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | string | Yes | Team display name |
| `player_ids` | integer[] | Yes | At least one ID; players must be unassigned |

**Server-side behavior**

- `identifier` is auto-generated from name (lowercase, spaces → underscores).
- `rank` is auto-assigned as `last_rank + 1`.
- `category` is derived from rank (see [Data Models](./DATA_MODELS.md)).

**Validation errors**

| Message | Cause |
|---------|-------|
| `"At least one player is required."` | Empty `player_ids` |
| `"Some players already belong to another team."` | Player already on a different team |
| `"Invalid Players IDs: {set}"` | ID not found or not a free player |

---

### Get team by ID

| | |
|---|---|
| **Method / URL** | `GET /teams/{id}` |
| **Auth** | Authenticated |

---

### Update team

| | |
|---|---|
| **Method / URL** | `PATCH /teams/{id}` |
| **Auth** | Admin |

**Request body**

| Field | Type | Notes |
|-------|------|-------|
| `name` | string | Optional |
| `player_ids` | integer[] | Replaces roster; only **unassigned** players can be added |

Players removed from `player_ids` are unassigned from the team (`team` set to `null`).

> The serializer does not use `partial=True`, so include all fields you intend to update in practice.

---

### Delete team

| | |
|---|---|
| **Method / URL** | `DELETE /teams/{id}` |
| **Auth** | Admin |

---

## Challenges

Base path: `/challenge/`

### List challenges

| | |
|---|---|
| **Method / URL** | `GET /challenge/` |
| **Auth** | Authenticated |

**Response `data`** — array of challenge objects (newest `challenge_date` first):

```json
{
  "id": 1,
  "challenger": {
    "id": 5,
    "name": "Underdogs",
    "identifier": "underdogs",
    "rank": 8
  },
  "challenged": {
    "id": 3,
    "name": "Top Tier",
    "identifier": "top_tier",
    "rank": 5
  },
  "challenge_date": "2026-06-25",
  "winner": null,
  "status": "UPCOMING",
  "challenger_points": null,
  "challenged_points": null,
  "created_at": "2026-06-21T10:00:00Z",
  "updated_at": "2026-06-21T10:00:00Z"
}
```

---

### Create challenge

| | |
|---|---|
| **Method / URL** | `POST /challenge/` |
| **Auth** | Authenticated |
| **Status** | `201 Created` |

**Request body**

| Field | Type | Required |
|-------|------|----------|
| `challenger_id` | integer | Yes | Team ID of the challenging (lower-ranked) team |
| `challenged_id` | integer | Yes | Team ID being challenged |
| `challenge_date` | string (date) | Yes | `YYYY-MM-DD` |

**Business rules** (server enforced)

- A team cannot challenge itself.
- Challenger rank must be **greater** (worse position) than challenged rank.
- Rank gap must be **1–3** (challenger can only target ranks `challenger.rank - 3` through `challenger.rank - 1`).
- Neither team may already have a challenge on the same date.
- **Status** is set automatically from date:
  - Future date → `UPCOMING`
  - Today → `TODAY`
  - Past date → `PENDING_RESULT`

**Example error messages**

| Message | Cause |
|---------|-------|
| `"Team cannot challenge itself"` | Same team IDs |
| `"This challenger can only challenge teams with ranks X to Y"` | Rank gap invalid |
| `"Challenger team already have Challenge on this date"` | Date conflict |
| `"Challenged team already have Challenge on this date"` | Date conflict |

---

### Get challenge by ID

| | |
|---|---|
| **Method / URL** | `GET /challenge/{challenge_id}/` |
| **Auth** | Authenticated |

---

### Delete challenge

| | |
|---|---|
| **Method / URL** | `DELETE /challenge/{challenge_id}/` |
| **Auth** | Authenticated |

Only a user whose **own team is the challenger** may delete the challenge.

**Error:** `"Only challenger can delete his own challenge"` if the user's team is not the challenger.

---

### Update challenge (PATCH)

| | |
|---|---|
| **Method / URL** | `PATCH /challenge/{challenge_id}/` |
| **Auth** | Authenticated |

> **Note:** The current backend implementation routes PATCH to challenge creation logic rather than an update flow. Treat PATCH as **unsupported/unstable** until the backend team confirms otherwise. Prefer delete + recreate for now.

---

### Submit challenge result

| | |
|---|---|
| **Method / URL** | `PATCH /challenge/result/{challenge_id}/` |
| **Auth** | Admin |

**Request body**

| Field | Type | Required |
|-------|------|----------|
| `challenger_points` | integer (≥ 0) | Yes |
| `challenged_points` | integer (≥ 0) | Yes |

**Rules**

- Challenge must have status `PENDING_RESULT`.
- Winner is determined by points (higher wins; equal = `DRAW`).
- If challenger wins, ranks are recalculated (challenger takes challenged team's rank; intermediate teams shift down).

**Response `data`** — updated challenge with `winner`, `status: "COMPLETED"`, and refreshed team ranks in nested objects.

**Example errors**

| Message | Cause |
|---------|-------|
| `"Only challenges with PENDING_RESULT can be updated"` | Wrong status |
| `"Both team scores are required"` | Missing points |

---

## Endpoint summary table

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/accounts/login/` | Public | Login |
| POST | `/accounts/refresh/` | Public | Refresh JWT |
| POST | `/accounts/register/` | Admin | Create user |
| GET | `/accounts/users/` | Admin | List users |
| GET | `/players/` | Auth | List players |
| POST | `/players/` | Admin | Create player |
| GET | `/players/{id}/` | Auth | Get player |
| PATCH | `/players/{id}/` | Admin | Update player |
| DELETE | `/players/{id}/` | Admin | Delete player |
| GET | `/teams/` | Auth | List teams |
| POST | `/teams/` | Admin | Create team |
| GET | `/teams/{id}` | Auth | Get team |
| PATCH | `/teams/{id}` | Admin | Update team |
| DELETE | `/teams/{id}` | Admin | Delete team |
| GET | `/challenge/` | Auth | List challenges |
| POST | `/challenge/` | Auth | Create challenge |
| GET | `/challenge/{id}/` | Auth | Get challenge |
| DELETE | `/challenge/{id}/` | Auth | Delete (challenger only) |
| PATCH | `/challenge/result/{id}/` | Admin | Submit result |

**Auth legend:** Public = no token; Auth = any authenticated user; Admin = `role === "Admin"`.
