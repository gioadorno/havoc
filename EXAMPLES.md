# Havoc: Examples & Usage

Havoc uses Google Vertex AI (Gemini) to generate hyper-realistic mock datasets, and then applies a "Chaos Engine" to intentionally break them.

## 1. Generating a Chaotic Dataset

You need to load-test a database schema but require realistic data that includes edge cases.

**The Input (`user_schema.json`):**
```json
{
  "id": "Integer (1 to 99999)",
  "full_name": "String (First and Last name)",
  "email": "String (valid email format)",
  "account_balance": "Float (between 0.00 and 50000.00)",
  "signup_date": "Date (ISO8601 format)"
}
```

**The Command:**
```bash
$ python generator.py --schema user_schema.json --rows 5 --chaos high --output out.csv
```

**The Output Logs:**
```text
🧠 Asking Vertex AI to hallucinate 5 realistic records...
🌪️ Injecting HIGH chaos...
✅ Generated 5 chaotic records -> out.csv
```

**The Result (`out.csv`):**
```csv
id,full_name,email,account_balance,signup_date
48291.0,Eleanor Vance\u0000,ERR,14520.5,2023-05-14T08:30:00Z
,ERR,mthorne88@company.net,340.75,ERR
85932.0,NaN,smartinez.design@studio.co,42199.1,ERR
2274.0,Julian Foster,julian.foster_99@webmail.org,8950.0,2024-01-15T19:42:10Z
67105.0,,cchen.analytics@data.io,,2023-09-07T09:12:33Z
```

### Actionable FDE Takeaways:
By injecting `HIGH` chaos, the pipeline successfully simulated real-world corruption:
*   **Null Byte Injection:** `Eleanor Vance\u0000` contains an invisible null byte (`\u0000`) which causes PostgreSQL `COPY` commands to fail entirely.
*   **Type Corruption:** Expected floats/dates were replaced with the string `"ERR"`.
*   **Missing PKs:** Row 2 is missing its `id` entirely.

If your code can gracefully ingest `out.csv` without crashing, it is ready for production.
