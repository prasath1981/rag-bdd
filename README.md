# RAG-BDD: Retrieval-Augmented Generation for BDD Feature Engineering

## Overview

**RAG-BDD** is a Python tool that leverages Retrieval-Augmented Generation (RAG) and LLMs to help you manage, rewrite, and generate BDD (Behavior-Driven Development) feature files. It enables you to:

- Parse `.feature` files into scenario chunks.
- Index and search scenarios using ChromaDB and HuggingFace embeddings.
- Rewrite existing scenarios in a descriptive style, preserving key phrases.
- Generate new BDD scenarios from requirements, with automatic consistency checks against existing scenarios.

## Features

- **Indexing:** Converts all `.feature` files into a vector database for semantic search.
- **Rewriting:** Rewrites scenarios in a more descriptive, consistent style using an LLM.
- **New Scenario Generation:** Given a requirement, suggests similar existing scenarios and generates a new, consistent scenario.
- **Consistency Check:** Before generating a new scenario, lists similar scenarios with similarity scores and summaries to avoid duplication.

## Dependencies

Install all dependencies with:

```bash
pip install -r requirements.txt
```

**Key dependencies:**
- `langchain==0.3.27`
- `openai==1.109.1`
- `chromadb==1.1.0`
- `sentence-transformers>=2.2.0`
- `pypdf==6.1.0`
- `python-dotenv>=1.0.0`
- `tqdm>=4.64.0`

You also need an OpenAI API key. Create a `.env` file in the project root with:

```
OPENAI_API_KEY=sk-...
```

## Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd rag-bdd
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key:**
   - Create a `.env` file in the project root.
   - Add your OpenAI API key as shown above.

4. **Prepare your feature files:**
   - Place your `.feature` files in the `features/` directory.

## Usage

All commands are run from the project root.

### 1. Index your feature files

```bash
python rag_bdd.py index --path features --persist ./chroma_db
```

This will index all `.feature` files in the `features/` directory into a Chroma vector database.

### 2. Rewrite a feature file in descriptive style

```bash
python rag_bdd.py rewrite --file features/retirement_calculator2.feature --persist ./chroma_db --out ./out/my_feature.descriptive.feature
```

- The rewritten file will be saved to the path specified by `--out`.

### 3. Generate a new scenario from a requirement

```bash
python rag_bdd.py new --requirement "User should be able to set a custom retirement age and see the updated projection." --persist ./chroma_db --top 5 --out ./out/new_scenario.feature
```

- The tool will print a consistency check: a list of similar existing scenarios with scores and summaries.
- If no highly similar scenario exists, a new scenario will be generated and saved to the specified output file.

## Project Structure

```
rag_bdd.py                # Main CLI tool
rag_bdd2.py               # Alternative pipeline (for experimentation)
requirements.txt          # Python dependencies
features/                 # Your BDD .feature files
chroma_db/                # Chroma vector database (auto-generated)
out/                      # Output directory for rewritten/generated features
```

## Notes

- The tool uses HuggingFace embeddings locally for privacy and speed.
- All LLM calls require a valid OpenAI API key.
- For best results, keep your `.feature` files well-structured and use standard Gherkin syntax.

