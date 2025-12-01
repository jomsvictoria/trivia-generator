# Trivia API Documentation

A simple REST API for managing trivia questions with support for categories, searching, and CRUD operations.

## Base URL

```
http://localhost:5000
```

## Endpoints

### 1. Health Check

**GET /**

Check if the API is running and get the total question count.

**Response:**
```json
{
  "status": "ok",
  "message": "Trivia API",
  "count": 5
}
```

**Status Code:** `200 OK`

---

### 2. Get All Questions

**GET /questions**

Retrieve all trivia questions. Supports optional filtering.

**Query Parameters:**
- `category` (optional) - Filter by category (case-insensitive)
- `q` (optional) - Search term to find in question or answer text

**Examples:**

```bash
# Get all questions
curl http://localhost:5000/questions

# Filter by category
curl http://localhost:5000/questions?category=Science

# Search for questions containing "earth"
curl http://localhost:5000/questions?q=earth
```

**Response:**
```json
[
  {
    "id": 1,
    "question": "What is the capital of France?",
    "answer": "Paris",
    "category": "Geography"
  },
  {
    "id": 2,
    "question": "What is 2 + 2?",
    "answer": "4",
    "category": "Math"
  }
]
```

**Status Code:** `200 OK`

---

### 3. Get Single Question

**GET /questions/:id**

Retrieve a specific question by its ID.

**URL Parameters:**
- `id` (required) - The question ID

**Example:**

```bash
curl http://localhost:5000/questions/1
```

**Response:**
```json
{
  "id": 1,
  "question": "What is the capital of France?",
  "answer": "Paris",
  "category": "Geography"
}
```

**Status Codes:**
- `200 OK` - Question found
- `404 Not Found` - Question ID doesn't exist

**Error Response (404):**
```json
{
  "error": "Question not found"
}
```

---

### 4. Create Question

**POST /questions**

Add a new trivia question to the database.

**Request Body:**
```json
{
  "question": "What is the largest planet in our solar system?",
  "answer": "Jupiter",
  "category": "Science"
}
```

**Fields:**
- `question` (required, string) - The trivia question text
- `answer` (required, string) - The answer to the question
- `category` (optional, string) - Question category (defaults to "General")

**Example:**

```bash
curl -X POST http://localhost:5000/questions \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the largest planet in our solar system?",
    "answer": "Jupiter",
    "category": "Science"
  }'
```

**Response:**
```json
{
  "id": 3,
  "question": "What is the largest planet in our solar system?",
  "answer": "Jupiter",
  "category": "Science"
}
```

**Status Codes:**
- `201 Created` - Question successfully created
- `400 Bad Request` - Invalid JSON or missing required fields

**Error Response (400):**
```json
{
  "error": "question and answer are required"
}
```

---

### cURL

```bash
# Health check
curl http://localhost:5000/

# Get all questions
curl http://localhost:5000/questions

# Filter by category
curl "http://localhost:5000/questions?category=Science"

# Search questions
curl "http://localhost:5000/questions?q=capital"

# Get single question
curl http://localhost:5000/questions/1

# Create new question
curl -X POST http://localhost:5000/questions \
  -H "Content-Type: application/json" \
  -d '{"question":"What year did WW2 end?","answer":"1945","category":"History"}'
```

---

## Error Handling

The API uses standard HTTP status codes:

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request (malformed JSON or missing fields)
- `404 Not Found` - Resource not found

All errors return a JSON object with an `error` field describing the issue.

---

## Running the API

```bash
# Start the server
python src/api.py

# The API will be available at http://localhost:5000
```

The server runs in debug mode by default, which means it will automatically reload when you make code changes.

---

## Data Persistence

All questions are stored in `questions.json` at the project root. The file is automatically created and updated when you add new questions. The API uses atomic writes to prevent data corruption.