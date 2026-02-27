import json

def structured_to_sql(structured_str):
    try:
        struct = json.loads(structured_str)
        conditions = []
        for key, value in struct.items():
            field = key.lower()
            op = value['op']
            val = value['val']
            if isinstance(val, str):
                val = f"'{val}'"
            conditions.append(f"{field} {op} {val}")
        
        where_clause = " AND ".join(conditions)
        return f"SELECT * FROM patients WHERE {where_clause}"
    except Exception as e:
        # If generation failed or format is wrong, return empty SQL
        return "SELECT * FROM patients WHERE 1=0"
