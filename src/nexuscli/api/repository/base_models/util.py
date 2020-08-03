import os


def get_files(src_dir, recurse=True):
    """
    Walks the given directory and collects files to be uploaded. If
    recurse option is False, only the files on the root of the directory
    will be returned.

    :param src_dir: location of files
    :param recurse: If false, only the files on the root of src_dir
                    are returned
    :return: file set to be used with upload_directory
    :rtype: set
    """
    source_files = set()
    for dirname, dirnames, filenames in os.walk(src_dir):
        if not recurse:
            del dirnames[:]

        source_files.update(
            os.path.relpath(os.path.join(dirname, f), src_dir)
            for f in filenames)

    return source_files
