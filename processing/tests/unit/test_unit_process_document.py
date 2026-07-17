from unittest.mock import Mock
from processing import utils

def test_process_document(mocker):
    fake_dl_doc = Mock()
    fake_dl_doc.export_to_markdown.return_value = "# My document"

    fake_result = Mock()
    fake_result.document = fake_dl_doc

    fake_converter = Mock()
    fake_converter.convert.return_value = fake_result

    mocker.patch.object(utils, "_converter", fake_converter)

    fake_chunk = object()

    fake_chunker = Mock()
    fake_chunker.chunk.return_value = [fake_chunk]
    fake_chunker.contextualize.return_value = "chunk 1"

    mocker.patch("processing.utils.HybridChunker", return_value=fake_chunker)

    filename = "tests/data/family-day.eml"
    with open(filename, "rb") as f:
        file_bytes = f.read()

        document, chunks = utils.process_document(
            filename,
            file_bytes,
        )

    assert document == "# My document"
    assert chunks == ["chunk 1"]

    fake_converter.convert.assert_called_once()
    fake_chunker.chunk.assert_called_once_with(dl_doc=fake_dl_doc)
    fake_chunker.contextualize.assert_called_once_with(chunk=fake_chunk)
