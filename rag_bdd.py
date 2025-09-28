#!/usr/bin/env python3
"""
rag_bdd.py
Simple RAG tool for BDD feature files:
- parse .feature files into scenario chunks
- index into Chroma (HuggingFace embeddings via LangChain)
- rewrite feature(s) in descriptive style preserving exact phrases
- create new scenario from requirement and list matching scenarios
"""

import os
import re
import argparse
from typing import List, Dict, Tuple
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI

# rag_bdd.py

from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI

# 1. Load environment variables from .env file
load_dotenv()

# 2. Fetch API key
api_key = os.getenv("OPENAI_API_KEY")

# 3. Initialize OpenAI client
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    openai_api_key="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"
)

# rest of your imports and RAG pipeline code go here...


# -----------------------
# Parser: Feature -> Scenarios (simple, regex-based)
# -----------------------
def parse_feature_file(path: str) -> List[Dict]:
    """
    Parse a Gherkin .feature file into a list of scenario dicts:
    { 'feature': ..., 'scenario': ..., 'steps': [...], 'raw': ..., 'file': path }
    This is intentionally simple and assumes standard Gherkin keywords in English.
    """
    scenarios = []
    current_feature = None
    current_scenario = None
    current_steps = []
    raw_lines = []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        raw_lines.append(line)
        m_feat = re.match(r'^\s*Feature:\s*(.+)', line, re.IGNORECASE)
        m_scn = re.match(r'^\s*Scenario(?: Outline)?:\s*(.+)', line, re.IGNORECASE)
        m_step = re.match(r'^\s*(Given|When|Then|And|But)\b(.*)', line, re.IGNORECASE)
        if m_feat:
            current_feature = m_feat.group(1).strip()
        elif m_scn:
            # push previous scenario
            if current_scenario:
                scenarios.append({
                    'feature': current_feature,
                    'scenario': current_scenario,
                    'steps': [s.strip() for s in current_steps],
                    'raw': '\n'.join(raw_lines),  # raw file; useful for reference
                    'file': path
                })
                current_steps = []
            current_scenario = m_scn.group(1).strip()
        elif m_step and current_scenario:
            # preserve the whole step line (keyword + rest)
            step_line = line.strip()
            current_steps.append(step_line)
        # else ignore other lines for now (Examples, background, comments handled loosely)

    # push last scenario
    if current_scenario:
        scenarios.append({
            'feature': current_feature,
            'scenario': current_scenario,
            'steps': [s.strip() for s in current_steps],
            'raw': '\n'.join(raw_lines),
            'file': path
        })
    return scenarios

def parse_path(path: str) -> List[Dict]:
    """
    Accept either a single .feature file or a directory of .feature files.
    Returns combined list of scenario dicts.
    """
    scen_list = []
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for fn in files:
                if fn.endswith('.feature'):
                    scen_list.extend(parse_feature_file(os.path.join(root, fn)))
    elif os.path.isfile(path) and path.endswith('.feature'):
        scen_list = parse_feature_file(path)
    else:
        raise ValueError("Please provide a .feature file or directory containing .feature files.")
    return scen_list

# -----------------------
# Build index
# -----------------------
def build_index(scenarios: List[Dict], persist_dir: str = "./chroma_db"):
    """
    Convert scenario list to LangChain Documents and index with Chroma.
    """
    docs = []
    for i, s in enumerate(scenarios):
        content = f"Feature: {s.get('feature')}\nScenario: {s.get('scenario')}\n" + "\n".join(s.get('steps', []))
        metadata = {
            'file': s.get('file'),
            'feature': s.get('feature'),
            'scenario': s.get('scenario'),
            'id': f"{os.path.basename(s['file'])}::scenario::{i}"
        }
        docs.append(Document(page_content=content, metadata=metadata))

    emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")  # local embeddings (requires sentence-transformers)
    vectordb = Chroma.from_documents(docs, emb, persist_directory=persist_dir)
    vectordb.persist()
    print(f"Indexed {len(docs)} scenario documents into Chroma at {persist_dir}")
    return vectordb

