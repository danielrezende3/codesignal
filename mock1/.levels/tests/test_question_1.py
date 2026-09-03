from mock1.solution import FileStorage


def test_add_and_get_file_size():
    fs = FileStorage()
    assert fs.add_file("/a.txt", 100) is True
    assert fs.add_file("/a.txt", 200) is False  # Duplicate name
    assert fs.get_file_size("/a.txt") == 100
    assert fs.get_file_size("/missing.txt") is None


def test_add_file_with_zero_size():
    fs = FileStorage()
    assert fs.add_file("/empty.txt", 0) is True
    assert fs.get_file_size("/empty.txt") == 0
    assert fs.add_file("/empty.txt", 0) is False


def test_copy_file_basic():
    fs = FileStorage()
    assert fs.add_file("/a.txt", 100) is True
    assert fs.copy_file("/a.txt", "/b.txt") is True
    assert fs.get_file_size("/b.txt") == 100
    assert fs.copy_file("/missing", "/c.txt") is False
    assert fs.copy_file("/a.txt", "/b.txt") is False  # Destination already exists


def test_copy_file_to_self():
    fs = FileStorage()
    fs.add_file("/a.txt", 100)
    # Copying a file to its own name should fail because destination already exists
    assert fs.copy_file("/a.txt", "/a.txt") is False
    assert fs.get_file_size("/a.txt") == 100


def test_multiple_files_and_copies_independence():
    fs = FileStorage()
    assert fs.add_file("/dir/file1.txt", 50) is True
    assert fs.add_file("/dir/file2.txt", 150) is True
    assert fs.copy_file("/dir/file1.txt", "/dir/file3.txt") is True
    assert fs.get_file_size("/dir/file3.txt") == 50
    assert fs.get_file_size("/dir/file1.txt") == 50
    assert fs.get_file_size("/dir/file2.txt") == 150
    # Copying a copied file
    assert fs.copy_file("/dir/file3.txt", "/dir/file4.txt") is True
    assert fs.get_file_size("/dir/file4.txt") == 50
