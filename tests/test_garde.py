"""Teste le garde-fou SANS appeler Claude : il doit refuser toute lecture hors du dossier audité.
Lancer : python tests/test_garde.py"""
import asyncio
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit import fabriquer_garde  # noqa: E402


def decision(garde, outil, **args):
    r = asyncio.run(garde({"tool_name": outil, "tool_input": args}, None, None))
    return r.get("hookSpecificOutput", {}).get("permissionDecision", "allow")


with tempfile.TemporaryDirectory() as tmp:
    racine = Path(tmp) / "repo"
    racine.mkdir()
    garde = fabriquer_garde(racine)
    cas = [
        ("Read",  {"file_path": str(racine / "SKILL.md")},          "allow"),
        ("Read",  {"file_path": "scripts/setup.sh"},                 "allow"),
        ("Read",  {"file_path": str(Path.home() / ".ssh/id_rsa")},   "deny"),
        ("Read",  {"file_path": "../../.env"},                       "deny"),
        ("Grep",  {"pattern": "curl", "path": str(Path.home())},     "deny"),
        ("Grep",  {"pattern": "curl"},                               "allow"),
        ("Glob",  {"pattern": "**/*"},                               "allow"),
        ("Glob",  {"pattern": "../**/*"},                            "deny"),
        ("Glob",  {"pattern": str(Path.home() / "**/*.env")},        "deny"),
    ]
    ok = 0
    for outil, args, attendu in cas:
        obtenu = decision(garde, outil, **args)
        ok += obtenu == attendu
        print(f"{'✅' if obtenu == attendu else '❌'} {outil:4} {args} → {obtenu} (attendu {attendu})")
    print(f"\n{ok}/{len(cas)} cas OK")
    sys.exit(0 if ok == len(cas) else 1)
