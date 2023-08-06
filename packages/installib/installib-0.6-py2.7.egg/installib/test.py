import os

from installib.obfuscation_checker import assert_not_equal_hash
from installib.compare import compare_versions_str
from installib.windows import get_file_properties


WINDOWS_ASSEMBLY_GAC_MSIL_PATH = "C:\Windows\\assembly\GAC_MSIL\\"
WINDOWS_DOTNET_ASSEMBLY_GAC_MSIL_PATH = "C:\Windows\Microsoft.Net\\assembly\GAC_MSIL\\"


def is_file_in_subdirectory(filename, dirname):
    for _, directories, _ in os.walk(dirname):
        for directory in directories:
            subdir = os.path.join(dirname, directory)
            if os.path.isfile(os.path.join(subdir, filename)):
                return True
    return False


def assert_source_files_are_installed_and_obfuscated(install_path, source_files,
                                                     source_files_without_obfuscate_path=None):
    """
    Assert that source_files are installed in install_path and selected source files are obfuscated.
    :param install_path:
    :param source_files: list of tuples (file_path, operator, version_to_compare, check_obfuscation)
        For example:
            [("es\resource.dll", ">=", "1.3.0.0", False), ("core.dll", "", "", False)]
    :param source_files_without_obfuscate_path: (optional) needed to compare obfuscated source files
    """
    assert os.path.isdir(install_path), "%s does not exist" % install_path
    for source_file, op, version, check_obfuscation in source_files:
        file_path = os.path.join(install_path, source_file)
        assert os.path.isfile(file_path), "%s file not found in %s" % (source_file, install_path)
        properties = get_file_properties(file_path)
        product_version = properties["StringFileInfo"].get('ProductVersion', None) if properties["StringFileInfo"] is not None else None
        assert compare_versions_str(product_version, op, version, default=True), \
            "%s ProductVersion %s is not %s %s" % (file_path, product_version, op, version)
        if check_obfuscation:
            assert_not_equal_hash(file_path, source_files_without_obfuscate_path + source_file)


def assert_assembly_files_are_installed(assembly_source_files, microsoft_assembly_source_files):
    """
    Assert that files are installed in GAC_MSIL.
    :param assembly_source_files: list of file names.
    :param microsoft_assembly_source_files: list of file names.
    """
    for assembly_file in assembly_source_files:
        assert is_file_in_subdirectory("%s.dll"% assembly_file, WINDOWS_ASSEMBLY_GAC_MSIL_PATH + assembly_file), \
            "%s file not found in directory %s" % (assembly_file, WINDOWS_ASSEMBLY_GAC_MSIL_PATH)

    for assembly_file in microsoft_assembly_source_files:
        assert is_file_in_subdirectory("%s.dll" % assembly_file, WINDOWS_DOTNET_ASSEMBLY_GAC_MSIL_PATH + assembly_file), \
            "%s file not found in directory %s" % (assembly_file, WINDOWS_DOTNET_ASSEMBLY_GAC_MSIL_PATH)
