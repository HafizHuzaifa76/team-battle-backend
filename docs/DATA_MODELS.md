# Data Models & Business Rules

## Entity relationship

```
User (accounts.User)
├── role: Admin | CAPTAIN | PLAYER
├── team → Team (nullable FK)
└── email (unique, used as login username)

Team (teams.Team)
├── name, identifier, rank, category
└── players ← User (related_name="players")

Challenge (teams_challenge.Challenge)
├── challenger → Team
├── challenged → Team
├── challenge_date, status, winner
└── challenger_points, challenged_points
```

---

## User

| Field | Type | Notes |
|-------|------|-------|
| `id` | integer | Primary key |
| `name` | string | Default: `"New Player"` |
| `email` | string | Unique; login identifier |
| `role` | enum | See [Roles](#roles) |
| `team` | Team object or `null` | Only relevant for players |

### Roles

| Stored value | Label | Typical use |
|--------------|-------|-------------|
| `Admin` | ADMIN | System administration |
| `CAPTAIN` | Captain | Team captain (future use) |
| `PLAYER` | Player | Team member |

---

## Team

| Field | Type | Read-only | Notes |
|-------|------|-----------|-------|
| `id` | integer | Yes | |
| `name` | string | No | Display name |
| `identifier` | string | Yes | Auto: `name` lowercased, spaces → `_` |
| `rank` | integer | Yes | Lower number = better position (1 is best) |
| `category` | enum | Yes | Derived from rank at creation |
| `players` | User[] | Yes | Current roster (basic player info) |
| `player_ids` | integer[] | Write-only | Used on create/update |

### Category (from rank at team creation)

| Rank range | Category |
|------------|----------|
| 1 – 4 | `Platinum` |
| 5 – 21 | `Gold` |
| 22 – 32 | `Silver` |
| 33+ | `Bronze` |

Category is **not** recalculated when rank changes after a challenge win.

### Team roster rules

- A player (`role: "PLAYER"`) can belong to **at most one** team.
- Creating a team requires at least one unassigned player.
- Updating a team's `player_ids` replaces the roster:
  - Removed players become unassigned.
  - New IDs must refer to players with no current team (except those already on this team being kept).

---

## Challenge

| Field | Type | Notes |
|-------|------|-------|
| `id` | integer | |
| `challenger` | Team (nested) | Lower-ranked team initiating |
| `challenged` | Team (nested) | Higher-ranked team being challenged |
| `challenge_date` | date | `YYYY-MM-DD` |
| `status` | enum | See [Challenge status](#challenge-status) |
| `winner` | enum or `null` | Set when result is submitted |
| `challenger_points` | integer or `null` | Set on result |
| `challenged_points` | integer or `null` | Set on result |
| `created_at` | datetime | ISO 8601 |
| `updated_at` | datetime | ISO 8601 |

### Challenge status

| Value | Meaning | Frontend hint |
|-------|---------|---------------|
| `UPCOMING` | Scheduled in the future | Show countdown / calendar |
| `TODAY` | Scheduled for today | Highlight as active |
| `PENDING_RESULT` | Date passed, no result yet | Admin result entry |
| `COMPLETED` | Result recorded | Show scores and winner |
| `CANCELLED` | Cancelled | Reserved (not auto-set currently) |

Status is assigned automatically when a challenge is **created**, based on `challenge_date` vs today.

### Winner

| Value | Meaning |
|-------|---------|
| `CHALLENGER_TEAM` | Challenger scored higher |
| `CHALLENGED_TEAM` | Challenged team scored higher |
| `DRAW` | Equal scores |

### Challenge eligibility (rank rules)

Given challenger rank `C` and challenged rank `T`:

1. `C > T` — challenger must be ranked **worse** (higher number).
2. `C - T <= 3` — maximum 3-rank gap.
3. Valid challenged ranks: `max(1, C - 3)` through `C - 1`.

**Example:** Rank 8 team can challenge ranks 5, 6, or 7.

### Rank swap on challenger win

When an admin submits a result and the **challenger wins**:

1. All teams with rank between challenged and challenger (inclusive of challenged, exclusive of challenger) move down by 1.
2. Challenger team takes the challenged team's old rank.

No rank change occurs on challenged-team win or draw.

---

## TypeScript types (reference)

Copy into your frontend project as a starting point:

```typescript
export type UserRole = 'Admin' | 'CAPTAIN' | 'PLAYER';

export type TeamCategory = 'Platinum' | 'Gold' | 'Silver' | 'Bronze';

export type ChallengeStatus =
  | 'UPCOMING'
  | 'TODAY'
  | 'PENDING_RESULT'
  | 'COMPLETED'
  | 'CANCELLED';

export type ChallengeWinner =
  | 'CHALLENGER_TEAM'
  | 'CHALLENGED_TEAM'
  | 'DRAW'
  | null;

export interface TeamBasic {
  id: number;
  name: string;
  identifier: string;
  rank: number;
}

export interface PlayerBasic {
  id: number;
  name: string;
  email: string;
  role: UserRole;
}

export interface Team extends TeamBasic {
  category: TeamCategory;
  players: PlayerBasic[];
}

export interface Player extends PlayerBasic {
  team: TeamBasic | null;
}

export interface User {
  id: number;
  name: string;
  email: string;
  role: UserRole;
  team: TeamBasic | null;
}

export interface Challenge {
  id: number;
  challenger: TeamBasic;
  challenged: TeamBasic;
  challenge_date: string;
  winner: ChallengeWinner;
  status: ChallengeStatus;
  challenger_points: number | null;
  challenged_points: number | null;
  created_at: string;
  updated_at: string;
}

export interface ApiSuccess<T> {
  success: true;
  message: string;
  data: T;
  errors: null;
}

export interface ApiError {
  success: false;
  message: string;
  errors: unknown;
}

export interface LoginData {
  user: User;
  tokens: {
    access: string;
    refresh: string;
  };
}
```

---

## Default credentials (development)

When an admin creates a player via `POST /players/`, the backend sets password to **`player123`**. Players should change this in a future flow if password management is added.

Superusers created via `createsuperuser` receive `role: Admin` automatically.
