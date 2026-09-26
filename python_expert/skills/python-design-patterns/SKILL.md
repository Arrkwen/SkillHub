---
name: python-design-patterns
description: Python design principles (KISS, separation of concerns, single responsibility, composition over inheritance, rule of three, Pythonic style) and the 23 Gang of Four patterns in idiomatic Python. Use when designing a new service or component and choosing how to layer responsibilities, when refactoring a God class or tangled module-level functions, when deciding whether to add an abstraction or live with duplication, when reviewing a pull request for tight coupling or leaking internal types, when choosing between inheritance and composition, when I/O and business logic are entangled, or when a named pattern is in play (factory, abstract factory, builder, prototype, singleton, adapter, bridge, composite, decorator, facade, flyweight, proxy, chain of responsibility, command, interpreter, iterator, mediator, memento, observer, state, strategy, template method, visitor). Also use for pattern-shaped problems that are not named yet, such as a type switch, a constructor with many parameters, a tree of nodes, undo, or a subsystem that needs one entry point.
---

# Python Design Patterns

Write maintainable Python code using fundamental design principles. These patterns help you build systems that are easy to understand, test, and modify.

## When to Use This Skill

- Designing new components or services
- Refactoring complex or tangled code
- Deciding whether to create an abstraction
- Choosing between inheritance and composition
- Evaluating code complexity and coupling
- Planning modular architectures
- Choosing or implementing a named object pattern
- A type switch, a many-parameter constructor, a tree, undo, or a subsystem with no single entry point
- Choosing a function, a class, or a dataclass for the next unit

## Core Concepts

### 1. KISS (Keep It Simple)

Choose the simplest solution that works. Complexity must be justified by concrete requirements.

### 2. Single Responsibility (SRP)

Each unit should have one reason to change. Separate concerns into focused components.

### 3. Composition Over Inheritance

Build behavior by combining objects, not extending classes.

### 4. Rule of Three

Wait until you have three instances before abstracting. Duplication is often better than premature abstraction.

### 5. Pythonic style

Use the language feature that fits: a function for a transform, a `@dataclass` for data, a class for state or identity, a `Protocol` when implementations must swap. A module is the namespace — not a class of unused `self`.

## Quick Start

```python
# Simple beats clever
# Instead of a factory/registry pattern:
FORMATTERS = {"json": JsonFormatter, "csv": CsvFormatter}

def get_formatter(name: str) -> Formatter:
    return FORMATTERS[name]()
```

## Object patterns

The principles above still decide whether a pattern is worth writing. Prefer the language feature that already is the pattern. Do not port a Java inheritance tree into Python.

Full intent, the Python form, a short example, and when not to use each of the 23 Gang of Four patterns: `references/gof.md`.

Patterns that look alike:

- **Adapter, facade, proxy, decorator** all wrap something. Adapter changes the interface. Facade hides a subsystem behind one entry. Proxy keeps the interface and controls access. Decorator keeps the interface and adds behavior that can stack.
- **Strategy and state** both swap an object. The caller picks a strategy. A state changes itself when the context transitions.
- **Strategy and template method** both vary part of an algorithm. Strategy passes the varying part in. Template method fixes the sequence in one place and lets steps differ.
- **Factory method, abstract factory, and builder** construct objects. Factory method picks one product. Abstract factory picks a family that must stay consistent. Builder assembles one object whose parts have an order.
- **Composite and decorator** both recurse. Composite combines children. Decorator wraps one object and adds one behavior.
- **Chain of responsibility, command, mediator, and observer** connect senders and receivers. A chain passes one request along handlers. A command turns the request into a value you can queue or undo. A mediator stops a mesh of objects from calling each other. An observer notifies many listeners of one change.

## Detailed patterns and worked examples

Worked examples for the principles live in `references/details.md`. The object-pattern catalog lives in `references/gof.md`. Read the file that matches the question.

## Best Practices Summary

1. **Keep it simple** - Choose the simplest solution that works
2. **Single responsibility** - Each unit has one reason to change
3. **Separate concerns** - Distinct layers with clear purposes
4. **Compose, don't inherit** - Combine objects for flexibility
5. **Rule of three** - Wait before abstracting
6. **Keep functions small** - 20-50 lines (varies by complexity), one purpose
7. **Inject dependencies** - Constructor injection for testability
8. **Delete before abstracting** - Remove dead code, then consider patterns
9. **Test each layer** - Isolated tests for each concern
10. **Explicit over clever** - Readable code beats elegant code
11. **Pythonic style** - Use the language feature that fits

## Troubleshooting

**A class is growing and seems to have multiple responsibilities, but splitting it feels wrong.**
Apply the "reason to change" test: list every change that could require editing this class. If the list has items from different domains (e.g., HTTP parsing AND business rules AND formatting), split it. If all changes stem from the same domain concern, the class may be appropriately sized.

**Injecting all dependencies through the constructor is producing constructors with 7+ parameters.**
This is a sign of too many responsibilities in one class, not a problem with dependency injection. Split the class into smaller units first, then each constructor naturally becomes smaller.

**Composition is producing deeply nested wrapper objects that are hard to trace.**
Keep the composition shallow (2-3 levels). If wrapping is the only mechanism, consider whether a Protocol-based approach or simple function composition would be cleaner than a chain of decorator objects.

**The rule of three says not to abstract yet, but the duplication is causing bugs when one copy is updated but not the other.**
Duplication that diverges in dangerous ways should be abstracted sooner. The rule of three is a heuristic, not a law. If the copies are already diverging incorrectly, extract immediately and add a test that exercises the shared behavior.

**A service layer is importing from the API layer, breaking the dependency direction.**
This is a layering violation. The service layer must not import from handlers. Introduce a shared types/models layer that both can import from, keeping the dependency arrow pointing downward (API → Service → Repository).

**The current code is all functions. Should it become classes?**
Only when a function is already acting like an object (hidden state, shared collaborators, mixed I/O). A class that never uses `self` should be a module.

## Related Skills

- [python-testing-patterns](../python-testing-patterns/SKILL.md) — Test each layer in isolation using the dependency injection structure established here
- [python-project-structure](../python-project-structure/SKILL.md) — Organize modules and directory layout so layer boundaries are explicit from the start

## Source

Adapted from [`wshobson/agents`](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-design-patterns). This copy may differ from upstream.
