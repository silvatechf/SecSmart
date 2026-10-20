import pytest
from src.engines.sast_scanner import SASTScanner

@pytest.mark.asyncio
async def test_scanner_instantiation():
    scanner = SASTScanner()
    assert scanner is not None
