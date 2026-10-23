"""
OrderStream Developer Suite - Monetization & Wallet Integration
Direct 0-fee Web3 settlement & Polar.sh enterprise tier validation.
"""

import os
from typing import Dict, Any, Optional

STELLAR_WALLET = "GABFQIK63R2NETJM7T673EAMZN4RJLLGP3OFUEJU5ZVTGWUKULZJNL6"
STELLAR_MEMO = "400566831"
EVM_WALLET = "0x5de2b62434754bfd39ef350a3a867ed3eced5074"
POLAR_URL = "https://polar.sh/orderstream"

class LicenseManager:
    @staticmethod
    def get_tier(license_key: Optional[str] = None) -> Dict[str, Any]:
        key = license_key or os.environ.get("ORDERSTREAM_LICENSE_KEY", "").strip()
        if not key:
            return {
                "tier": "community",
                "name": "Community Open-Source Edition",
                "features": ["copyleft_header_scan", "ast_fingerprint_check"],
                "is_commercial": False,
            }
        
        if key.startswith("ord_ent_"):
            return {
                "tier": "enterprise",
                "name": "Enterprise Legal IP Compliance SLA",
                "features": ["copyleft_header_scan", "ast_fingerprint_check", "github_global_ast_index", "audit_due_diligence_report", "priority_support"],
                "is_commercial": True,
            }
        elif key.startswith("ord_pro_"):
            return {
                "tier": "pro",
                "name": "Pro Developer Tier",
                "features": ["copyleft_header_scan", "ast_fingerprint_check", "audit_due_diligence_report"],
                "is_commercial": True,
            }
        else:
            return {
                "tier": "invalid",
                "name": "Unrecognized License Key",
                "features": ["copyleft_header_scan"],
                "is_commercial": False,
            }

    @staticmethod
    def get_banner(tool_name: str) -> str:
        return f"""
================================================================================
  {tool_name.upper()} | OrderStream Developer Suite
  Polar: {POLAR_URL}
  Web3 Wallets (0% Fee Direct Settlement):
    - Stellar USDC/XLM : {STELLAR_WALLET} (Memo: {STELLAR_MEMO})
    - Base / EVM USDC  : {EVM_WALLET}
================================================================================
"""

    @staticmethod
    def get_remediation_footer() -> str:
        return (
            f"\n💡 Need automated M&A legal IP audit reports or GitHub global AST indexing?\n"
            f"   Subscribe on Polar: {POLAR_URL}\n"
            f"   Or fund directly with 0 platform fees:\n"
            f"   - Stellar (USDC/XLM): {STELLAR_WALLET} (Memo: {STELLAR_MEMO})\n"
            f"   - EVM (Base USDC):    {EVM_WALLET}\n"
        )
