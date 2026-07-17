import pytest
from unittest.mock import AsyncMock
from processing import utils


@pytest.mark.asyncio
async def test_run_pipeline_success(mocker):
    pipeline = AsyncMock()
    mocker.patch.object(utils, "_pipeline", pipeline)

    logger = mocker.patch.object(utils, "logger")

    await utils.run_pipeline(
        document_collection_name="documents",
        chunks_collection_name="chunks",
        filename="test.pdf",
        file_bytes=b"contents",
    )

    pipeline.assert_awaited_once_with(
        "documents",
        "chunks",
        "test.pdf",
        b"contents",
    )

    logger.info.assert_called_once_with(
        "Processed %s successfully",
        "test.pdf",
    )
    logger.error.assert_not_called()


@pytest.mark.asyncio
async def test_run_pipeline_failure(mocker):
    err = RuntimeError("error")
    pipeline = AsyncMock(side_effect=err)
    mocker.patch.object(utils, "_pipeline", pipeline)

    logger = mocker.patch.object(utils, "logger")

    # Should not raise
    await utils.run_pipeline(
        document_collection_name="documents",
        chunks_collection_name="chunks",
        filename="test.pdf",
        file_bytes=b"contents",
    )

    pipeline.assert_awaited_once()

    logger.info.assert_not_called()
    logger.error.assert_called_once_with(
        "Failed to process %s: %s",
        "test.pdf",
        err,
    )