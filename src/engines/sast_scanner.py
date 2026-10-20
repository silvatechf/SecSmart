import os
import re
from src.domain.entities import Vulnerability, SecretToken, Severity

SECRET_PATTERNS = {
    "AWS_ACCESS_KEY": r"(AKIA[0-9A-Z]{16})",
    "GCP_API_KEY": r"(AIza[0-9A-Za-z\-_]{35})"
}

class SASTScanner:
    async def scan(self, directory: str):
        vulns = []
        if not os.path.exists(directory): return vulns
            
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    path = os.path.join(root, file)
                    with open(path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            for sec_type, pattern in SECRET_PATTERNS.items():
                                match = re.search(pattern, line)
                                if match:
                                    token = SecretToken(raw_value=match.group(1), entropy_score=5.5, secret_type=sec_type)
                                    vulns.append(Vulnerability(
                                        file_path=path, line_number=i+1, token=token, context_snippet=line.strip()
                                    ))
        return vulns
