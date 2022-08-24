import zipfile


class FileHandler:
    def __init__(self) -> None:
        pass

    @staticmethod
    def read_file(path, read_mode='w'):
        if path:
            with open(path, mode=read_mode) as f:
                content = f.read()
                f.close()
                return content
        return None

    @staticmethod
    def save_file(path, save_mode, file_object):
        with open(path, save_mode) as f:
            f.write(file_object)

    @staticmethod
    def unzip_file(file_path, target_dir, read_mode='r'):
        with zipfile.ZipFile(file_path, read_mode) as zip_ref:
            zip_ref.extractall(target_dir)
