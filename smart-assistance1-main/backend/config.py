import os
from dotenv import load_dotenv

# Load .env at import‑time
load_dotenv()

# Public config constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")         # set this in .env
EMBED_MODEL     = "text-embedding-3-small"
CHAT_MODEL      = "gpt-4o-mini"                      # or "gpt-4o" / "gpt-4"
MAX_TOKENS_PER_CHUNK = 500                           # ≈ 2k chars
TOP_K           = 4                                  # chunks to retrieve
