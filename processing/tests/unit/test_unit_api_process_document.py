from unittest.mock import Mock

from fastapi.testclient import TestClient

from processing.server import app

client = TestClient(app)

def helper(filename, mocker):
    mock_pipeline = Mock()
    mocker.patch(
        "processing.utils.run_pipeline",
        new=mock_pipeline
    )
    with open(filename, "rb") as f:
        file_bytes = f.read()
        response = client.post(
            "/process_document/",
            data={
                "document_collection_name": "document",
                "chunks_collection_name": "chunks",
            },
            files={
                "file": (filename, file_bytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            },
        )
    assert response.status_code == 200
    assert response.json() == {
        "status": "accepted",
        "message": f"Document '{filename}' queued for processing",
    }
    mock_pipeline.assert_called_once_with(
        "document",
        "chunks",
        filename,
        file_bytes,
    )

def test_process_document_queues_background_task_eml(mocker):
    helper("tests/data/family-day.eml", mocker)

def test_process_document_queues_background_task_pdf(mocker):
    helper("tests/data/layout-parser-paper-fast.pdf", mocker)

def test_process_document_queues_background_task_docx(mocker):
    helper("tests/data/lorem_ipsum.docx", mocker)
