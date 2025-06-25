import os
import tempfile
from apps.ocr.file_discovery import discover_contract_files

def test_discover_contract_files(tmp_path):
    # Create a nested directory structure with supported and unsupported files
    contract_dir = tmp_path / "contracts"
    contract_dir.mkdir()
    (contract_dir / "a.pdf").write_text("PDF content")
    (contract_dir / "b.docx").write_text("DOCX content")
    (contract_dir / "c.png").write_text("PNG content")
    (contract_dir / "d.jpeg").write_text("JPEG content")
    (contract_dir / "e.txt").write_text("Not supported")
    sub_dir = contract_dir / "sub"
    sub_dir.mkdir()
    (sub_dir / "f.pdf").write_text("PDF in subfolder")
    (sub_dir / "g.docx").write_text("DOCX in subfolder")
    # Run discovery
    found_files = discover_contract_files(str(contract_dir))
    found_basenames = {os.path.basename(f) for f in found_files}
    assert found_basenames == {"a.pdf", "b.docx", "c.png", "d.jpeg", "f.pdf", "g.docx"}
    # All returned paths should be absolute
    for f in found_files:
        assert os.path.isabs(f) 