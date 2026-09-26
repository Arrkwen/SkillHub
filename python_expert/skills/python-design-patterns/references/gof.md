# Gang of Four patterns in Python

Twenty-three object patterns in Pythonic style. See `SKILL.md`. A function, dict, generator, dataclass, `Protocol`, or class can be the pattern. Do not replace composition with a Java inheritance tree.

Required values stay required. Do not hide a missing argument behind a default. Mutable pattern state (listener lists, command history, handler chains) is created in `__init__` or with `field(default_factory=...)`, never as a class attribute or a mutable default argument.

| Pattern | Intent | Python form |
| --- | --- | --- |
| Factory method | Pick one product | `dict` of callables, or `match` |
| Abstract factory | Pick a consistent family | `Protocol` with several constructors |
| Builder | Assemble one complex object | keyword-only dataclass; a builder only for ordered steps |
| Prototype | Copy an existing object | `dataclasses.replace`, `copy.deepcopy` |
| Singleton | One shared instance | module-level object, injected at the edge |
| Adapter | Match an interface you cannot change | small wrapper |
| Bridge | Vary two axes without a class explosion | composition plus `Protocol` |
| Composite | Treat a leaf and a group the same way | shared `Protocol`, recurse |
| Decorator | Stack behavior around one object | function decorator, or a same-interface wrapper |
| Facade | One entry to a subsystem | one function or class |
| Flyweight | Share immutable state across many objects | cache the shared part |
| Proxy | Same interface, controlled access | lazy load, `__getattr__` |
| Chain of responsibility | First handler that can take the request | list of callables |
| Command | Turn an action into a value | callable; dataclass when undo is required |
| Interpreter | Evaluate a small language | a parser library, or a tiny recursive function |
| Iterator | Walk a structure without exposing it | `__iter__` / `yield` |
| Mediator | Replace a mesh of calls with one coordinator | one service the parts call |
| Memento | Snapshot and restore without leaking fields | frozen dataclass |
| Observer | Notify many listeners of one change | list of callbacks |
| State | Behavior follows internal state | `enum` + `match`, or state objects |
| Strategy | Swap an algorithm | pass a function |
| Template method | Fixed sequence, a few steps vary | function taking the steps; ABC only if the skeleton is large |
| Visitor | New operation over a stable set of types | `singledispatch` or `match` |

## Creational

### Factory method

**Intent.** Decide which concrete product to create without scattering that choice through callers.

**Use when.** The product type comes from configuration, a file extension, or a registry that grows independently of the caller.

**Python form.** A dict of callables is the factory. A class with an overridable method is only worth it when each subclass must supply its own product as part of a larger inherited algorithm.

```python
def load_parser(kind: str) -> Parser:
    try:
        return PARSERS[kind]()
    except KeyError as exc:
        raise ValueError(f"unknown parser: {kind}") from exc
```

**Do not use when.** There are two fixed types and a single `if` is clearer. See the dict example in `SKILL.md`. Do not build a registration decorator until new products are added from outside the module.

### Abstract factory

**Intent.** Create a family of objects that must match each other. Switching the family switches every member.

**Use when.** One choice implies several products, and mixing members from two families is a bug. Example: a UI theme that must produce both a button and a dialog from the same theme.

```python
from typing import Protocol

class Theme(Protocol):
    def button(self, label: str) -> Button: ...
    def dialog(self, title: str) -> Dialog: ...

def render(theme: Theme) -> None:
    button = theme.button("Save")
    dialog = theme.dialog("Confirm")
    dialog.add(button)
```

**Do not use when.** There is only one product. That is a factory method. Do not invent a family so that two unrelated constructors live on the same object.

### Builder

**Intent.** Construct an object that has many parts, some of which are optional or must be set in order, and reject an incomplete result.

**Use when.** A constructor's argument list is hard to read, or later steps depend on earlier ones and an invalid combination must fail before the object exists.

**Python form.** Start with a dataclass whose required fields have no defaults. Add a builder only when the steps themselves carry state or validation that does not belong on the finished object.

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Report:
    title: str
    body: str
    footer: str = ""

def build_report(title: str, body: str, footer: str = "") -> Report:
    if not title or not body:
        raise ValueError("title and body are required")
    return Report(title=title, body=body, footer=footer)
