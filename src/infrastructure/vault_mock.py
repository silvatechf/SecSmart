import uuid
import structlog

logger = structlog.get_logger()

class VaultMock:
    _instance = None
    _storage = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VaultMock, cls).__new__(cls)
        return cls._instance

    async def store_secret(self, key_type: str, value: str) -> str:
        vault_id = f"SEC_{key_type}_{uuid.uuid4().hex[:12].upper()}"
        self._storage[vault_id] = value
        logger.info("vault.stored", vault_id=vault_id)
        return vault_id
