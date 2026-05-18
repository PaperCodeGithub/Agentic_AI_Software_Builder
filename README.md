# IRUS
This is an **Agentic Code-Generation & Repository Workspace Engine**. It is a command-line pipeline that acts as a local product team. When a user requests an application, 
the system handles the layout, drafts the technical architecture, validates output fields, writes clean source code, generates binary UI/image assets via an asset engine, and 
spins up a localized Retrieval-Augmented Generation (RAG) environment so you can talk to, modify, and debug the generated codebase in real time.

---

## Features

* **Multi-Agent Pipeline**: Separates planning from engineering to guarantee cleaner structural blueprints and highly decoupled workflows.
* **Strict Schema Enforcement**: Implements LangChain Expression Language (LCEL) paired with Pydantic output parsers to ensure local models output clean, reliable JSON data without conversational filler.
* **Intelligent Asset Routing**: Automatically splits standard source code writing from binary visual asset generation via a dedicated asset engine wrapper.
* **Dual-Mode Codebase Traversal**: Embeds generated applications into an interactive Retrieval-Augmented Generation (RAG) loop, allowing users to choose between text streaming (Query mode) or direct source-code modification (Agent mode).

## Technical Architecture

The codebase operates via four distinct execution layers:

1. **The PlannerEngine (Layer 1)**: Accepts the user's high-level instruction and structures a comprehensive architectural breakdown detailing required files, relative paths, and technical stacks. No actual code is written here.
2. **The ArchEngineer (Layer 2)**: Executes the planner's JSON payload. Code scripts are written sequentially to the file system, shell scripts are granted execution privileges via file permissions, and asset descriptors are isolated for binary synthesis.
3. **AssetEngine (Layer 3)**: Logs session history and raw schema generations into a centralized database instance to protect context windows and enable pagination workflows.
4. **Traversal & Debugging Engine (Layer 4)**: Leverages a multi-language chunking pipeline backed by a vectorized storage instance to read, analyze, and stream codebase updates or handle programmatic file refactoring.

## Tech Stack
* **Orchestration**: LangChain (LCEL), LangChain-Core, LangChain-Community, LangChain-classic
* **Inference Models**: Qwen-Coder (`qwen3-coder:480b-cloud` Ollama model)
* **Vector Store**: LangChroma (ChromaDB)
* **Text Processing**: LangChain-Text-Splitters, LangChain-HuggingFace (`all-MiniLM-L6-v2`)
* **Data Validation**: Pydantic v2
* **Terminal UI Utilities**: Rich, Colorama