```

A fluent builder earns its class when each step can fail on its own and the caller must not touch a half-built object:

```python
class QueryBuilder:
    def __init__(self, table: str) -> None:
        if not table:
            raise ValueError("table is required")
        self._table = table
        self._where: list[str] = []

    def where(self, clause: str) -> "QueryBuilder":
        if not clause:
            raise ValueError("empty clause")
        self._where.append(clause)
        return self

    def build(self) -> Query:
        return Query(self._table, tuple(self._where))
```

**Do not use when.** The object is a few independent fields. Keyword arguments are the builder.

### Prototype

**Intent.** Make a new object by copying an existing one, then change the copy.

**Use when.** The starting point is an object you already have, and constructing it again would repeat work or drop fields the caller does not know about.

```python
import copy
from dataclasses import dataclass, replace

@dataclass(frozen=True, slots=True)
class Invoice:
    number: str
    total: int
    lines: list[str]

def next_invoice(current: Invoice, number: str) -> Invoice:
    return replace(current, number=number, lines=list(current.lines))

def deep_copy(current: Invoice) -> Invoice:
    return copy.deepcopy(current)
```

`replace` is shallow. Copy nested mutable fields yourself, or use `deepcopy` when the graph is nested and a shared inner list would be a bug.

**Do not use when.** A constructor call is shorter and makes the new values obvious. Do not add a `clone()` method that wraps `copy`.

### Singleton

**Intent.** Ensure there is one shared instance of something expensive or inherently unique, such as a process-wide client.

**Python form.** The module is already a singleton. Create the object in one place and pass it in. Callers depend on a parameter, not on an import of global state.

```python
def main() -> None:
    client = build_client()  # once, at the edge
    run(client)

def run(client: Client) -> None:
    client.request()
```

`functools.cache` on a zero-argument factory is acceptable when construction is expensive and the call sites cannot take a parameter. Tests must call `cache_clear()`, because the cached object survives from test to test.

**Do not use when.** You want a convenient global. A metaclass or `__new__` singleton hides the dependency and makes tests order-dependent. Two instances are usually fine; sharing one is a choice you pass in.

## Structural

### Adapter

**Intent.** Make an object you do not own satisfy the interface your code already calls.

**Use when.** A library's names or shapes do not match a `Protocol` you already have, and you cannot change the library.

```python
from typing import Protocol

class Storage(Protocol):
    def read(self, key: str) -> bytes: ...

class S3Storage:
    def __init__(self, bucket: Bucket) -> None:
        self._bucket = bucket

    def read(self, key: str) -> bytes:
        return self._bucket.get_object(Key=key)["Body"].read()
```

If the caller needs one function, adapt with a function instead of a class.

**Do not use when.** You own both sides. Change the call or the definition. Duck typing often means no adapter: if the library already has the method you call, use it directly.

### Bridge

**Intent.** Let an abstraction and its implementation vary independently, so you do not multiply subclasses for every combination.

**Use when.** Two axes both change. Example: a remote control and a device. Subclassing `AdvancedSonyRemote` and `BasicSamsungRemote` is the explosion this pattern stops.

```python
from typing import Protocol

class Device(Protocol):
    def enable(self) -> None: ...
    def set_volume(self, level: int) -> None: ...

class Remote:
    def __init__(self, device: Device) -> None:
        self._device = device

    def toggle_power(self) -> None:
        self._device.enable()

class AdvancedRemote(Remote):
    def mute(self) -> None:
        self._device.set_volume(0)
```

**Do not use when.** There is one implementation. Pass that object in; do not invent a second axis.

### Composite

**Intent.** Treat a single item and a group of items through the same operation. Groups contain items or further groups.

**Use when.** The domain is a tree: files and folders, an outline, an org chart, an expression of terms and sums.

```python
from dataclasses import dataclass
from typing import Protocol

class Node(Protocol):
    def size(self) -> int: ...

@dataclass(frozen=True, slots=True)
class File:
    bytes: int

    def size(self) -> int:
        return self.bytes

@dataclass(slots=True)
class Folder:
    children: list[Node]

    def size(self) -> int:
        return sum(child.size() for child in self.children)
