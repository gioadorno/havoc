# Build Plan: havoc

## Step 1: LLM Integration
*   Set up Google Cloud Vertex AI SDK for Python (`google-generativeai` or Vertex specific SDK).
*   Write prompt templates that instruct Gemini to generate JSON arrays matching a provided schema.

## Step 2: The Chaos Engine
*   Build a Python module that takes clean generated data and "breaks" it.
*   Implement flags for `--null-rate`, `--date-corruption-rate`, and `--unicode-injection`.
*   Randomly apply these corruptions to the dataset.

## Step 3: Schema Parsing
*   Allow the user to pass a simple JSON or YAML file defining the desired columns (e.g., "Name: String, DOB: Date, Balance: Float").

## Step 4: Output Handlers
*   Write output modules for CSV and JSON.
*   (Optional) Add a SQLAlchemy/psycopg2 output handler to directly `INSERT` chaotic rows into a local Postgres database.
