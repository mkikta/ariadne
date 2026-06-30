"""Script to upload documents to ariadne database."""

import argparse
from pathlib import Path
import requests
import mimetypes

ENDPOINT="http://localhost:3100/process_document/"

def upload_file(path: Path):
    with open(path, "rb") as file:
        mime_type, _ = mimetypes.guess_type(path) or (None, None)
        response = requests.post(
            ENDPOINT,
            files={"file": (path.name, file, mime_type)},
            data={"document_collection_name": "document", "chunks_collection_name": "chunks",}
        )
        if response.status_code != 200:
            print(response.status_code)
            print(f"Error uploading {path}. It has been skipped.")

def upload_dir(path: Path):
    for item in path.iterdir():
        if item.is_file():
            upload_file(item)
        elif item.is_dir():
            upload_dir(item)

def main(paths: list[str]):
    for path in paths:
        path = Path(path)
        if path.is_file():
            upload_file(path)
        elif path.is_dir():
            upload_dir(path)
        else:
            print(f"Path {path} does not exist.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Helper script to upload documents to Ariadne database.")
    parser.add_argument("-p", "--paths", nargs="+", required=True, type=str, help="Space separated list of folders and/or files to upload.")
    args = parser.parse_args()

    main(args.paths)
