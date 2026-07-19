from dataclasses import dataclass, field
from cd_assist.tools import LineSnippet, SearchResult, MatchType

def search_result_sort_key(result: SearchResult):
    return (
        result.path.lower(),
        result.line_snippet.line if result.line_snippet is not None else -1,
    )


@dataclass
class FileContext:
    file_name: str
    snippets: list[LineSnippet] = field(default_factory=list)

    def generate_context(self):
        sections = [f"File: {self.file_name}"]

        for line_snippet in self.snippets:
            sections.append(
                f"Line {line_snippet.line}:\n"
                f"{line_snippet.snippet.rstrip()}"
            )

        return "\n\n".join(sections)


def build_working_context(search_results: list[SearchResult], max_chars=20_000):
    for result in search_results:
        if result.match_type == MatchType.CONTENT and (
            result.line_snippet is None or result.line_snippet.line is None
        ):
            raise ValueError("Content search result requires a line snippet")

    results = sorted(search_results, key=search_result_sort_key)

    # split results into list[FileContext]
    file_contexts = []
    current_file_path = ""
    curr_file_context = None
    for result in results:
        if result.path != current_file_path:
            file_context_obj = FileContext(
                    file_name=result.path
                )
            file_contexts.append(file_context_obj)
            current_file_path = result.path
            curr_file_context = file_context_obj
        
        if result.match_type == MatchType.CONTENT:
            curr_file_context.snippets.append(result.line_snippet)
    
    # generate the context from list[FileContext]
    final_context_str = "\n\n".join(
        context.generate_context() for context in file_contexts
    )

    not_truncated_marker = "Context truncated: False"
    separator = "\n\n" if final_context_str else ""
    complete_context = final_context_str + separator + not_truncated_marker
    if len(complete_context) <= max_chars:
        return complete_context

    truncated_marker = "Context truncated: True"
    separator = "\n\n" if max_chars > len(truncated_marker) else ""
    available_context_chars = max(
        0,
        max_chars - len(separator) - len(truncated_marker),
    )
    truncated_context = (
        final_context_str[:available_context_chars]
        + separator
        + truncated_marker
    )
    return truncated_context[:max_chars]

