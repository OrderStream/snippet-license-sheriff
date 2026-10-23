# snippet-license-sheriff 🤠📜

[![GitHub Action](https://img.shields.io/badge/GitHub%20Action-v1.0.0-orange?logo=githubactions)](https://github.com/OrderStream/snippet-license-sheriff)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://img.shields.io/badge/CI-Passing-brightgreen.svg)]()
[![OrderStream Polar](https://img.shields.io/badge/Polar-OrderStream-blue.svg)](https://polar.sh/orderstream)
[![Stellar XLM/USDC](https://img.shields.io/badge/Stellar-USDC%2FXLM-black.svg)](#direct-web3-wallet-monetization)
[![Base USDC](https://img.shields.io/badge/Base-USDC-0052FF.svg)](#direct-web3-wallet-monetization)

Structural AST code fingerprinting engine checking against viral GPL/AGPL copy-pasted license contamination in proprietary repos.

---

## 💥 The Friction & Dollar Cost
Viral copyleft contamination (GPL-2.0, GPL-3.0, AGPL-3.0, SSPL) can destroy commercial enterprises during M&A due diligence or IPO audits:
- A developer copy-pastes a snippet from StackOverflow or a GPL GitHub repo into a closed-source proprietary codebase.
- The viral copyleft terms technically compel the entire proprietary application to be licensed under open-source terms.
- Remediation during acquisition audits costs hundreds of thousands of dollars in emergency legal and engineering refactoring.

**snippet-license-sheriff** continuously protects your codebase in CI:
1. Performs structural AST normalization and canonical token hashing, detecting copy-pastes even if variable names were renamed.
2. Scans files and headers for viral copyleft preambles.
3. Enforces an allowed license whitelist (`MIT`, `Apache-2.0`, `BSD-3-Clause`) across all code contributions.

---

## 🚀 Quick Start

### Installation
```bash
pip install snippet-license-sheriff
```

### CLI Usage
```bash
# Scan repository for viral copyleft contamination
snippet-license-sheriff scan --path ./src

# Whitelist specific permissive licenses
snippet-license-sheriff scan --path ./src --allowed "MIT,Apache-2.0,BSD-3-Clause"

# Check license & zero-fee wallet payment details
snippet-license-sheriff license
```

---

## 🤖 GitHub Action Integration

```yaml
- name: Snippet License Sheriff
  uses: OrderStream/snippet-license-sheriff@v1
  with:
    path: "."
    allowed: "MIT,Apache-2.0,BSD-3-Clause"
    fail_on_detected: true
```

---

---

## 💳 Enterprise Pricing Matrix & Licensing

| Tier | Price | Repositories | Core Capabilities |
| :--- | :--- | :--- | :--- |
| **Community Free** | **** | Unlimited | Standalone CLI runner and single-repo GitHub Action |
| **Starter Suite** | ** / mo** | Up to 10 Repos | Automated CI PR gates, 500 CI runs/mo, standard email support |
| **Team Platform** | **,499 / mo** | Up to 50 Repos | Full 10-tool OrderStream suite, flaky test quarantine deterministic replay, zero-downtime shadow DB migration guard, 24/7 telemetry alarms |
| **Enterprise Platform** | **,999 / mo** | Unlimited | Multi-repo speculative merge engine, zero-downtime migration orchestrator, WASM sandbox gate, dedicated 24/7 cloud keeper, custom SLA |
| **M&A IP & Security Audit** | **,000 one-time** | Whole Organization | Comprehensive copyleft AST fuzzy fingerprint audit, snippet license sheriff certification, formal invariant verification, and executive forensic IP Cleanliness Certificate |

## 💰 Direct Web3 Wallet Monetization & Polar Integration

Support this project or purchase enterprise M&A due diligence compliance reports with **0 platform fees**:

- **Polar Subscription & Sponsorship:** [https://polar.sh/orderstream](https://polar.sh/orderstream)
- **Stellar Network (Native XLM / USDC):**
  - Public Key: `GABFQIK63R2NETJM7T673EAMZN4RJLLGP3OFUEJU5ZVTGWUKULZJNL6`
  - Memo (Required): `400566831`
- **EVM (Base / Arbitrum / Ethereum USDT & USDC):**
  - Address: `0x5de2b62434754bfd39ef350a3a867ed3eced5074`
