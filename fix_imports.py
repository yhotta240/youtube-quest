import os
import shutil

def fix_imports_in_file(file_path):
    try:
        tmp_file_path = file_path + ".tmp"
        shutil.copyfile(file_path, tmp_file_path)
        with open(tmp_file_path, 'r', encoding="utf-8") as infile, open(file_path, 'w', encoding="utf-8") as outfile:
            for line in infile:
                line = line.replace("from .route import app", "from route import app")
                line = line.replace("from .youtube_api", "from youtube_api")
                line = line.replace("from .download_csv", "from download_csv")
                outfile.write(line)
        os.remove(tmp_file_path)  # Remove temporary file
        print(f"Imports in {file_path} fixed successfully.")
    except Exception as e:
        print(f"Error occurred while fixing imports in {file_path}: {e}")

if __name__ == "__main__":
    fix_imports_in_file("api/route.py")
    fix_imports_in_file("api/run.py")
