# API Documentation

**Version:** 2.0
**Base URL:** `https://api.company.com/v2`
**Authentication:** Bearer Token

## Authentication

All API requests require authentication using a Bearer token in the Authorization header.

```http
Authorization: Bearer YOUR_API_TOKEN
```

### Obtaining an API Token

```http
POST /auth/token
Content-Type: application/json

{
  "username": "user@company.com",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

## Users API

### List Users

Retrieve a paginated list of users.

```http
GET /users?page=1&limit=20
```

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `limit` (integer): Items per page (default: 20, max: 100)
- `search` (string): Search by name or email
- `role` (string): Filter by role

**Response:**
```json
{
  "data": [
    {
      "id": "usr_123",
      "email": "john@company.com",
      "name": "John Doe",
      "role": "developer",
      "created_at": "2025-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

### Get User

Retrieve a specific user by ID.

```http
GET /users/{user_id}
```

**Response:**
```json
{
  "id": "usr_123",
  "email": "john@company.com",
  "name": "John Doe",
  "role": "developer",
  "department": "Engineering",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

### Create User

Create a new user.

```http
POST /users
Content-Type: application/json

{
  "email": "jane@company.com",
  "name": "Jane Smith",
  "role": "designer",
  "department": "Design"
}
```

**Response:** 201 Created
```json
{
  "id": "usr_124",
  "email": "jane@company.com",
  "name": "Jane Smith",
  "role": "designer",
  "created_at": "2025-01-15T11:00:00Z"
}
```

### Update User

Update an existing user.

```http
PATCH /users/{user_id}
Content-Type: application/json

{
  "name": "Jane Doe",
  "department": "Product"
}
```

### Delete User

Delete a user.

```http
DELETE /users/{user_id}
```

**Response:** 204 No Content

## Projects API

### List Projects

```http
GET /projects?status=active
```

**Query Parameters:**
- `status` (string): Filter by status (active, archived, completed)
- `team` (string): Filter by team ID

**Response:**
```json
{
  "data": [
    {
      "id": "proj_456",
      "name": "Mobile App Redesign",
      "status": "active",
      "team_id": "team_789",
      "start_date": "2025-01-01",
      "due_date": "2025-03-31"
    }
  ]
}
```

### Create Project

```http
POST /projects
Content-Type: application/json

{
  "name": "API v3 Migration",
  "description": "Migrate to new API version",
  "team_id": "team_789",
  "start_date": "2025-02-01"
}
```

## Tasks API

### List Tasks

```http
GET /tasks?project_id=proj_456&assignee=usr_123
```

**Response:**
```json
{
  "data": [
    {
      "id": "task_001",
      "title": "Design homepage mockup",
      "description": "Create high-fidelity mockup",
      "status": "in_progress",
      "priority": "high",
      "assignee_id": "usr_123",
      "project_id": "proj_456",
      "due_date": "2025-01-20"
    }
  ]
}
```

### Update Task Status

```http
PATCH /tasks/{task_id}
Content-Type: application/json

{
  "status": "completed"
}
```

## Error Responses

The API uses standard HTTP status codes:

- `200 OK`: Request succeeded
- `201 Created`: Resource created
- `204 No Content`: Request succeeded, no content returned
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

**Error Response Format:**
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "value": "invalid-email"
    }
  }
}
```

## Rate Limiting

- **Standard:** 1000 requests per hour
- **Premium:** 5000 requests per hour

Rate limit headers:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642267200
```

## Webhooks

Subscribe to events by configuring webhooks in your account settings.

**Events:**
- `user.created`
- `user.updated`
- `user.deleted`
- `project.created`
- `task.completed`

**Webhook Payload:**
```json
{
  "event": "user.created",
  "timestamp": "2025-01-15T10:30:00Z",
  "data": {
    "id": "usr_123",
    "email": "john@company.com"
  }
}
```

## SDKs

Official SDKs available:
- Python: `pip install company-api`
- JavaScript: `npm install @company/api`
- Ruby: `gem install company-api`
- Go: `go get github.com/company/api-go`

## Support

- [API Status](https://status.company.com)
- [Developer Forum](https://forum.company.com)
- Email: api-support@company.com