```

**Do not use when.** The collection is flat. A list and a loop are the composite. Do not force leaves to implement child-management methods they cannot support.

### Decorator

**Intent.** Add behavior to an object at runtime, without subclassing, in a way that can stack.

**Python form.** For functions, use a function decorator with `functools.wraps`. For objects, wrap an instance that already matches the `Protocol` and forward the call. The wrapper is itself a valid implementation, so wrappers can nest.

```python
from typing import Protocol

class Notifier(Protocol):
    def send(self, message: str) -> None: ...

class EmailNotifier:
    def send(self, message: str) -> None:
        deliver_email(message)

class RetryNotifier:
    def __init__(self, inner: Notifier, attempts: int) -> None:
        if attempts < 1:
            raise ValueError("attempts must be >= 1")
        self._inner = inner
        self._attempts = attempts

    def send(self, message: str) -> None:
        last_error: TimeoutError | None = None
        for _ in range(self._attempts):
            try:
                self._inner.send(message)
                return
            except TimeoutError as exc:
                last_error = exc
        if last_error is None:
            raise RuntimeError("retry loop made no attempt")
        raise last_error
```

The `@decorator` syntax is this pattern applied to functions. It is not a different idea.

**Do not use when.** The extra behavior is permanent and local. A function call at the use site is clearer than a wrapper. Stop stacking once the call path is hard to follow; two or three wrappers is already deep.

### Facade

**Intent.** Offer one straightforward entry point over a subsystem that has several steps and types.

**Use when.** Callers keep repeating the same sequence of setup, calls, and teardown against a library or a cluster of your own modules.

```python
def export_csv(rows: list[dict[str, str]], path: str) -> None:
    table = normalize(rows)
    encoded = encode_csv(table)
    write_atomic(path, encoded)
```

**Do not use when.** You are about to wrap a single function in another function of the same shape. A facade that only forwards one call adds a name and no simplification. Do not let the facade become the only place business rules live; it coordinates, it does not absorb the subsystem.

### Flyweight

**Intent.** Share the immutable part of many similar objects so the process does not store that part once per instance.

**Use when.** You have measured a large number of objects whose heavy fields repeat, and the repeated fields are safe to share because nothing mutates them.

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Glyph:
    char: str
    font: str

_glyphs: dict[tuple[str, str], Glyph] = {}

def glyph(char: str, font: str) -> Glyph:
    key = (char, font)
    shared = _glyphs.get(key)
    if shared is None:
        shared = Glyph(char, font)
        _glyphs[key] = shared
    return shared
```

Keep the per-instance data (position, owner) outside the shared object.

**Do not use when.** You have not measured memory. Interning every small string or dataclass makes identity surprising and rarely saves enough to matter.

### Proxy

**Intent.** Provide the same interface as a real object while controlling how and when it is reached: lazy creation, a permission check, or a remote call.

**Use when.** Creating or calling the real object is expensive or restricted, and callers should not know which.

```python
from collections.abc import Callable

class UserProxy:
    def __init__(self, user_id: str, load: Callable[[str], User]) -> None:
        self._user_id = user_id
        self._load = load
        self._user: User | None = None

    def profile(self) -> User:
        if self._user is None:
            self._user = self._load(self._user_id)
        return self._user
```

`__getattr__` can forward unknown attributes. Prefer explicit methods when the interface is small, so typos fail immediately.

**Do not use when.** You own the real class and can put the check or the cache there. A proxy and a decorator both wrap. The proxy decides whether the call happens. The decorator lets the call happen and adds behavior around it.

## Behavioral

### Chain of responsibility

**Intent.** Give more than one handler a chance at a request, in order, until one of them handles it.

**Use when.** The handler is not known by the sender, and the order of checks should be easy to change: authentication, then validation, then authorization.

```python
from collections.abc import Callable

Handler = Callable[[Request], Response | None]

def dispatch(request: Request, handlers: list[Handler]) -> Response:
    for handler in handlers:
        result = handler(request)
        if result is not None:
            return result
    raise ValueError("no handler accepted the request")
```

Build `handlers` at the edge and pass the list in. A handler returns `None` to pass the request on.

**Do not use when.** One specific function is the handler. A chain that always has one real handler is an indirect call.

### Command

**Intent.** Represent an action as a value, so it can be queued, logged, retried, or undone.

**Use when.** The moment you decide the action is not the moment you run it, or you must reverse it later.

