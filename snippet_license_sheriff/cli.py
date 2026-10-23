"""
Command line interface for snippet-license-sheriff.
"""

import argparse
import sys
from pathlib import Path
from snippet_license_sheriff.core import SnippetLicenseSheriff
from snippet_license_sheriff.monetization import LicenseManager

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="snippet-license-sheriff",
        description="Structural AST code fingerprinting engine checking against viral GPL/AGPL copy-pasted license contamination in proprietary repos"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # scan command
    scan_parser = subparsers.add_parser("scan", help="Scan codebase for viral copyleft contamination")
    scan_parser.add_argument("--path", default=".", help="Directory to scan")
    scan_parser.add_argument("--allowed", default="MIT,Apache-2.0,BSD-3-Clause,BSD-2-Clause,ISC", help="Comma-separated allowed licenses")
    scan_parser.add_argument("--fail-on-detected", action="store_true", default=True, help="Fail CI if contamination detected")
    scan_parser.add_argument("--license-key", default=None, help="OrderStream license key")

    # license / donate command
    subparsers.add_parser("license", help="View license tier and zero-fee crypto donation wallets")

    args = parser.parse_args(argv)

    if not args.command or args.command == "license":
        print(LicenseManager.get_banner("snippet-license-sheriff"))
        tier = LicenseManager.get_tier(getattr(args, "license_key", None))
        print(f"Active Tier: {tier['name']} ({tier['tier']})")
        print(f"Features: {', '.join(tier['features'])}")
        print(LicenseManager.get_remediation_footer())
        return 0

    if args.command == "scan":
        print(LicenseManager.get_banner("snippet-license-sheriff"))
        allowed_list = [lic.strip() for lic in args.allowed.split(",") if lic.strip()]
        violations = SnippetLicenseSheriff.scan_directory(args.path, allowed_list)

        print(f"[SNIPPET-LICENSE-SHERIFF] Scanned Path: {args.path}")
        print(f"[SNIPPET-LICENSE-SHERIFF] Allowed Licenses: {', '.join(allowed_list)}")
        print(f"[SNIPPET-LICENSE-SHERIFF] Viral Contaminations Detected: {len(violations)}")

        for v in violations:
            print(f"\n  🚨 [{v.severity}] {v.detected_license} ({v.violation_type}) in {v.file_path}:{v.line}")
            print(f"     Snippet: {v.snippet_preview}")
            print(f"     Action:  {v.remediation}")

        print(LicenseManager.get_remediation_footer())

        if args.fail_on_detected and len(violations) > 0:
            print("\n❌ [SNIPPET-LICENSE-SHERIFF] FAILED: Viral copyleft code contamination detected! Build blocked.")
            return 1

        print("\n✅ [SNIPPET-LICENSE-SHERIFF] PASSED: Clean proprietary IP compliance.")
        return 0

    return 0

if __name__ == "__main__":
    sys.exit(main())
