"""
Structural AST code fingerprinting engine checking against viral GPL/AGPL copy-pasted license contamination in proprietary repos.
"""

import ast
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Set, Optional, Tuple

VIRAL_COPYLEFT_PATTERNS = [
    (r"\bGNU\s+General\s+Public\s+License\b", "GPL"),
    (r"\bGNU\s+Affero\s+General\s+Public\s+License\b", "AGPL"),
    (r"\bAffero\s+GPL\b", "AGPL"),
    (r"\bAGPL-3\.0\b", "AGPL-3.0"),
    (r"\bGPL-3\.0\b", "GPL-3.0"),
    (r"\bGPL-2\.0\b", "GPL-2.0"),
    (r"\bServer\s+Side\s+Public\s+License\b", "SSPL"),
    (r"\bGNU\s+Lesser\s+General\s+Public\s+License\b", "LGPL"),
]

# Signatures of famous copyleft algorithms often copy-pasted
COPYLEFT_AST_SIGNATURES = {
    # Token hash of Linux kernel red-black tree or GPL fast inverse sqrt
    "gpl_crc32_fast": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069"
}

@dataclass
class LicenseContamination:
    file_path: str
    line: int
    detected_license: str
    severity: str  # CRITICAL, HIGH
    violation_type: str  # VIRAL_HEADER, STRUCTURAL_AST_MATCH
    snippet_preview: str
    remediation: str

class ASTFingerprinter:
    RESERVED_KEYWORDS = {
        "def", "class", "return", "if", "elif", "else", "for", "while", "try",
        "except", "finally", "with", "as", "import", "from", "function", "const",
        "let", "var", "async", "await", "yield", "raise", "throw", "catch",
        "break", "continue", "pass", "None", "True", "False", "true", "false",
        "null", "undefined", "new", "switch", "case", "default", "in", "is", "not"
    }

    @classmethod
    def normalize_and_fingerprint(cls, code: str) -> str:
        """
        Strips comments, docstrings, normalizes variable names to canonical tokens, and computes SHA-256 fingerprint.
        """
        # Remove comments and docstrings
        clean = re.sub(r'"""[\s\S]*?"""', "", code)
        clean = re.sub(r"'''[\s\S]*?'''", "", clean)
        clean = re.sub(r"#.*", "", clean)
        clean = re.sub(r"//.*", "", clean)
        clean = re.sub(r"/\*.*?\*/", "", clean, flags=re.DOTALL)

        # Normalize whitespace and identifiers
        tokens = re.findall(r"[a-zA-Z0-9_]+|[^\s\w]", clean)
        var_map: Dict[str, str] = {}
        normalized_tokens: List[str] = []

        for t in tokens:
            if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", t):
                if t not in cls.RESERVED_KEYWORDS:
                    if t not in var_map:
                        var_map[t] = f"v_{len(var_map)}"
                    normalized_tokens.append(var_map[t])
                else:
                    normalized_tokens.append(t)
            else:
                normalized_tokens.append(t)

        canonical_repr = "".join(normalized_tokens)
        return hashlib.sha256(canonical_repr.encode("utf-8")).hexdigest()

class SnippetLicenseSheriff:
    @staticmethod
    def scan_file(file_path: str, content: str, allowed_licenses: Set[str]) -> List[LicenseContamination]:
        violations: List[LicenseContamination] = []
        lines = content.splitlines()

        # 1. Header / text scan for viral copyleft keywords
        for idx, line in enumerate(lines, 1):
            for pat, lic_name in VIRAL_COPYLEFT_PATTERNS:
                if re.search(pat, line, re.IGNORECASE):
                    if lic_name not in allowed_licenses:
                        violations.append(LicenseContamination(
                            file_path=file_path,
                            line=idx,
                            detected_license=lic_name,
                            severity="CRITICAL",
                            violation_type="VIRAL_HEADER",
                            snippet_preview=line.strip()[:100],
                            remediation=f"Viral copyleft header detected ('{lic_name}'). Must be removed or rewritten under permissive terms to avoid repository contamination."
                        ))

        # 2. Structural AST fingerprint scan
        fp = ASTFingerprinter.normalize_and_fingerprint(content)
        for sig_name, sig_hash in COPYLEFT_AST_SIGNATURES.items():
            if fp == sig_hash:
                violations.append(LicenseContamination(
                    file_path=file_path,
                    line=1,
                    detected_license="GPL-2.0",
                    severity="CRITICAL",
                    violation_type="STRUCTURAL_AST_MATCH",
                    snippet_preview=f"Matches known GPL algorithm signature '{sig_name}'",
                    remediation=f"Code matches GPL structural fingerprint '{sig_name}'. Replace with independent clean-room implementation."
                ))

        return violations

    @classmethod
    def scan_directory(cls, directory: str, allowed: Optional[List[str]] = None) -> List[LicenseContamination]:
        allowed_set = set(allowed or ["MIT", "Apache-2.0", "BSD-3-Clause", "BSD-2-Clause", "ISC", "Unlicense"])
        violations: List[LicenseContamination] = []
        dir_path = Path(directory)

        for file in dir_path.rglob("*"):
            if not file.is_file():
                continue
            parts = file.parts
            if any(p.startswith(".") or p in {"node_modules", "venv", ".git", "__pycache__", "dist", "build"} for p in parts):
                continue
            if file.suffix in {".py", ".ts", ".js", ".go", ".rs", ".java", ".c", ".cpp", ".h"}:
                try:
                    content = file.read_text(encoding="utf-8", errors="ignore")
                    violations.extend(cls.scan_file(str(file), content, allowed_set))
                except Exception:
                    continue

        return violations

    @staticmethod
    def generate_markdown(violations: List[LicenseContamination]) -> str:
        if not violations:
            return (
                "### ✅ Snippet License Sheriff: Clean Pass\n\n"
                "No viral GPL/AGPL/SSPL code copy-paste contamination detected."
            )

        md = [
            "### 🚨 Viral License Contamination Detected",
            "",
            "| Severity | License | Violation Type | Location | Snippet / Risk | Action Required |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |"
        ]
        for v in violations:
            md.append(f"| `{v.severity}` | **{v.detected_license}** | `{v.violation_type}` | `{v.file_path}:{v.line}` | `{v.snippet_preview}` | {v.remediation} |")

        md.append("")
        md.append("---")
        md.append("> **Proprietary IP Compliance by OrderStream**")
        return "\n".join(md)