**Python form.** A callable is a command. Return the inverse action when the caller must undo.

```python
from collections.abc import Callable

def rename(document: Document, new_name: str) -> Callable[[], None]:
    previous = document.name
    document.name = new_name

    def undo() -> None:
        document.name = previous

    return undo
```

**Do not use when.** You call the function immediately and never store it. Do not invent a command interface of one method around a function you could pass directly.

### Interpreter

**Intent.** Represent the grammar of a small language and evaluate sentences in it.

**Use when.** The language is tiny and stable, such as a filter expression you already receive as a tree. Each grammar rule is a function or a node with an `eval` method.

**Python form.** Prefer an existing parser for anything with precedence, strings, or errors a user will see. If you already have an AST, evaluate it with recursion or `match`. Do not design a class per grammar rule unless the tree is produced elsewhere and you are only walking it.

```python
from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Number:
    value: int

@dataclass(frozen=True, slots=True)
class Name:
    ident: str

@dataclass(frozen=True, slots=True)
class Add:
    left: Expr
    right: Expr

Expr = Number | Name | Add

def evaluate(node: Expr, env: dict[str, int]) -> int:
    match node:
        case Number(value):
            return value
        case Name(ident):
            return env[ident]
        case Add(left, right):
            return evaluate(left, env) + evaluate(right, env)
        case _:
            raise TypeError(type(node))
```

**Do not use when.** The "language" is a few flags. Parse those with normal arguments. Hand-rolled interpreters grow into bad parsers.

### Iterator

**Intent.** Walk the elements of a structure without exposing how they are stored.

**Python form.** Implement `__iter__` with `yield`. A handwritten iterator class is rarely needed; a generator already holds the traversal state.

```python
from collections.abc import Iterator

class Tree:
    def __init__(self, value: int, children: list[Tree] | None = None) -> None:
        self.value = value
        self.children = [] if children is None else children

    def __iter__(self) -> Iterator[int]:
        yield self.value
        for child in self.children:
            yield from child
```

An empty list is falsy, so `children or []` would drop a list the caller passed in. Test `is None` instead. Do not write `children: list[Tree] = []` on the class: that list would be shared by every instance.

**Do not use when.** The data is already a list, tuple, or other iterable. Callers can use `for` directly.

### Mediator

**Intent.** Stop a set of objects from holding references to each other. They talk to one coordinator, which talks to them.

**Use when.** Changing one participant forces edits in many others because each one calls the rest.

```python
class Dialog:
    def __init__(self) -> None:
        self._name = ""
        self._can_save = False

    def set_name(self, name: str) -> None:
        self._name = name
        self._can_save = bool(name)

    def save(self) -> None:
        if not self._can_save:
            raise ValueError("name is required")
        store(self._name)
```

The widgets do not call each other. The dialog owns the rule that a name enables save.

**Do not use when.** Two objects collaborate. Passing one into the other is enough. A mediator that only forwards every call becomes a place where every feature lands.

### Memento

**Intent.** Capture an object's state so it can be restored later, without publishing the fields that make up that state.

**Use when.** You need undo, a transaction rollback, or a draft that can be discarded.

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class EditorSnapshot:
    text: str
    cursor: int

class Editor:
    def __init__(self, text: str) -> None:
        self._text = text
        self._cursor = 0

    def snapshot(self) -> EditorSnapshot:
        return EditorSnapshot(self._text, self._cursor)

    def restore(self, saved: EditorSnapshot) -> None:
        self._text = saved.text
        self._cursor = saved.cursor
```

Keep the snapshot frozen. Store snapshots outside the editor if history is a separate responsibility.

**Do not use when.** `replace` on an already-frozen value is the snapshot. Do not pickle the live object; a pickle restores code as well as data and breaks when the class changes.

### Observer

**Intent.** When one object changes, notify every interested listener. The subject does not know what the listeners do.

**Use when.** Several independent parts must react to the same event, and the set of listeners changes at runtime.

```python
from collections.abc import Callable

class Document:
    def __init__(self) -> None:
        self._text = ""
        self._listeners: list[Callable[[str], None]] = []

    def subscribe(self, listener: Callable[[str], None]) -> None:
        self._listeners.append(listener)

    def set_text(self, text: str) -> None:
        self._text = text
        for listener in list(self._listeners):
            listener(text)
