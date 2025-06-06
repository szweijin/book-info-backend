import time
from app import db
from sqlalchemy import text

def measure_query_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[Query Time] {func.__name__}: {(end - start)*1000:.2f} ms")
        return result
    return wrapper

def explain_query(sql):
    explain_result = db.session.execute(text(f"EXPLAIN {sql}"))
    plan = "\n".join(row[0] for row in explain_result)
    print(f"[EXPLAIN]\n{plan}")
    return plan
