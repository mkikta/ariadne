from processing import utils

def test_process_document():
    filename = "tests/data/layout-parser-paper-fast.pdf"
    with open(filename, "rb") as f:
        file_bytes = f.read()

        document, chunks = utils.process_document(
            filename,
            file_bytes,
        )

    assert document.startswith("## LayoutParser : A Unified Toolkit for Deep Learning Based Document Image Analysis")
    assert len(chunks) > 0
