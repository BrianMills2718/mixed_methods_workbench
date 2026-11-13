"""Write the type inventory of the workbench's code: every class, where it is defined, what builds it and what reads it.

Legacy trace: system-model/type-inventory (Plan #8 planning package, docs/planning/SYSTEM_MODEL.md).

    uv run python scripts/type_inventory.py            # writes docs/planning/TYPES.md
    uv run python scripts/type_inventory.py --check    # exits 1 if TYPES.md is stale

"Built in" lists the modules that call the class or its ``model_validate``; "read in" lists the other modules
that name it (annotations, isinstance checks, imports). Both are found by parsing the code, not by reading prose.
"""

from __future__ import annotations

import argparse
import ast
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "docs" / "planning" / "TYPES.md"
ROOTS = [REPO / "src", REPO / "scripts"]


def _modules() -> list[Path]:
    return sorted(p for root in ROOTS for p in root.rglob("*.py") if "__pycache__" not in p.parts)


def _kind(node: ast.ClassDef) -> str:
    names = {b.id if isinstance(b, ast.Name) else b.attr if isinstance(b, ast.Attribute) else "" for b in node.bases}
    if names & {"Enum", "StrEnum", "IntEnum"}:
        return "enum"
    if names & {"Exception", "ValueError", "RuntimeError", "TypeError", "KeyError"} or any(
        n.endswith("Error") for n in names
    ):
        return "error"
    if any(isinstance(d, ast.Name) and d.id == "dataclass" or isinstance(d, ast.Call) and getattr(d.func, "id", "") == "dataclass" for d in node.decorator_list):
        return "dataclass"
    if names & {"TypedDict"}:
        return "typed dict"
    if names & {"Protocol"}:
        return "protocol"
    return "record" if names else "class"


def _module_path(dotted: str, rel: str, level: int) -> str | None:
    """Map an import's module to a repository path, or None when it is outside the repository."""
    if level:
        base = Path(rel).parent
        for _ in range(level - 1):
            base = base.parent
        parts = [p for p in dotted.split(".") if p] if dotted else []
        candidate = base.joinpath(*parts)
    else:
        if not dotted.startswith("mixed_methods_workbench"):
            return None
        candidate = Path("src").joinpath(*dotted.split("."))
    for option in (candidate.with_suffix(".py"), candidate / "__init__.py"):
        if (REPO / option).exists():
            return str(option)
    return None


def build() -> str:
    modules = _modules()
    # Classes are keyed by (module, name): two modules may define classes with the same name.
    defined: dict[tuple[str, str], tuple[int, str]] = {}
    by_name: dict[str, list[str]] = defaultdict(list)
    trees: dict[str, ast.Module] = {}
    for path in modules:
        rel = str(path.relative_to(REPO))
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel)
        trees[rel] = tree
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                defined[(rel, node.name)] = (node.lineno, _kind(node))
                by_name[node.name].append(rel)

    def resolve(name: str, rel: str, imports: dict[str, tuple[str, str]]) -> tuple[str, str] | None:
        if (rel, name) in defined:
            return (rel, name)
        if name in imports:
            target = imports[name]
            return target if target in defined else None
        homes = by_name.get(name, [])
        return (homes[0], name) if len(homes) == 1 else None

    built: dict[tuple[str, str], set[str]] = defaultdict(set)
    read: dict[tuple[str, str], set[str]] = defaultdict(set)
    for rel, tree in trees.items():
        imports: dict[str, tuple[str, str]] = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                home = _module_path(node.module or "", rel, node.level)
                if home is None:
                    continue
                for alias in node.names:
                    imports[alias.asname or alias.name] = (home, alias.name)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name) and func.id in by_name:
                    key = resolve(func.id, rel, imports)
                    if key:
                        built[key].add(rel)
                elif isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) and func.value.id in by_name:
                    if func.attr in {"model_validate", "model_validate_json", "model_construct", "from_dict"}:
                        key = resolve(func.value.id, rel, imports)
                        if key:
                            built[key].add(rel)
            if isinstance(node, ast.Name) and node.id in by_name:
                key = resolve(node.id, rel, imports)
                if key:
                    read[key].add(rel)
            elif isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value in by_name:
                key = resolve(node.value, rel, imports)
                if key:
                    read[key].add(rel)
    rows = []
    for key in sorted(defined, key=lambda k: (k[0], defined[k][0])):
        rel, name = key
        line, kind = defined[key]
        b = sorted(built[key])
        r = sorted(read[key] - built[key] - {rel})
        rows.append(
            f"| `{name}` | {kind} | `{rel}:{line}` | {', '.join(f'`{m}`' for m in b) or 'not called directly (built inside a parent record or a base class)'} | "
            f"{', '.join(f'`{m}`' for m in r) or 'its own module only'} |"
        )
    header = (
        "# Type inventory\n\n"
        "Generated by `scripts/type_inventory.py` from the code under `src/` and `scripts/`; do not edit by hand\n"
        "(`make type-inventory` rewrites it, `pytest` fails when it is stale). The system model,\n"
        "[SYSTEM_MODEL.md](SYSTEM_MODEL.md), says what each module does and which types Plan #8 adds.\n\n"
        f"{len(rows)} classes. \"Built in\" is every module that calls the class or its `model_validate`; \"read in\" is every\n"
        "other module that names it. A name is resolved to the class in the same module, else the one it is imported\n"
        "from, else the only class with that name; a name defined in several modules and not imported is not counted.\n"
        "Kinds: record (a Pydantic model or other typed class), enum, error, dataclass.\n\n"
        "| Type | Kind | Defined at | Built in | Read in |\n| --- | --- | --- | --- | --- |\n"
    )
    return header + "\n".join(rows) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    text = build()
    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != text:
            print("docs/planning/TYPES.md is stale: run scripts/type_inventory.py")
            return 1
        print(f"TYPES.md current ({text.count(chr(10) + '| `')} types)")
        return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)} ({text.count(chr(10) + '| `')} types)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
