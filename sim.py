#!/usr/bin/env python3
"""
sim.py - Gerenciador de simulação progressiva para CodeSignal
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
STATE_FILE = ROOT_DIR / ".sim_state.json"

MOCKS = {
    "mock3": {
        "id": "mock3",
        "name": "Mock 3 — In-Memory Database",
        "class_name": "InMemoryDB",
        "order": 1,
    },
    "mock1": {
        "id": "mock1",
        "name": "Mock 1 — File Storage",
        "class_name": "FileStorage",
        "order": 2,
    },
    "mock4": {
        "id": "mock4",
        "name": "Mock 4 — Employee System",
        "class_name": "EmployeeSystem",
        "order": 3,
    },
    "mock2": {
        "id": "mock2",
        "name": "Mock 2 — Banking System",
        "class_name": "BankingSystem",
        "order": 4,
    },
}


def normalize_mock(name: str | None) -> str | None:
    if not name:
        return None
    name = name.strip().lower()
    if name in MOCKS:
        return name
    if name in {"1", "m1"}:
        return "mock1"
    if name in {"2", "m2"}:
        return "mock2"
    if name in {"3", "m3"}:
        return "mock3"
    if name in {"4", "m4"}:
        return "mock4"
    return None


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {
        "active_mock": "mock3",
        "mocks": {m: {"current_level": 1, "total_levels": 4} for m in MOCKS},
    }


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def get_active_mock(state: dict, requested: str | None = None) -> str:
    if requested:
        normalized = normalize_mock(requested)
        if normalized:
            return normalized
        print(f"❌ Mock inválido: '{requested}'. Opções: mock1, mock2, mock3, mock4 (ou 1, 2, 3, 4)")
        sys.exit(1)
    return state.get("active_mock", "mock3")


def build_readme_content(mock: str, max_level: int) -> str:
    mock_dir = ROOT_DIR / mock
    levels_dir = mock_dir / ".levels"
    header_file = levels_dir / "header.md"

    parts = []
    if header_file.exists():
        parts.append(header_file.read_text(encoding="utf-8").strip())

    for lvl in range(1, max_level + 1):
        lvl_file = levels_dir / f"level_{lvl}.md"
        if lvl_file.exists():
            parts.append(lvl_file.read_text(encoding="utf-8").strip())

    if max_level < 4:
        parts.append(
            f"---\n> 💡 Quando passar nos testes deste nível (`uv run sim test`), use `uv run sim next` para desbloquear o Level {max_level + 1}."
        )
    else:
        parts.append(
            "---\n> 🏆 Parabéns! Todos os 4 níveis deste mock foram desbloqueados. Valide o resultado final com `uv run sim test`!"
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

    for lvl in range(1, 5):
        dest_file = mock_dir / f"test_question_{lvl}.py"
        src_file = source_tests / f"test_question_{lvl}.py"

        if lvl <= current_level:
            if not dest_file.exists() and src_file.exists():
                shutil.copy2(src_file, dest_file)
        else:
            if dest_file.exists():
                dest_file.unlink()



def cmd_start(args: argparse.Namespace) -> int:
    state = load_state()
    mock = get_active_mock(state, args.mock)
    state["active_mock"] = mock

    mock_info = state["mocks"].setdefault(mock, {"current_level": 1, "total_levels": 4})
    current_level = mock_info.get("current_level", 1)

    # Garantir que o README reflete o nível atual e testes sincronizados
    readme_file = ROOT_DIR / mock / "README.md"
    readme_file.write_text(build_readme_content(mock, current_level), encoding="utf-8")
    sync_tests(mock, current_level)

    save_state(state)

    print("=" * 60)
    print(f"🚀 Simulado Ativo: {MOCKS[mock]['name']}")
    print(f"📍 Nível Atual: Level {current_level} de 4")
    print("=" * 60)
    print(f"📖 Enunciado e assinaturas : {mock}/README.md")
    print(f"✍️  Arquivo para solução    : {mock}/solution.py")
    print("🧪 Executar testes          : uv run sim test")
    print("⏭️  Avançar de nível        : uv run sim next")
    print("=" * 60)
    return 0


def cmd_test(args: argparse.Namespace) -> int:
    state = load_state()
    mock = get_active_mock(state, args.mock)

    print(f"🧪 Executando testes para {MOCKS[mock]['name']}...")
    cmd = [sys.executable, "-m", "pytest", f"{mock}/", *args.pytest_args]
    result = subprocess.run(cmd, cwd=ROOT_DIR, check=False)
    return result.returncode


def cmd_next(args: argparse.Namespace) -> int:
    state = load_state()
    mock = get_active_mock(state, args.mock)
    mock_info = state["mocks"].setdefault(mock, {"current_level": 1, "total_levels": 4})
    current_level = mock_info.get("current_level", 1)

    if current_level >= 4:
        print(f"🏆 {MOCKS[mock]['name']} já está no nível máximo (Level 4 de 4)!")
        return 0

    next_level = current_level + 1
    print(f"🔍 Validando testes até o Level {current_level} para {MOCKS[mock]['name']}...")

    # Executar pytest para os testes até o nível atual
    test_files = [f"{mock}/test_question_{lvl}.py" for lvl in range(1, current_level + 1)]
    cmd = [sys.executable, "-m", "pytest", "-q", "--tb=short", *test_files]
    result = subprocess.run(cmd, cwd=ROOT_DIR, check=False)

    if result.returncode != 0:
        print()
        print("❌ BLOQUEADO: Você ainda tem testes falhando no nível atual!")
        print(f"👉 Resolva os requisitos do Level {current_level} antes de avançar para o Level {next_level}.")
        print("💡 Use `uv run sim test` para ver o relatório detalhado de erros.")
        return 1

    # Atualizar nível, README e testes
    mock_info["current_level"] = next_level
    save_state(state)

    readme_file = ROOT_DIR / mock / "README.md"
    readme_file.write_text(build_readme_content(mock, next_level), encoding="utf-8")
    sync_tests(mock, next_level)

    print()
    print("=" * 60)
    print(f"🎉 PARABÉNS! Todos os testes do Level {current_level} passaram!")
    print(f"🔓 Level {next_level} de 4 desbloqueado com sucesso!")
    print("=" * 60)
    print(f"📖 Novos requisitos e assinaturas adicionados em: {mock}/README.md")
    print(f"🧪 Novo arquivo de teste liberado: {mock}/test_question_{next_level}.py")
    print(f"✍️  Adicione os novos métodos em: {mock}/solution.py")
    print("🧪 Teste quando estiver pronto com: uv run sim test")
    print("=" * 60)
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    state = load_state()
    active_mock = state.get("active_mock", "mock3")

    # Mocks ordenados pela ordem recomendada
    sorted_mocks = sorted(MOCKS.keys(), key=lambda m: MOCKS[m]["order"])

    print("=" * 64)
    print("                CodeSignal - Status dos Mocks")
    print("=" * 64)
    print(f"Simulado ativo: {MOCKS[active_mock]['name']}\n")

    for m in sorted_mocks:
        info = state["mocks"].get(m, {"current_level": 1, "total_levels": 4})
        lvl = info.get("current_level", 1)
        is_active = " [ATIVO]" if m == active_mock else ""
        progress = "■" * lvl + "□" * (4 - lvl)
        print(f"  [{MOCKS[m]['order']}] {MOCKS[m]['name']:<35} [{progress}] Level {lvl}/4{is_active}")

    print("=" * 64)
    print("Comandos:")
    print("  uv run sim start <mock>   # Seleciona mock (ex: mock3 ou 3)")
    print("  uv run sim test           # Executa os testes do mock ativo")
    print("  uv run sim next           # Desbloqueia o próximo nível (após passar nos testes)")
    print("  uv run sim reset <mock>   # Reinicia o mock para o Level 1")
    print("=" * 64)
    return 0


def cmd_reset(args: argparse.Namespace) -> int:
    state = load_state()
    mock = get_active_mock(state, args.mock)

    state["mocks"][mock] = {"current_level": 1, "total_levels": 4}
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

    # start
    p_start = subparsers.add_parser("start", help="Inicia ou ativa um simulado")
    p_start.add_argument("mock", nargs="?", help="Nome ou número do mock (ex: mock3 ou 3)")
    p_start.set_defaults(func=cmd_start)

    # test
    p_test = subparsers.add_parser("test", help="Executa testes do mock ativo")
    p_test.add_argument("mock", nargs="?", help="Nome ou número do mock (opcional)")
    p_test.add_argument(
        "pytest_args",
        nargs=argparse.REMAINDER,
        help="Argumentos extras para o pytest",
    )
    p_test.set_defaults(func=cmd_test)

    # next
    p_next = subparsers.add_parser("next", help="Avança para o próximo nível se os testes passarem")
    p_next.add_argument("mock", nargs="?", help="Nome ou número do mock (opcional)")
    p_next.set_defaults(func=cmd_next)

    # status
    p_status = subparsers.add_parser("status", help="Exibe o status e progresso dos mocks")
    p_status.set_defaults(func=cmd_status)

    # reset
    p_reset = subparsers.add_parser("reset", help="Reinicia um simulado para o Level 1")
    p_reset.add_argument("mock", nargs="?", help="Nome ou número do mock (opcional)")
    p_reset.set_defaults(func=cmd_reset)

    parsed_args = parser.parse_args(argv)
    if not parsed_args.command:
        cmd_status(parsed_args)
        sys.exit(0)

    exit_code = parsed_args.func(parsed_args)
    sys.exit(exit_code or 0)


if __name__ == "__main__":
    main()
