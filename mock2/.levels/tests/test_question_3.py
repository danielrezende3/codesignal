from mock2.solution import FileStorage


def test_users_and_quotas_basic():
    fs = FileStorage()
    assert fs.add_user("daniel", 1000) is True
    assert fs.add_user("daniel", 500) is False

    assert fs.add_file_by("daniel", "/a", 400) == 600
    assert fs.add_file_by("daniel", "/b", 300) == 300
    # Ultrapassa capacidade (300 restante < 400)
    assert fs.add_file_by("daniel", "/c", 400) is None

    # Redução de capacidade: 500 total, arquivos atuais somam 700 (/a: 400, /b: 300).
    # Deve remover o maior (/a de 400). Sobra /b (300 <= 500). Removeu 1 arquivo.
    assert fs.update_capacity("daniel", 500) == 1

    assert fs.get_file_size("/a") is None
    assert fs.get_file_size("/b") == 300


def test_add_file_by_nonexistent_user_and_duplicate_filename():
    fs = FileStorage()
    fs.add_user("u1", 500)
    fs.add_file_by("u1", "/f1", 100)

    # Usuário inexistente
    assert fs.add_file_by("ghost", "/ghost.txt", 100) is None
    assert fs.update_capacity("ghost", 500) is None

    # Arquivo com nome já existente não pode ser adicionado
    assert fs.add_file_by("u1", "/f1", 50) is None
    # Quota não deve ter sido consumida
    assert fs.add_file_by("u1", "/f2", 400) == 0


def test_admin_files_do_not_consume_user_quota():
    fs = FileStorage()
    assert fs.add_user("u1", 200) is True
    # Arquivo de admin (add_file)
    assert fs.add_file("/admin_file", 1000) is True
    # u1 ainda tem seus 200 inteiros
    assert fs.add_file_by("u1", "/u1_file", 200) == 0


def test_copy_file_preserves_owner_and_checks_quota():
    fs = FileStorage()
    fs.add_user("u1", 300)
    assert fs.add_file_by("u1", "/file1", 200) == 100

    # Cópia para /file2 precisa de mais 200, mas u1 só tem 100 restante -> deve falhar
    assert fs.copy_file("/file1", "/file2") is False
    assert fs.get_file_size("/file2") is None

    # Se aumentar a capacidade, agora a cópia deve funcionar
    assert fs.update_capacity("u1", 500) == 0
    assert fs.copy_file("/file1", "/file2") is True
    assert fs.get_file_size("/file2") == 200


def test_update_capacity_tie_breaker_complex():
    fs = FileStorage()
    fs.add_user("u1", 1000)
    fs.add_file_by("u1", "/z_large", 400)
    fs.add_file_by("u1", "/c_mid", 200)
    fs.add_file_by("u1", "/a_mid", 200)
    fs.add_file_by("u1", "/b_mid", 200)

    # Total = 1000. Reduz para 350.
    # 1º a remover: maior tamanho -> /z_large (400). Sobram /a_mid (200), /b_mid (200), /c_mid (200) = 600.
    # Ainda 600 > 350.
    # 2º a remover (empate de 200): menor nome lexicográfico -> /a_mid. Sobram /b_mid, /c_mid = 400.
    # Ainda 400 > 350.
    # 3º a remover (empate de 200): menor nome lexicográfico -> /b_mid. Sobra /c_mid = 200 (<= 350).
    # Total removidos = 3.
    assert fs.update_capacity("u1", 350) == 3
    assert fs.get_file_size("/z_large") is None
    assert fs.get_file_size("/a_mid") is None
    assert fs.get_file_size("/b_mid") is None
    assert fs.get_file_size("/c_mid") == 200


def test_update_capacity_no_removal_needed():
    fs = FileStorage()
    fs.add_user("u1", 500)
    fs.add_file_by("u1", "/a", 100)
    # Aumentar ou manter capacidade retorna 0
    assert fs.update_capacity("u1", 600) == 0
    assert fs.update_capacity("u1", 200) == 0
    assert fs.get_file_size("/a") == 100
