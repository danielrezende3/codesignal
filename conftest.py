import re


def get_question_number(nodeid: str) -> int:
    match = re.search(r"test_question_(\d+)\.py", nodeid)
    if match:
        return int(match.group(1))
    return 999


def pytest_collection_modifyitems(session, config, items):
    """
    Garante que os testes sejam sempre ordenados por:
    1. Diretório do mock descoberto
    2. Número da questão (test_question_1.py -> test_question_4.py)
    3. Ordem de definição dentro do arquivo de teste
    """
    items.sort(
        key=lambda item: (
            str(item.fspath.dirname),
            get_question_number(str(item.fspath)),
            item.location[1],
        )
    )
