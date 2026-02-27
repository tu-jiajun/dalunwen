import json
import random
import os

# Define some templates for generation
AGE_TEMPLATES = [
    ("Patient is over {val} years old", "age > {val}"),
    ("Patients younger than {val}", "age < {val}"),
    ("Age must be at least {val}", "age >= {val}"),
    ("Must be {val} or older", "age >= {val}")
]

DIAGNOSIS_TEMPLATES = [
    ("Diagnosed with {val}", "diagnosis = '{val}'"),
    ("Patient has {val}", "diagnosis = '{val}'"),
    ("Must have a history of {val}", "diagnosis = '{val}'")
]

GENDER_TEMPLATES = [
    ("Female patients only", "gender = 'Female'"),
    ("Male participants", "gender = 'Male'"),
    ("Restricted to women", "gender = 'Female'")
]

def generate_sample():
    # Randomly choose a type of criteria
    criteria_type = random.choice(["age", "diagnosis", "gender", "composite"])
    
    if criteria_type == "age":
        val = random.randint(18, 80)
        nl_temp, sql_cond = random.choice(AGE_TEMPLATES)
        nl = nl_temp.format(val=val)
        struct = {"age": {"op": sql_cond.split()[1], "val": val}}
        sql = f"SELECT * FROM patients WHERE {sql_cond.format(val=val)}"
        
    elif criteria_type == "diagnosis":
        diseases = ["Diabetes", "Hypertension", "Cancer", "Asthma"]
        val = random.choice(diseases)
        nl_temp, sql_cond = random.choice(DIAGNOSIS_TEMPLATES)
        nl = nl_temp.format(val=val)
        struct = {"diagnosis": {"op": "=", "val": val}}
        sql = f"SELECT * FROM patients WHERE {sql_cond.format(val=val)}"
        
    elif criteria_type == "gender":
        nl_temp, sql_cond = random.choice(GENDER_TEMPLATES)
        nl = nl_temp
        val = "Female" if "Female" in sql_cond else "Male"
        struct = {"gender": {"op": "=", "val": val}}
        sql = f"SELECT * FROM patients WHERE {sql_cond}"
        
    else: # Composite: Age AND Diagnosis
        val_age = random.randint(18, 80)
        nl_age, sql_age = random.choice(AGE_TEMPLATES)
        
        diseases = ["Diabetes", "Hypertension", "Cancer", "Asthma"]
        val_diag = random.choice(diseases)
        nl_diag, sql_diag = random.choice(DIAGNOSIS_TEMPLATES)
        
        nl = f"{nl_age.format(val=val_age)} and {nl_diag.format(val=val_diag)}"
        struct = {
            "age": {"op": sql_age.split()[1], "val": val_age},
            "diagnosis": {"op": "=", "val": val_diag}
        }
        sql = f"SELECT * FROM patients WHERE {sql_age.format(val=val_age)} AND {sql_diag.format(val=val_diag)}"

    return {
        "text": nl,
        "structured": json.dumps(struct),
        "sql": sql
    }

def generate_dataset(size, output_path):
    data = [generate_sample() for _ in range(size)]
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Generated {size} samples to {output_path}")

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    generate_dataset(800, "data/train.json")
    generate_dataset(100, "data/validation.json")
    generate_dataset(100, "data/test.json")
