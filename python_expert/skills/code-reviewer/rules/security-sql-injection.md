---
title: SQL Injection Prevention
impact: CRITICAL
category: security
tags: sql, security, injection, database
---

# SQL Injection Prevention

Never construct SQL queries with string concatenation or f-strings. Always use parameterized queries to prevent SQL injection attacks.

## Why This Matters

SQL injection is one of the most common and dangerous web vulnerabilities. Attackers can:
- Access unauthorized data
- Modify or delete database records
- Execute admin operations on the database
- In some cases, issue commands to the OS

## ❌ Incorrect

**Problem:** User input directly interpolated into SQL query.

```python
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = db.execute(query)
    return result

# Vulnerable to: get_user("1 OR 1=1")
# Executes: SELECT * FROM users WHERE id = 1 OR 1=1
# Returns all users!
```

**Why it's dangerous:**
- Attacker can inject arbitrary SQL
- Can bypass authentication
- Can extract entire database
- Simple user input becomes code execution

## ✅ Correct

**Solution:** Use the ORM. If raw SQL is required, pass values separately from the query string. Do not use `?` as the Python default: Django uses `%s`, SQLAlchemy uses `:name`.

```python
def get_user(session: Session, user_id: int) -> User | None:
    return session.scalar(select(User).where(User.id == user_id))
```

**Why it's safe:**
- The value is a bound parameter, not part of the SQL string
- The driver sends it as data
- Query structure cannot be changed by the input

## Framework-Specific Solutions

### SQLAlchemy 2.0 (Python)
```python
from sqlalchemy import select, text

# ORM
user = session.scalar(select(User).where(User.id == user_id))

# Core
stmt = select(users).where(users.c.id == user_id)

# text() with a named bind
stmt = text("SELECT * FROM users WHERE id = :id")
result = session.execute(stmt, {"id": user_id})
```

### Django (Python)
```python
# ✅ Using ORM
User.objects.get(id=user_id)

# ✅ Using raw SQL with parameters
User.objects.raw("SELECT * FROM users WHERE id = %s", [user_id])
```

### Node.js (PostgreSQL)
```javascript
// ✅ Using parameterized query
const result = await client.query(
  'SELECT * FROM users WHERE id = $1',
  [userId]
);
```

### Node.js (MySQL)
```javascript
// ✅ Using placeholder
const [rows] = await connection.execute(
  'SELECT * FROM users WHERE id = ?',
  [userId]
);
```

## Additional Best Practices

1. **Validate input types**
   ```python
   def get_user(user_id: int) -> User | None:
       if not isinstance(user_id, int):
           raise ValueError("user_id must be an integer")
       # ... query
   ```

2. **Use ORMs when possible**
   - ORMs handle parameterization automatically
   - Reduces risk of manual SQL errors
   - Provides abstraction and type safety

3. **Principle of least privilege**
   - Database users should have minimal permissions
   - Read-only accounts for SELECT operations
   - Limits damage from successful injection

4. **Input validation as defense-in-depth**
   - Parameterization is primary defense
   - Validation provides additional layer
   - Whitelist allowed characters/patterns

## References

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)
- [SQLAlchemy SQL Injection Prevention](https://docs.sqlalchemy.org/en/14/core/tutorial.html#using-textual-sql)
