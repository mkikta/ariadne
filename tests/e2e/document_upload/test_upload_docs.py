from pathlib import Path
import requests
import mimetypes


ENDPOINT="http://localhost:3000/process_document/"

def upload_file(path: Path):
    with open(path, "rb") as file:
        mime_type, _ = mimetypes.guess_type(path) or (None, None)
        response = requests.post(
            ENDPOINT,
            files={"file": (path.name, file, mime_type)},
            data={"document_collection_name": "document", "chunks_collection_name": "chunks",}
        )
        return response

def test_upload_word():
    response = upload_file(Path("e2e/data/lorem_ipsum.docx"))
    assert response.status_code == 200

def test_upload_pdf():
    response = upload_file(Path("e2e/data/layout-parser-paper-fast.pdf"))
    assert response.status_code == 200

def test_upload_eml():
    response = upload_file(Path("e2e/data/family-day.eml"))
    assert response.status_code == 200
