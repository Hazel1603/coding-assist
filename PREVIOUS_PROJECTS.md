# Previous Projects

This file summarizes the agent-building concepts already covered in earlier projects. It is intended to give the next project enough background to build on prior work without repeating introductory material.

## Project 1: AI CLI Assistant

The first project was a command-line AI assistant focused on direct model interaction, conversation state, tool calling, structured responses, and basic observability.

### Implemented Capabilities

- Integrated with the OpenAI Responses API.
- Loaded an API key from local environment configuration.
- Ran as an interactive terminal assistant.
- Streamed and handled model response events internally.
- Maintained multi-turn conversation history.
- Persisted conversation history to local storage.
- Restored previous conversation history when the application started.
- Supported inspecting and clearing conversation history.
- Defined a real function tool named `read_text_file`.
- Allowed the model to request tool calls.
- Executed requested tool calls in Python.
- Returned tool results through `function_call_output`.
- Supported multiple rounds of model-tool interaction.
- Supported tool chains where one file referred to another file.
- Tracked which files had been successfully read.
- Cached file contents in runtime memory.
- Avoided rereading already cached files unless memory was cleared.
- Returned structured assistant responses using a JSON schema.
- Parsed structured fields including `answer`, `summary`, `files_used`, and `follow_up_questions`.
- Reported token usage after successful model calls.
- Logged usage and runtime events to JSONL.
- Logged model call success, parsing failures, model errors, user input, token usage, success status, and files used.
- Included commands for viewing total usage and detailed logs.
- Included a clean CLI loop, help command, graceful exit handling, and Ctrl+C handling.
- Included basic unit-test coverage.
- Validated supported local file types.

### Concepts Covered

- Model API integration.
- System and user messages.
- Multi-turn conversation state.
- Persisted assistant memory.
- Structured outputs.
- JSON-schema-constrained responses.
- Parsing and validating model output.
- Function/tool schemas.
- Model-selected tool calls.
- Python-side tool execution.
- Returning tool observations to the model.
- Multi-round tool calling.
- Runtime caching.
- Local file access as a tool.
- Token usage tracking.
- JSONL observability logs.
- Handling incomplete, failed, and error response events.
- Basic agent loop behavior.
- Basic CLI usability patterns.
- Basic unit testing for agent-adjacent code.

### Concepts Introduced But Not Deeply Explored

- Agent loops beyond simple tool calling.
- Stateful versus stateless agent behavior.
- Tool-call evaluation.
- Context growth over long sessions.
- Tool security and prompt injection.
- Retry behavior.
- Idempotency.
- Variance in model outputs.
- Durable state design.
- Trajectory evaluation.

## Project 2: Personal Knowledge Assistant

The second project was a personal knowledge assistant focused on retrieval-augmented generation concepts, document chunking, context construction, citation, and retrieval evaluation design.

The central learning question was:

```text
What information should be placed into the model's context?
```

The intended assistant pipeline was:

```text
User Question
      ↓
Query Processing
      ↓
Document Retrieval
      ↓
Ranking
      ↓
Context Construction
      ↓
LLM Answer
      ↓
Sources and Evaluation
```

### Implemented Capabilities

- Loaded notes from a folder passed on the command line.
- Recursively scanned nested folders.
- Loaded `.md`, `.txt`, `.MD`, and `.TXT` files.
- Skipped unsupported file types.
- Skipped files that could not be read as UTF-8.
- Sorted loaded paths for deterministic output.
- Printed the number of loaded notes and each loaded note path.
- Listed loaded notes from the CLI.
- Displayed a selected note from the CLI.
- Searched loaded notes from the CLI.
- Searched both note paths and note contents.
- Performed case-insensitive keyword search.
- Displayed a friendly message when no notes matched.
- Split loaded notes into smaller text chunks.
- Preserved source note path on each chunk.
- Assigned stable chunk indexes.
- Skipped empty notes and empty chunks.
- Split long notes into multiple chunks.
- Generated deterministic fake embeddings for chunks.
- Represented embeddings as lists of floats.
- Preserved original chunks when embedding them.
- Stored embedded chunks in a local in-memory vector database.
- Preserved note path, chunk index, content, and embedding in vector records.
- Retrieved relevant chunks for a user question.
- Converted user questions into fake embeddings.
- Compared question embeddings against stored vector records.
- Ranked retrieval results by similarity score.
- Supported limiting retrieved results with `top_k`-style behavior.
- Returned no results for empty questions or empty vector databases.
- Built compact context blocks from retrieved chunks.
- Included source note path, chunk index, and content in context.
- Preserved retrieval ranking order during context construction.
- Enforced a configurable character budget for context.
- Excluded chunks that did not fit within the context budget.
- Answered questions using constructed context and a model abstraction.
- Returned a friendly fallback when no relevant context was available.
- Kept answer generation testable with a fake or placeholder model.
- Displayed citations for source chunks used in an answer.
- Included note path and chunk index in citation strings.
- Deduplicated repeated citation references.
- Covered loader, search, chunking, embedding, vector storage, retrieval, context construction, answer generation, citation, print, and CLI behavior with tests.

