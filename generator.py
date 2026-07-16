import argparse
import json
import os
import random
import sys
import pandas as pd
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

def parse_args():
    parser = argparse.ArgumentParser(description="🌪️ havoc: The Chaos Data Generator")
    parser.add_argument("--schema", type=str, required=True, help="Path to JSON schema file")
    parser.add_argument("--rows", type=int, default=100, help="Number of rows to generate")
    parser.add_argument("--chaos", type=str, choices=["none", "low", "medium", "high"], default="low", help="Level of intentional data corruption")
    parser.add_argument("--output", type=str, default="mock_dump.csv", help="Output file path (CSV or JSON)")
    parser.add_argument("--model", type=str, default=None, help="Vertex AI model name (Default: env VERTEX_MODEL_NAME or gemini-3.1-pro-preview)")
    return parser.parse_args()

def init_gemini(model_name=None):
    project = os.environ.get("GOOGLE_VERTEX_PROJECT", "extreme-karma-gm")
    location = os.environ.get("GOOGLE_VERTEX_LOCATION", "global")
    
    vertexai.init(project=project, location=location)
    
    selected_model = model_name or os.environ.get("VERTEX_MODEL_NAME", "gemini-3.1-pro-preview")
    return GenerativeModel(selected_model)

def generate_clean_data(model, schema_str, num_rows):
    prompt = f"""
    You are an expert data engineer. Generate EXACTLY {num_rows} rows of highly realistic mock data.
    The data MUST be formatted as a pure JSON array of objects.
    
    Here is the schema mapping (Column Name: Data Type / Description):
    {schema_str}
    
    DO NOT wrap the response in markdown blocks like ```json. Return ONLY the raw JSON array.
    Ensure names, dates, and numbers look like real-world production data.
    """
    
    print(f"🧠 Asking Vertex AI to hallucinate {num_rows} realistic records...")
    
    config = GenerationConfig(temperature=0.8)
    response = model.generate_content(prompt, generation_config=config)
    
    try:
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
        
        data = json.loads(raw_text)
        return data
    except Exception as e:
        print(f"❌ Failed to parse Vertex AI output as JSON: {e}")
        print("Raw output:")
        print(response.text)
        sys.exit(1)

def apply_chaos(df, chaos_level):
    if chaos_level == "none":
        return df
        
    rates = {
        "low": {"null": 0.05, "type": 0.02, "unicode": 0.01},
        "medium": {"null": 0.15, "type": 0.05, "unicode": 0.05},
        "high": {"null": 0.30, "type": 0.15, "unicode": 0.10},
    }
    r = rates[chaos_level]
    
    print(f"🌪️ Injecting {chaos_level.upper()} chaos...")
    
    for col in df.columns:
        for idx in df.index:
            roll = random.random()
            
            if roll < r["null"]:
                df.at[idx, col] = None
                continue
                
            elif roll < (r["null"] + r["type"]):
                df.at[idx, col] = random.choice(["N/A", "UNKNOWN", "ERR", "NaN", "   "])
                continue
                
            elif pd.api.types.is_string_dtype(df[col]) and roll < (r["null"] + r["type"] + r["unicode"]):
                val = str(df.at[idx, col])
                df.at[idx, col] = val + random.choice(["\u0000", "🔥", "DROP TABLE", "\n\r", "   "])
                
    return df

def main():
    args = parse_args()
    
    with open(args.schema, 'r') as f:
        schema_str = f.read()
        
    model = init_gemini(args.model)
    
    batch_size = 50
    all_data = []
    
    remaining = args.rows
    while remaining > 0:
        current_batch = min(batch_size, remaining)
        batch_data = generate_clean_data(model, schema_str, current_batch)
        all_data.extend(batch_data)
        remaining -= current_batch
        
    df = pd.DataFrame(all_data)
    df = apply_chaos(df, args.chaos)
    
    if args.output.endswith('.json'):
        df.to_json(args.output, orient='records', indent=2)
    else:
        df.to_csv(args.output, index=False)
        
    print(f"✅ Generated {len(df)} chaotic records -> {args.output}")

if __name__ == "__main__":
    main()
