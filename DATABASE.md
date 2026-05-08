# DriftDater — Database Schema Documentation

## Overview

The database consists of **8 tables** in **Third Normal Form (3NF)**. Designed using PostgreSQL via SQLAlchemy ORM. Migrations managed with Flask-Migrate.

---

## Tables

### `members`
Stores account credentials. Kept separate from profile data to allow authentication without loading profile info.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PK, AUTO | Primary key |
| `handle` | VARCHAR(80) | UNIQUE, NOT NULL, INDEX | Unique username |
| `email_address` | VARCHAR(120) | UNIQUE, NOT NULL, INDEX | Login identifier |
| `secret_key` | VARCHAR(255) | NOT NULL | Werkzeug-hashed password |
| `joined_on` | DATETIME | DEFAULT now() | Registration timestamp |

---

### `user_details`
Extended profile information. One-to-one with `members`. Separated to keep auth logic clean and profiles independently manageable.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PK, AUTO | Primary key |
| `member_id` | INTEGER | FK → members.id, UNIQUE | Owner reference |
| `full_name` | VARCHAR(100) | NOT NULL | Display name |
| `years_old` | INTEGER | NOT NULL, INDEX | Used in matching and filtering |
| `about_me` | TEXT | NULLABLE | Free-text bio/description |
| `city_area` | VARCHAR(100) | INDEX | City for proximity matching |
| `home_parish` | VARCHAR(100) | NULLABLE | Parish/region |
| `sex` | VARCHAR(20) | NULLABLE | User's gender |
| `seeking` | VARCHAR(20) | NULLABLE | Gender preference (male/female/any) |
| `job_title` | VARCHAR(100) | NULLABLE | Custom field 1 — occupation |
| `connection_goal` | VARCHAR(50) | NULLABLE | Custom field 2 — serious/casual/friendship |
| `display_picture` | VARCHAR(255) | NULLABLE | Filename of uploaded profile photo |
| `visibility_status` | BOOLEAN | DEFAULT true | Profile visibility control (public/private) |
| `setup_date` | DATETIME | DEFAULT now() | Profile creation timestamp |

---

### `tags`
Lookup table for interest tags. Normalized to avoid string duplication across profiles.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PK, AUTO | Primary key |
| `label` | VARCHAR(50) | UNIQUE, NOT NULL | Interest label (e.g. "hiking") |

---

### `detail_tags_link` *(junction table)*
Resolves the many-to-many relationship between `user_details` and `tags`.

| Column | Type | Constraints |
|--------|------|-------------|
| `detail_id` | INTEGER | FK → user_details.id, PK |
| `tag_id` | INTEGER | FK → tags.id, PK |

---

### `swipe_actions`
Records every like or pass action a member takes on another profile. Used to determine mutual matches and exclude already-acted profiles from browse.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PK, AUTO | Primary key |
| `actor_id` | INTEGER | FK → members.id, INDEX | The member taking action |
| `target_id` | INTEGER | FK → members.id, INDEX | The member being acted on |
| `logged_at` | DATETIME | DEFAULT now() | Timestamp of the action |

**Constraints:** UNIQUE(`actor_id`, `target_id`) — one action per pair.

---

### `connections`
Created automatically when two members have both liked each other (mutual match detection). `peer_a_id` always holds the lower user ID by convention to prevent duplicate entries.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PK, AUTO | Primary key |
| `peer_a_id` | INTEGER | FK → members.id, INDEX | Lower member ID (by convention) |
| `peer_b_id` | INTEGER | FK → members.id, INDEX | Higher member ID |
| `formed_at` | DATETIME | DEFAULT now() | Timestamp when the match was made |

**Constraints:** UNIQUE(`peer_a_id`, `peer_b_id`) — no duplicate connections.

---

### `direct_messages`
Stores chat messages between connected members. Only members with a mutual connection can message each other (enforced at the API level).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PK, AUTO | Primary key |
| `author_id` | INTEGER | FK → members.id, INDEX | Message sender |
| `recipient_id` | INTEGER | FK → members.id, INDEX | Message receiver |
| `body_text` | TEXT | NOT NULL | Message content |
| `dispatched_at` | DATETIME | DEFAULT now() | Send timestamp |

---

### `saved_profiles`
Allows members to bookmark other profiles for later viewing.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PK, AUTO | Primary key |
| `owner_id` | INTEGER | FK → members.id, INDEX | The bookmarking member |
| `bookmarked_member_id` | INTEGER | FK → members.id, INDEX | The bookmarked member |
| `saved_at` | DATETIME | DEFAULT now() | Timestamp |

**Constraints:** UNIQUE(`owner_id`, `bookmarked_member_id`) — no duplicate bookmarks.

---

## Relationships

| Relationship | Type | Description |
|---|---|---|
| members → user_details | One-to-One | Each member has exactly one profile |
| user_details ↔ tags | Many-to-Many | Via `detail_tags_link` junction table |
| members → swipe_actions | One-to-Many | A member can like/pass many others |
| members → connections | One-to-Many | A member can have many mutual connections |
| members → direct_messages | One-to-Many | A member can send/receive many messages |
| members → saved_profiles | One-to-Many | A member can bookmark many profiles |

---

## Indexes

| Table | Column(s) | Reason |
|---|---|---|
| members | `email_address` | Frequent lookup during login |
| members | `handle` | Uniqueness check during registration |
| user_details | `years_old` | Range filtering in browse and search |
| user_details | `city_area` | Location-based filtering |
| swipe_actions | `actor_id` | Check actions taken by current member |
| swipe_actions | `target_id` | Check who has liked a member |
| connections | `peer_a_id`, `peer_b_id` | Connection lookup for both parties |
| direct_messages | `author_id`, `recipient_id` | Conversation history queries |
| saved_profiles | `owner_id` | Bookmark list lookup |

---

## Normalization (3NF)

- **1NF**: All columns are atomic — no arrays or repeated groups. Interests are stored in the `tags` table and linked via `detail_tags_link`, not as comma-separated strings.
- **2NF**: No partial dependencies — all non-key attributes depend on the full primary key. The junction table `detail_tags_link` uses a composite primary key with no non-key attributes.
- **3NF**: No transitive dependencies — account credentials live in `members`, extended profile info in `user_details`. Tag labels are not duplicated per profile; they reference the `tags` lookup table. Message content depends only on the message's own primary key.
