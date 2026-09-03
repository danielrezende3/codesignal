from mock2.solution import FileStorage


def test_compression_and_decompression_basic():
    fs = FileStorage()
    assert fs.add_user("u1", 1000) is True
    assert fs.add_file_by("u1", "/movie", 600) == 400

    assert fs.compress_file("u1", "/movie") == 700
    assert fs.get_file_size("/movie") is None
    assert fs.get_file_size("/movie.COMPRESSED") == 300

    assert fs.decompress_file("u1", "/movie.COMPRESSED") == 400
    assert fs.get_file_size("/movie") == 600
    assert fs.get_file_size("/movie.COMPRESSED") is None


def test_compress_odd_size_integer_division():
    fs = FileStorage()
    fs.add_user("u1", 500)
    fs.add_file_by(
        "u1", "/odd", 101
    )  # 101 // 2 = 50. Quota usada passa de 101 para 50.

    # 500 - 50 = 450 restante
    assert fs.compress_file("u1", "/odd") == 450
    assert fs.get_file_size("/odd.COMPRESSED") == 50

    # Descompactar: 50 * 2 = 100. Quota usada passa para 100. Restante 400.
    assert fs.decompress_file("u1", "/odd.COMPRESSED") == 400
    assert fs.get_file_size("/odd") == 100


def test_compress_invalid_cases():
    fs = FileStorage()
    fs.add_user("u1", 1000)
    fs.add_user("u2", 1000)
    fs.add_file_by("u1", "/file1", 200)

    # Wrong user
    assert fs.compress_file("u2", "/file1") is None
    # File doesn't exist
    assert fs.compress_file("u1", "/missing") is None

    # Compress successfully
    assert fs.compress_file("u1", "/file1") == 900

    # Cannot compress already compressed file
    assert fs.compress_file("u1", "/file1.COMPRESSED") is None


def test_compress_target_already_exists():
    fs = FileStorage()
    fs.add_user("u1", 1000)
    fs.add_file_by("u1", "/file1", 200)
    fs.add_file_by("u1", "/file1.COMPRESSED", 100)

    # Tentativa de compactar /file1 quando /file1.COMPRESSED já existe deve falhar
    assert fs.compress_file("u1", "/file1") is None
    assert fs.get_file_size("/file1") == 200


def test_decompress_exceeds_quota():
    fs = FileStorage()
    fs.add_user("u1", 500)
    fs.add_file_by("u1", "/f1", 400)
    fs.compress_file("u1", "/f1")  # /f1.COMPRESSED tem 200, sobra 300
    fs.add_file_by("u1", "/f2", 200)  # sobra 100

    # Para descompactar /f1.COMPRESSED, precisa de mais 200 (tamanho vira 400).
    # Como só restam 100 de quota, deve falhar (retornar None).
    assert fs.decompress_file("u1", "/f1.COMPRESSED") is None
    assert fs.get_file_size("/f1.COMPRESSED") == 200


def test_decompress_target_already_occupied():
    fs = FileStorage()
    fs.add_user("u1", 1000)
    fs.add_file_by("u1", "/doc", 200)
    fs.compress_file("u1", "/doc")  # vira /doc.COMPRESSED

    # Cria um novo arquivo /doc enquanto /doc.COMPRESSED existe
    fs.add_file_by("u1", "/doc", 100)

    # Descompactar /doc.COMPRESSED não pode sobrescrever /doc existente
    assert fs.decompress_file("u1", "/doc.COMPRESSED") is None
    assert fs.get_file_size("/doc.COMPRESSED") == 100


def test_decompress_not_ending_in_compressed():
    fs = FileStorage()
    fs.add_user("u1", 1000)
    fs.add_file_by("u1", "/normal.txt", 100)
    assert fs.decompress_file("u1", "/normal.txt") is None
