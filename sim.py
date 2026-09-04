#!/usr/bin/env python3
"""
sim.py - Gerenciador de simulação progressiva para CodeSignal
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
STATE_FILE = ROOT_DIR / ".sim_state.json"


def discover_mocks() -> dict[str, dict[str, str | int]]:
    mocks = {}

    for mock_dir in sorted(ROOT_DIR.iterdir()):
        levels_dir = mock_dir / ".levels"
        if not mock_dir.is_dir() or not levels_dir.is_dir():
            continue

        level_numbers = []
        for level_file in levels_dir.glob("level_*.md"):
            match = re.fullmatch(r"level_(\d+)\.md", level_file.name)
            if match:
                level_numbers.append(int(match.group(1)))

        header_file = levels_dir / "header.md"
        stubs_file = levels_dir / "stubs_full.py"
        if not level_numbers or not header_file.exists() or not stubs_file.exists():
            continue

        title = header_file.read_text(encoding="utf-8").splitlines()[0]
        name = title.removeprefix("#").strip()

        tree = ast.parse(stubs_file.read_text(encoding="utf-8"))
        class_node = next(
            (node for node in tree.body if isinstance(node, ast.ClassDef)), None
        )
        if class_node is None:
            continue

        mocks[mock_dir.name] = {
            "id": mock_dir.name,
            "name": name,
            "class_name": class_node.name,
            "total_levels": max(level_numbers),
        }

    return mocks


MOCKS = discover_mocks()


def normalize_mock(name: str | None) -> str | None:
    if not name:
        return None
    name = name.strip().lower().replace("-", "_").replace(" ", "_")
    if name in MOCKS:
        return name
    return None


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            mocks_state = state.setdefault("mocks", {})

            for missing_mock in set(mocks_state) - set(MOCKS):
                del mocks_state[missing_mock]

            for mock, mock_info in MOCKS.items():
                saved = mocks_state.setdefault(mock, {"current_level": 1})
                total_levels = int(mock_info["total_levels"])
                saved["current_level"] = min(
                    max(saved.get("current_level", 1), 1), total_levels
                )
                saved["total_levels"] = total_levels

            state.pop("active_mock", None)

            return state
        except (json.JSONDecodeError, OSError):
            pass

    default_state = {
        "mocks": {
            mock: {
                "current_level": 1,
                "total_levels": mock_info["total_levels"],
            }
            for mock, mock_info in MOCKS.items()
        },
    }
    save_state(default_state)
    return default_state


def save_state(state: dict) -> None:
    STATE_FILE.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def get_mock(requested: str | None) -> str:
    if requested:
        normalized = normalize_mock(requested)
        if normalized:
            return normalized
        options = ", ".join(MOCKS)
        print(f"❌ Mock inválido: '{requested}'. Opções: {options}")
        sys.exit(1)

    print("⚠️  Informe a pasta do mock (ex: employee_system).")
    sys.exit(1)


def build_readme_content(mock: str, max_level: int) -> str:
    mock_dir = ROOT_DIR / mock
    levels_dir = mock_dir / ".levels"
    header_file = levels_dir / "header.md"
    total_levels = int(MOCKS[mock]["total_levels"])

    parts = []
    if header_file.exists():
        parts.append(header_file.read_text(encoding="utf-8").strip())

    for lvl in range(1, max_level + 1):
        lvl_file = levels_dir / f"level_{lvl}.md"
        if lvl_file.exists():
            parts.append(lvl_file.read_text(encoding="utf-8").strip())

    if max_level < total_levels:
        parts.append(
            f"---\n> 💡 Quando passar nos testes deste nível (`uv run sim test {mock}`), use `uv run sim next {mock}` para desbloquear o Level {max_level + 1}."
        )
    else:
        parts.append(
            f"---\n> 🏆 Parabéns! Todos os {total_levels} níveis deste mock foram desbloqueados. Valide o resultado final com `uv run sim test {mock}`!"
        )

    return "\n\n".join(parts) + "\n"


def reset_solution(mock: str) -> None:
    class_name = MOCKS[mock]["class_name"]
    solution_file = ROOT_DIR / mock / "solution.py"
    clean_code = f"class {class_name}:\n    def __init__(self):\n        pass\n"
    solution_file.write_text(clean_code, encoding="utf-8")


def sync_tests(mock: str, current_level: int) -> None:
    mock_dir = ROOT_DIR / mock
    source_tests = mock_dir / ".levels" / "tests"

    for dest_file in mock_dir.glob("test_question_*.py"):
        match = re.fullmatch(r"test_question_(\d+)\.py", dest_file.name)
        if not match:
            continue
        level = int(match.group(1))
        if level > current_level or not (source_tests / dest_file.name).exists():
            dest_file.unlink()

    for src_file in source_tests.glob("test_question_*.py"):
        match = re.fullmatch(r"test_question_(\d+)\.py", src_file.name)
        if match and int(match.group(1)) <= current_level:
            shutil.copy2(src_file, mock_dir / src_file.name)


def cmd_test(args: argparse.Namespace) -> int:
    state = load_state()
    mock = get_mock(args.mock)
    current_level = state["mocks"][mock]["current_level"]

    sync_tests(mock, current_level)
    readme_file = ROOT_DIR / mock / "README.md"
    readme_file.write_text(build_readme_content(mock, current_level), encoding="utf-8")
    save_state(state)

    print(f"🧪 Executando testes para {MOCKS[mock]['name']}...")
    cmd = [sys.executable, "-m", "pytest", f"{mock}/", *args.pytest_args]
    result = subprocess.run(cmd, cwd=ROOT_DIR, check=False)
    return result.returncode


def cmd_next(args: argparse.Namespace) -> int:
    state = load_state()
    mock = get_mock(args.mock)
    total_levels = int(MOCKS[mock]["total_levels"])
    mock_info = state["mocks"].setdefault(
        mock, {"current_level": 1, "total_levels": total_levels}
    )
    current_level = mock_info.get("current_level", 1)

    sync_tests(mock, current_level)
    readme_file = ROOT_DIR / mock / "README.md"
    readme_file.write_text(build_readme_content(mock, current_level), encoding="utf-8")
    save_state(state)

    if current_level >= total_levels:
        print(
            f"🏆 {MOCKS[mock]['name']} já está no nível máximo "
            f"(Level {total_levels} de {total_levels})!"
        )
        return 0

    next_level = current_level + 1
    print(
        f"🔍 Validando testes até o Level {current_level} para {MOCKS[mock]['name']}..."
    )

    # Executar pytest para os testes até o nível atual
    test_files = [
        f"{mock}/test_question_{lvl}.py" for lvl in range(1, current_level + 1)
    ]
    cmd = [sys.executable, "-m", "pytest", "-q", "--tb=short", *test_files]
    result = subprocess.run(cmd, cwd=ROOT_DIR, check=False)

    if result.returncode != 0:
        print()
        print("❌ BLOQUEADO: Você ainda tem testes falhando no nível atual!")
        print(
            f"👉 Resolva os requisitos do Level {current_level} antes de avançar para o Level {next_level}."
        )
        print(f"💡 Use `uv run sim test {mock}` para ver os erros.")
        return 1

    # Atualizar nível, README e testes
    mock_info["current_level"] = next_level
    save_state(state)

    readme_file.write_text(build_readme_content(mock, next_level), encoding="utf-8")
    sync_tests(mock, next_level)

    print()
    print("=" * 60)
    print(f"🎉 PARABÉNS! Todos os testes do Level {current_level} passaram!")
    print(f"🔓 Level {next_level} de {total_levels} desbloqueado com sucesso!")
    print("=" * 60)
    print(f"📖 Novos requisitos e assinaturas adicionados em: {mock}/README.md")
    print(f"🧪 Novo arquivo de teste liberado: {mock}/test_question_{next_level}.py")
    print(f"✍️  Adicione os novos métodos em: {mock}/solution.py")
    print(f"🧪 Teste com: uv run sim test {mock}")
    print("=" * 60)
    return 0


def print_status() -> None:
    state = load_state()

    print("=" * 64)
    print("                CodeSignal - Status dos Mocks")
    print("=" * 64)

    for m in MOCKS:
        total_levels = int(MOCKS[m]["total_levels"])
        info = state["mocks"].get(m, {"current_level": 1, "total_levels": total_levels})
        lvl = info.get("current_level", 1)
        progress = "■" * lvl + "□" * (total_levels - lvl)
        print(f"  {MOCKS[m]['name']:<35} [{progress}] Level {lvl}/{total_levels}")

    print("=" * 64)
    print("Comandos:")
    print("  uv run sim test <pasta>   # Exemplo: employee_system")
    print("  uv run sim next <pasta>   # Exemplo: employee_system")
    print("  uv run sim reset <pasta>  # Exemplo: employee_system")
    print("=" * 64)


def cmd_reset(args: argparse.Namespace) -> int:
    state = load_state()
    mock = get_mock(args.mock)

    state["mocks"][mock] = {
        "current_level": 1,
        "total_levels": int(MOCKS[mock]["total_levels"]),
    }
    save_state(state)

    readme_file = ROOT_DIR / mock / "README.md"
    readme_file.write_text(build_readme_content(mock, 1), encoding="utf-8")
    reset_solution(mock)
    sync_tests(mock, 1)

    print(f"🔄 {MOCKS[mock]['name']} reiniciado com sucesso para o Level 1.")
    print(f"   • {mock}/README.md redefinido para Level 1.")
    print(f"   • {mock}/solution.py limpo (apenas classe base).")
    print(f"   • {mock}/test_question_1.py ativo (testes futuros removidos).")
    return 0


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="sim",
        description="Simulador progressivo de mocks do CodeSignal",
    )
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # test
    p_test = subparsers.add_parser("test", help="Executa os testes de um mock")
    p_test.add_argument("mock", help="Nome da pasta")
    p_test.add_argument(
        "pytest_args",
        nargs=argparse.REMAINDER,
        help="Argumentos extras para o pytest",
    )
    p_test.set_defaults(func=cmd_test)

    # next
    p_next = subparsers.add_parser(
        "next", help="Avança para o próximo nível se os testes passarem"
    )
    p_next.add_argument("mock", help="Nome da pasta")
    p_next.set_defaults(func=cmd_next)

    # reset
    p_reset = subparsers.add_parser("reset", help="Reinicia um simulado para o Level 1")
    p_reset.add_argument("mock", help="Nome da pasta")
    p_reset.set_defaults(func=cmd_reset)

    parsed_args = parser.parse_args(argv)
    if not parsed_args.command:
        print_status()
        return

    exit_code = parsed_args.func(parsed_args)
    sys.exit(exit_code or 0)


if __name__ == "__main__":
    main()
