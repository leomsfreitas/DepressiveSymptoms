from pathlib import Path

load_prompt = lambda path: Path(path).read_text(encoding="utf-8")

user_prompt = lambda text: f"# Input\n\nPostagem:\n\n{text}\n\n\nResposta:"