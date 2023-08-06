import os
import hashlib


def _hashfile(filepath):
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.hexdigest()


def _equal_hash(file1, file2):
    return _hashfile(file1) == _hashfile(file2)


def assert_not_equal_hash(path_to_file1, path_to_file2):
    assert os.path.isfile(path_to_file1), "%s not found" % path_to_file1
    assert os.path.isfile(path_to_file2), "%s not found" % path_to_file2
    assert not _equal_hash(path_to_file1, path_to_file2), "Ups, %s and %s files are equal" % (path_to_file1,
                                                                                              path_to_file2)