### Concepts Covered

- Retrieval-augmented generation as a pipeline.
- Separating retrieval, ranking, context construction, answer generation, and citation.
- Document loading for a local knowledge base.
- Recursive file discovery.
- Deterministic ordering for testability.
- Keyword search as a retrieval baseline.
- Chunking documents before retrieval.
- Stable chunk identity.
- Fake embeddings as a learning abstraction.
- Vector records and vector database basics.
- Similarity scoring with dot product.
- Ranking retrieved context.
- Limiting retrieval results.
- Context construction from retrieved records.
- Context budgets and pruning.
- Distinguishing retrieved context from generated answers.
- Grounding answers in provided context.
- Friendly fallback behavior when context is missing.
- Source citation for retrieved chunks.
- Deduplicating citations.
- Test-driven development of retrieval components.
- Using fake models and fake embeddings to learn architecture before adding provider complexity.

### Planned Or Partially Covered Concepts

- Loading a retrieval evaluation dataset.
- Defining evaluation questions with expected source notes.
- Calculating Retrieval Recall@K.
- Reporting per-question retrieval results.
- Reporting aggregate retrieval metrics.
- Measuring approximate context size.
- Comparing retrieval settings such as `top_k=3` and `top_k=5`.
- Making quality versus context-cost tradeoffs visible.
- Re-indexing after notes are added, changed, or deleted.
- Preserving deterministic behavior for unchanged notes during re-indexing.

## Current Learning Baseline

At this point, the learner has already built two important foundations:

- A model-facing assistant that can call tools, maintain conversation state, produce structured output, and log usage.
- A retrieval-facing assistant that can load notes, chunk them, embed them with a fake embedding function, store them in a simple vector database, retrieve relevant chunks, build model context, answer from context, and cite sources.

The next project should assume familiarity with:

- Python command-line applications.
- Basic OpenAI API usage.
- Model messages and responses.
- Function/tool calling.
- Tool schemas and tool execution.
- Structured JSON outputs.
- Conversation history.
- Runtime memory and caching.
- Local file reading.
- Token usage logging.
- Basic observability.
- Unit testing.
- Document loading.
- Keyword search.
- Chunking.
- Embedding abstractions.
- Vector records.
- Similarity search.
- Retrieval ranking.
- Context construction.
- Citation.
- Retrieval-focused testing.

## Good Next Learning Directions

Future projects should build on the existing foundation instead of rebuilding it. Useful next directions include:

- Replacing fake embeddings with real embeddings and measuring the improvement.
- Adding persistent vector storage after the indexing lifecycle is clear.
- Connecting answer generation to a real LLM after context construction is testable.
- Building retrieval evaluation before optimizing retrieval quality.
- Measuring latency, token usage, and cost for retrieval-augmented workflows.
- Studying prompt injection risks from retrieved external content.
- Adding stronger tool security boundaries.
- Evaluating complete agent trajectories, not only final answers.
- Designing durable state for longer-running multi-step agents.
- Introducing retries, idempotency, and recovery behavior.
- Adding observability for retrieval, tool calls, model calls, and user-visible outcomes.

## What The Next Project Should Avoid Repeating

The next project should not spend major time reintroducing:

- Basic CLI loops.
- Basic model API calls.
- Basic structured output parsing.
- Basic function-tool execution.
- Basic file-reading tools.
- Basic conversation history.
- Basic note loading.
- Basic chunking.
- Basic fake embedding generation.
- Basic in-memory vector search.
- Basic source citation formatting.

These can be reused or extended as needed, but the learning focus should move toward deeper agent behavior, evaluation, reliability, safety, persistence, and observability.
