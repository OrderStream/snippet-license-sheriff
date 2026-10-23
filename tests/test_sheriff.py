"""
Unit and integration tests for snippet-license-sheriff.
"""

import pytest
from pathlib import Path
from snippet_license_sheriff.core import SnippetLicenseSheriff, ASTFingerprinter
from snippet_license_sheriff.monetization import LicenseManager
from snippet_license_sheriff.cli import main

def test_license_manager():
    comm = LicenseManager.get_tier(None)
    assert comm["tier"] == "community"

    ent = LicenseManager.get_tier("ord_ent_legal_sheriff")
    assert ent["tier"] == "enterprise"

    banner = LicenseManager.get_banner("snippet-license-sheriff")
    assert "GABFQIK63R2NETJM7T673EAMZN4RJLLGP3OFUEJU5ZVTGWUKULZJNL6" in banner

def test_ast_fingerprinter_normalizes():
    c1 = """
def calculate_hash(data):
    # comment
    result = 0
    for x in data:
        result += ord(x)
    return result
"""
    c2 = """
def compute_sum(input_buffer):
    // another comment
    total = 0
    for item in input_buffer:
        total += ord(item)
    return total
"""
    # Renaming variables should produce identical normalized AST fingerprint
    fp1 = ASTFingerprinter.normalize_and_fingerprint(c1)
    fp2 = ASTFingerprinter.normalize_and_fingerprint(c2)
    assert fp1 == fp2

def test_viral_header_detection(tmp_path):
    viral_code = """/*
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License.
 */

function add(a, b) { return a + b; }
"""
    f = tmp_path / "contaminated.js"
    f.write_text(viral_code, encoding="utf-8")

    violations = SnippetLicenseSheriff.scan_file(str(f), viral_code, {"MIT", "Apache-2.0"})
    assert len(violations) >= 1
    assert violations[0].detected_license == "GPL"
    assert violations[0].severity == "CRITICAL"

def test_permissive_code_clean_pass(tmp_path):
    clean_code = """
# MIT License
# Copyright (c) 2026 OrderStream
def multiply(a, b):
    return a * b
"""
    f = tmp_path / "clean.py"
    f.write_text(clean_code, encoding="utf-8")

    violations = SnippetLicenseSheriff.scan_file(str(f), clean_code, {"MIT", "Apache-2.0"})
    assert len(violations) == 0

def test_cli_execution(tmp_path):
    f = tmp_path / "ok.py"
    f.write_text("def ping(): return 'pong'\n", encoding="utf-8")

    exit_clean = main(["scan", "--path", str(tmp_path)])
    assert exit_clean == 0

    exit_lic = main(["license"])
    assert exit_lic == 0
