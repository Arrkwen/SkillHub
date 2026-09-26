---
title: Add Type Hints
impact: MEDIUM
category: maintainability
tags: types, python, typescript, type-safety
---

# Add Type Hints

Use type annotations to make code self-documenting and catch errors early.

## Why This Matters

Type hints provide:
- **Static analysis** - catch bugs before runtime
- **Better IDE support** - autocomplete, refactoring
- **Documentation** - types explain intent
- **Confidence** - easier refactoring

##❌ Incorrect

```python
# ❌ No type hints
def get_user(id):
    return users.get(id)

def process_order(order, discount):
    if discount:
        return order['total'] * (1 - discount)
    return order['total']
```

## ✅ Correct

```python
# ✅ Python 3.10+ unions. Name the domain type. Do not use Optional, Dict, or Any.
def get_user(user_id: int) -> User | None:
    """Fetch user by ID."""
    return users.get(user_id)

def process_order(order: Order, discount: float | None = None) -> float:
    """Calculate order total with an optional discount rate."""
    if discount is not None:
        return order.total * (1 - discount)
    return order.total
```

## TypeScript

```typescript
// ✅ Explicit types
interface User {
  id: number;
  name: string;
  email: string;
}

function getUser(id: number): User | null {
  return users.get(id) ?? null;
}

function processOrder(
  order: { total: number },
  discount?: number
): number {
  if (discount) {
    return order.total * (1 - discount);
  }
  return order.total;
}
```

## References

- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
