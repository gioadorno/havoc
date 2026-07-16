# havoc 🌪️

**The Chaos Data Generator for Defensive Engineering**

## Overview
You need to test your dashboard's virtualization and your backend's memory limits, but you cannot use real client data due to privacy constraints, and standard fake data (like faker.js) is too "clean".

`havoc` is a Python CLI pipeline that generates realistic, intentionally flawed datasets. It leverages Google Vertex AI (Gemini) to hallucinate complex edge cases and injects structural chaos based on configurable parameters.

## Features
*   **LLM-Powered Generation:** Uses Gemini 3.1 Pro to generate highly realistic, domain-specific mock data (e.g., realistic medical records or supply chain logs).
*   **Configurable Chaos Levels:** Inject nulls, malformed dates, type mismatches, and Unicode anomalies at specific percentage rates.
*   **Direct Injection:** Output data to CSV, JSON, or pump it directly into a local PostgreSQL container for immediate load testing.

## Usage
```bash
# Generate 10,000 rows of chaotic user data based on a JSON schema
python generator.py --schema user_table.json --rows 10000 --chaos high --output ./mock_dump.csv
```

## FDE Philosophy
**Attack your own infrastructure.** Proving system resilience means hitting it with the worst possible data before the client does. If your pipeline survives the `havoc`, it will survive production.
