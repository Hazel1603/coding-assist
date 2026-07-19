# controlled, model-facing repository tools
from pathlib import Path

class FileParseError(Exception):
    pass

def read_file(workspace, requested_path, max_char=50_000):
    workspace = Path(workspace).resolve()
    target = (workspace / requested_path).resolve()

    if not target.is_relative_to(workspace):
        raise FileParseError("Path is outside the workspace")

    if not target.is_file():
        raise FileParseError("Path provided is not a file")
    
    if target.suffix.lower() != ".java":
        raise FileParseError("File is not a .java file")

    try:
        with target.open(encoding="utf-8") as file:
            content = file.read(max_char + 1)
    except UnicodeDecodeError as error:
        raise FileParseError("File is not valid UTF-8") from error
    except OSError as error:
        raise FileParseError(f"Could not read file: {error}") from error
    
    return {
        "content": content if len(content) <= max_char else content[:max_char],
        "truncated": len(content) > max_char
    }