```

Create `_listeners` in `__init__`. A class-level list would be shared by every document. Iterate a copy if a listener may unsubscribe during the call.

**Do not use when.** There is one known caller. Call it. Do not add an observer so that a child can tell its parent something the parent could have received as a return value.

### State

**Intent.** An object's behavior changes when its internal state changes, and the state knows the legal transitions.

**Use when.** Methods are full of `if self.status == ...`, and those branches must stay consistent with each other.

**Python form.** Few statuses and few methods: an `enum` and `match`. Many methods per status, or transitions that belong to the status: one object per state.

```python
from typing import Protocol

class GateState(Protocol):
    def pay(self, gate: "Gate") -> None: ...
    def enter(self, gate: "Gate") -> None: ...

class Locked:
    def pay(self, gate: "Gate") -> None:
        gate._set(Unlocked())

    def enter(self, gate: "Gate") -> None:
        raise ValueError("pay first")

class Unlocked:
    def pay(self, gate: "Gate") -> None:
        return

    def enter(self, gate: "Gate") -> None:
        gate._set(Locked())

class Gate:
    def __init__(self) -> None:
        self._state: GateState = Locked()

    def _set(self, state: GateState) -> None:
        self._state = state

    def pay(self) -> None:
        self._state.pay(self)

    def enter(self) -> None:
        self._state.enter(self)
```

The caller picks a strategy. A state object picks the next state. If the branches are independent algorithms rather than a lifecycle, use strategy.

**Do not use when.** There are two flags. An `enum` and a single `match` is the whole design.

### Strategy

**Intent.** Keep several algorithms interchangeable behind one call.

**Use when.** A function branches on a mode to choose a calculation, and new modes should not edit that function.

**Python form.** Pass a function. Use a `Protocol` only when the algorithm needs several methods or its own data.

```python
from collections.abc import Callable

def total(prices: list[int], discount: Callable[[int], int]) -> int:
    return sum(discount(price) for price in prices)

def no_discount(price: int) -> int:
    return price

def half_off(price: int) -> int:
    return price // 2
```

Select the function once, at the edge, from configuration. The dict in `SKILL.md` is this pattern used as a factory of strategies.

**Do not use when.** There are two cases and no third is coming. An `if` is the strategy.

### Template method

**Intent.** Fix the order of an algorithm in one place, and let a few steps vary.

**Use when.** Several operations share the same sequence and differ in one or two steps.

**Python form.** Pass the varying steps into the function that owns the sequence. An abstract base class is justified when the shared skeleton is large and the variants are whole objects with their own fields.

```python
from collections.abc import Callable

def migrate(rows: list[Raw], parse: Callable[[Raw], Item], save: Callable[[Item], None]) -> None:
    for row in rows:
        save(parse(row))
```

**Do not use when.** The only shared part is the idea of "do steps". Inheritance here exists to fill in hooks; if the hooks are functions, you do not need a subclass. Prefer strategy when the caller should choose the variant at runtime rather than by which class was constructed.

### Visitor

**Intent.** Add a new operation across a closed set of types without editing those types for every operation.

**Use when.** The types are stable (an AST, a document tree) and the operations keep arriving: render, measure, lint.

**Python form.** `functools.singledispatch` on the first argument, or one `match` that lists every type. Inside a class, `@singledispatch` would see `self` first; use `singledispatchmethod` and register the second parameter.

```python
import math
from dataclasses import dataclass
from functools import singledispatch

@dataclass(frozen=True, slots=True)
class Circle:
    radius: float

@dataclass(frozen=True, slots=True)
class Rect:
    width: float
    height: float

@singledispatch
def area(shape: object) -> float:
    raise TypeError(type(shape))

@area.register
def _(shape: Circle) -> float:
    return math.pi * shape.radius ** 2

@area.register
def _(shape: Rect) -> float:
    return shape.width * shape.height
```

Dispatch uses the runtime type. A subclass does not use its parent registration unless you register it too. `singledispatch` cannot branch on two arguments at once. If you need every case in one function, use `match`.

**Do not use when.** There is one operation. Give the types a method. Visitor pays off when new operations are more common than new types. If you add types often, a method on each type is the smaller change.
