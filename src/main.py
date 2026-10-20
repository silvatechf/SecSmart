import sys
import argparse
import asyncio
import os
import re
from rich.console import Console
from src.engines.remediation import RemediationEngine
from src.infrastructure.vault_mock import VaultMock
from src.domain.entities import Vulnerability, SecretToken

async def hook_mode(files):
    console = Console()
    vault = VaultMock()
    remediator = RemediationEngine(vault)
    threats_found = False
    
    patterns = {
        "AWS_ACCESS_KEY": r"(AKIA[0-9A-Z]{16})",
        "GCP_API_KEY": r"(AIza[0-9A-Za-z\-_]{35})"
    }
    
    for file_path in files:
        if not os.path.exists(file_path): 
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines):
            for sec_type, pattern in patterns.items():
                match = re.search(pattern, line)
                if match:
                    threats_found = True
                    token = SecretToken(raw_value=match.group(1), entropy_score=5.5, secret_type=sec_type)
                    vuln = Vulnerability(file_path=file_path, line_number=i+1, token=token, context_snippet=line.strip())
                    
                    console.print(f"[bold red][!] THREAT INTERCEPTED:[/bold red] {sec_type} in {file_path}")
                    # Auto-Remediation at commit time
                    await remediator.apply_remediation(vuln)
                    console.print(f"[bold green][✔] AUTO-REMEDIATION APPLIED:[/bold green] Code successfully mutated.")
                    
    if threats_found:
        console.print("[bold yellow][!] Commit preemptively blocked.[/bold yellow]")
        console.print("[bold cyan]Quick Review: Run 'git diff', validate the Vault injection, and run 'git add .' followed by 'git commit' again.[/bold cyan]")
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args()
    
    if args.filenames:
        asyncio.run(hook_mode(args.filenames))
    else:
        print("Usage for CI/CD Hook: python -m src.main <filename>")
