import os

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".pyc"):
            file_path = os.path.join(root, file)
            os.remove(file_path)
            print(f"Archivo eliminado: {file_path}")
    # for dir in dirs:
    #     if dir == "__pycache__":
    #         dir_path = os.path.join(root, dir)
    #         os.rmdir(dir_path)
    #         print(f"Directorio eliminado: {dir_path}")