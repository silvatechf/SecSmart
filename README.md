# SecSmarts: Enterprise Secret \& Remediation Sandbox


SecSmart is an advanced simulation laboratory and defensive CI/CD tool designed to detect, predict, and automatically remediate exposed secrets, hardcoded credentials, and infrastructure misconfigurations before they reach production.

![output terminal](assets/img2.png)

##  Architecture



Built on Clean Architecture (Modular Monolith), the project strictly separates concerns:

- Domain: Immutable data models (Pydantic v2) and ABC interfaces.

- Engines: CPU/IO optimized scanning (SAST/Shannon Entropy) and AST/Regex code mutators.

- Infrastructure: Adapters simulating HashiCorp Vault / AWS Secrets Manager.



##  Execution Modes

![output terminal](assets/img1.png)

### 1. Pre-Commit Hook (Shift-Left Security)

Intercepts developers' commits, removes hardcoded secrets, and safely injects Vault references on the fly.





