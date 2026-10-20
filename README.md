
# SecSmarts: Enterprise Secret & Remediation Sandbox

SecAmarts is an advanced simulation laboratory and defensive CI/CD tool designed to detect, predict, and automatically remediate exposed secrets, hardcoded credentials, and infrastructure misconfigurations before they reach production.

![alt text](assets/img2.png)

##  Proof of Concept: Auto-Remediation in Action

SecLabs does not just alert; it actively mutates the AST/file context during the commit hook.

**Before (Vulnerable Developer Code):**
```python
def connect_to_cloud():
    AWS_KEY = "AKIAIOSFODNN7EXAMPLE"
    print("Authenticating...")

```

**After (SecSmarts On-the-Fly Remediation):**

```python
import os
def connect_to_cloud():
    AWS_KEY = os.getenv("SEC_AWS_ACCESS_KEY_29BBC1122986") 
    print("Authenticating...")

```

##  Core Architecture & Engines

Built on **Clean Architecture (Modular Monolith)**, the project strictly separates concerns using Python and Pydantic v2.

* **Detection Engine (Shannon Entropy + Regex):** Pure Regex generates false positives (e.g., matching random IDs). SecLabs calculates the geometric randomness (Shannon Entropy) of matched strings. Only strings crossing the `5.5` entropy threshold are classified as cryptographic keys.
* **Remediation Engine:** An IO-optimized mutator that isolates the raw secret in memory, stores it in the configured Adapter (Vault/AWS Secrets Manager), and rewrites the source file securely.
* **Shift-Left Integration:** Acts as a preemptive barrier at the `git commit` level, preventing the secret from ever entering the Git history.

##  Quick Start (Pre-Commit Hook)

To test the defensive barrier locally:

1. Map the hook in your repository:

```yaml
# .pre-commit-hooks.yaml
- id: seclabs-remediator
  name: SecLabs Auto-Remediation
  description: Detects and replaces hardcoded secrets with Vault refs.
  entry: python -m src.main
  language: python
  types: [python, javascript, typescript]
  pass_filenames: true

```

2. Simulate a vulnerable commit:

```bash
python -m src.main target_code/vulnerable_app.py

```

![alt text](assets/img1.png)

##  Security Posture

* Secrets are NEVER printed to stdout or logs.
* Simulated Vault isolates real values in memory.
* Code conforms strictly to PEP 8 and Python Type Hinting.