# -----------------------
# Utilities: retrieval + step extraction
# -----------------------
def extract_steps_from_text(text: str) -> List[str]:
    return re.findall(r'^\s*(Given|When|Then|And|But)[^\n]*', text, flags=re.IGNORECASE | re.MULTILINE)

def find_matches(vectordb: Chroma, query: str, k: int = 5) -> List[Dict]:
    """
    Returns a list of matches with score, metadata, and a summary (first step or truncated scenario).
    """
    results = vectordb.similarity_search_with_score(query, k=k)
    matches = []
    for doc, score in results:
        steps = extract_steps_from_text(doc.page_content)
        summary = steps[0] if steps else doc.page_content[:80] + ("..." if len(doc.page_content) > 80 else "")
        matches.append({
            'score': score,
            'text': doc.page_content,
            'metadata': doc.metadata,
            'steps': steps,
            'summary': summary
        })
    return matches

# -----------------------
# LLM prompts & calls
# -----------------------
def call_llm(prompt: str, model_name="gpt-3.5-turbo", temperature=0.0) -> str:
    """
    Uses LangChain ChatOpenAI wrapper. Make sure OPENAI_API_KEY is set in env.
    Uses .invoke() for robust compatibility.
    """
    llm = ChatOpenAI(model_name=model_name, temperature=temperature)
    result = llm.invoke(prompt)
    # Robust extraction for different LangChain versions
    if isinstance(result, dict) and 'content' in result:
        return result['content']
    elif hasattr(result, 'content'):
        return result.content
    elif isinstance(result, str):
        return result
    else:
        return str(result)

# Prompt templates
REWRITE_PROMPT = """You are an expert BDD engineer. Re-write the ORIGIN_SCENARIO below into a descriptive style BDD scenario (Gherkin format).
Rules:
- Keep these exact phrases (case + whitespace) unchanged wherever applicable: 
{preserve_list}
- Use the CONTEXT snippets below to remain consistent with existing naming and phrasing.
- Keep the Gherkin keywords (Feature, Scenario, Given/When/Then/And/But).
- Produce only the rewritten scenario (Feature & Scenario & Steps), no extra commentary.

CONTEXT:
{context}

ORIGIN_SCENARIO:
{origin}
"""

NEW_SCENARIO_PROMPT = """You are an expert BDD engineer. Create a new BDD Scenario (Gherkin) that satisfies the requirement below.
Rules:
- Keep these exact phrases unchanged: {preserve_list}
- Use the CONTEXT snippets below to maintain consistent naming/phrasing.
- Provide a short header "Matches:" that lists matching existing scenarios (filename::scenario title) with similarity scores.
- Output only the Gherkin Scenario (Feature + Scenario + Steps) followed by the Matches listing.

CONTEXT:
{context}

REQUIREMENT:
{requirement}
"""

# -----------------------
# High-level operations
# -----------------------
def rewrite_feature_file(path: str, vectordb: Chroma, output_path: str = None):
    """
    Read one feature file, parse scenarios, for each scenario retrieve context and ask LLM to rewrite descriptively.
    """
    scenarios = parse_feature_file(path)
    rewritten_sections = []
    for s in scenarios:
        origin = f"Feature: {s['feature']}\nScenario: {s['scenario']}\n" + "\n".join(s['steps'])
        # Find matches for the scenario text
        matches = find_matches(vectordb, origin, k=5)
        # collect preserve phrases (unique step lines from matches)
        preserve = set()
        context_snippets = []
        for m in matches:
            context_snippets.append(f"[{m['metadata']['file']}::{m['metadata']['scenario']}] {m['text']}")
            for st in m['steps']:
                # keep only meaningful short steps; strip leading whitespace
                preserve.add(st.strip())
        preserve_list = "\n".join(sorted(preserve))
        context = "\n\n".join(context_snippets) if context_snippets else ""
        prompt = REWRITE_PROMPT.format(preserve_list=preserve_list, context=context, origin=origin)
        rewritten = call_llm(prompt)
        rewritten_sections.append(rewritten.strip())
        print(f"Rewrote scenario: {s['scenario']}")
    out = "\n\n".join(rewritten_sections)
    if not output_path:
        output_path = path.replace(".feature", ".descriptive.feature")
    # Ensure output directory exists
    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(out)
    print(f"Wrote rewritten file to {output_path}")


