from mock1.solution import FileStorage


def test_find_files_basic():
    fs = FileStorage()
    fs.add_file("/docs/a.txt", 100)
    fs.add_file("/docs/b.txt", 300)
    fs.add_file("/docs/c.pdf", 500)
    fs.add_file("/docs/d.txt", 300)
    fs.add_file("/images/a.txt", 900)

    assert fs.find_files("/docs", ".txt") == [
        "/docs/b.txt(300)",
        "/docs/d.txt(300)",
        "/docs/a.txt(100)",
    ]
    assert fs.find_files("/nothing", ".txt") == []


def test_find_files_empty_prefix_or_suffix():
    fs = FileStorage()
    fs.add_file("/docs/a.txt", 100)
    fs.add_file("/docs/b.txt", 300)
    fs.add_file("/photos/c.png", 200)

    # Empty prefix matches all ending with suffix
    assert fs.find_files("", ".png") == ["/photos/c.png(200)"]
    # Empty suffix matches all starting with prefix
    assert fs.find_files("/photos", "") == ["/photos/c.png(200)"]
    # Both empty matches all files in the system, sorted by size desc then name asc
    assert fs.find_files("", "") == [
        "/docs/b.txt(300)",
        "/photos/c.png(200)",
        "/docs/a.txt(100)",
    ]


def test_find_files_sorting_ties_and_alphabetical():
    fs = FileStorage()
    fs.add_file("/z.txt", 200)
    fs.add_file("/a.txt", 200)
    fs.add_file("/m.txt", 200)
    fs.add_file("/b.txt", 500)
    fs.add_file("/c.txt", 500)

    assert fs.find_files("/", ".txt") == [
        "/b.txt(500)",
        "/c.txt(500)",
        "/a.txt(200)",
        "/m.txt(200)",
        "/z.txt(200)",
    ]


def test_find_files_overlapping_prefix_suffix():
    fs = FileStorage()
    # File name is "aba"
    fs.add_file("aba", 50)
    fs.add_file("ababa", 100)
    fs.add_file("a", 10)

    # Starts with "ab" and ends with "ba"
    assert fs.find_files("ab", "ba") == [
        "ababa(100)",
        "aba(50)",
    ]
    # Exact full match
    assert fs.find_files("aba", "aba") == ["aba(50)"]
    # "a" starts with "a" and ends with "a"
    assert fs.find_files("a", "a") == [
        "ababa(100)",
        "aba(50)",
        "a(10)",
    ]


def test_find_files_empty_storage():
    fs = FileStorage()
    assert fs.find_files("any", "thing") == []
    assert fs.find_files("", "") == []