def new_scenario_from_requirement(requirement: str, vectordb: Chroma, top_k: int = 5, output_path: str = None):
    """
    Given a textual requirement, retrieve matches and ask LLM to generate a new, consistent scenario.
    Also returns the list of matching existing scenarios, with a consistency check.
    """
    matches = find_matches(vectordb, requirement, k=top_k)
    preserve = set()
    context_snippets = []
    matches_list = []
    print("\n--- Consistency Check: Similar Existing Scenarios ---")
    threshold = 0.8  # similarity threshold for warning
    found_high = False
    for m in matches:
        context_snippets.append(f"[{m['metadata']['file']}::{m['metadata']['scenario']}] {m['text']}")
        matches_list.append(f"{m['metadata']['file']}::{m['metadata']['scenario']} (score={m['score']:.4f})")
        for st in m['steps']:
            preserve.add(st.strip())
        print(f"- Feature: {m['metadata'].get('feature', '')}")
        print(f"  Scenario: {m['metadata'].get('scenario', '')}")
        print(f"  Score: {m['score']:.4f}")
        print(f"  Summary: {m['summary']}")
        print()
        if m['score'] >= threshold:
            found_high = True
    if found_high:
        print("WARNING: One or more similar scenarios have a high similarity score. This requirement may already be covered.\n")
    prompt = NEW_SCENARIO_PROMPT.format(
        preserve_list="\n".join(sorted(preserve)),
        context="\n\n".join(context_snippets),
        requirement=requirement
    )
    generated = call_llm(prompt)
    # Save or print
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(generated)
        print(f"Wrote generated scenario to {output_path}")
    print("\n--- Generated Scenario ---\n")
    print(generated)
    print("\n--- Matching existing scenarios (top results) ---")
    for m in matches_list:
        print("-", m)


# -----------------------
# CLI
# -----------------------
def main():
    parser = argparse.ArgumentParser(description="RAG BDD tool")
    sub = parser.add_subparsers(dest='cmd')

    p_idx = sub.add_parser('index', help='Index .feature files into Chroma')
    p_idx.add_argument('--path', required=True, help='.feature file or directory')
    p_idx.add_argument('--persist', default='./chroma_db', help='Chroma persist directory')

    p_rewrite = sub.add_parser('rewrite', help='Rewrite a feature file descriptively')
    p_rewrite.add_argument('--file', required=True, help='path to feature file to rewrite')
    p_rewrite.add_argument('--persist', default='./chroma_db', help='Chroma persist directory')
    p_rewrite.add_argument('--out', default=None, help='output file')

    p_new = sub.add_parser('new', help='Create new scenario from requirement')
    p_new.add_argument('--requirement', required=True, help='requirement text')
    p_new.add_argument('--persist', default='./chroma_db', help='Chroma persist directory')
    p_new.add_argument('--top', type=int, default=5, help='top-k matches')
    p_new.add_argument('--out', default=None, help='output file to save scenario')

    args = parser.parse_args()
    if args.cmd == 'index':
        scenarios = parse_path(args.path)
        build_index(scenarios, persist_dir=args.persist)
    elif args.cmd == 'rewrite':
        # load vectordb
        emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectordb = Chroma(persist_directory=args.persist, embedding_function=emb)
        rewrite_feature_file(args.file, vectordb, output_path=args.out)
    elif args.cmd == 'new':
        emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectordb = Chroma(persist_directory=args.persist, embedding_function=emb)
        new_scenario_from_requirement(args.requirement, vectordb, top_k=args.top, output_path=args.out)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
