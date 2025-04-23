from pathlib import Path
from Bio import Entrez

from ..configs.parameters import fetch_top_k_papers
from ..configs.paths import DATA_PATH

from app.configs.prompts import REWRITE_QUERY_FOR_PUBMED_SEARCH
from app.models.chatting_model import get_chatting_model_openai

import time
import os
from dotenv import load_dotenv


load_dotenv()

Entrez.email = os.getenv("NCBI_EMAIL")
if not Entrez.email:
    raise RuntimeError(
        "❌ Missing NCBI_EMAIL in environment. Set NCBI_EMAIL=your.email@institution.edu in your .env"
    )

Entrez.api_key = os.getenv("NCBI_API_KEY")
if not Entrez.api_key:
    print("⚠️  No NCBI_API_KEY provided; continuing with low rate limits.")


QUERY = "What is the cure for aging and how to prevent aging?"


def rewrite_pubmed_query(QUERY: str) -> str:
    """
    Use an LLM to turn a natural question into a concise PubMed search string.
    """
    llm = get_chatting_model_openai()

    messages = [
        {"role": "system", "content": REWRITE_QUERY_FOR_PUBMED_SEARCH},
        {"role": "user", "content": QUERY},
    ]

    resp = llm.invoke(messages)
    query = getattr(resp, "content", resp).strip()

    print(f"🔄 Rewritten PubMed query: {query}")
    return query


def get_pmcid_for_pmid(pmid: str) -> str | None:
    handle = Entrez.elink(dbfrom="pubmed", db="pmc", id=pmid)
    linksets = Entrez.read(handle)
    handle.close()
    for block in linksets[0].get("LinkSetDb", []):
        if block.get("DbTo", "").lower() == "pmc" and block.get("Link"):
            return block["Link"][0]["Id"]
    return None


def fetch_top_k_pmc_papers(query: str, k: int) -> list[tuple[str, str]]:
    """
    Return a list of (PMID, PMC ID) for the first k papers in PubMed that have a free PMC PDF.
    Internally pages through results until k are found or the result set is exhausted.
    """
    collected = []
    retstart = 0
    batch = 20  # how many PMIDs to fetch at a time from PubMed

    while len(collected) < k:
        # 1) fetch the next batch of PMIDs
        handle = Entrez.esearch(
            db="pubmed",
            term=query,
            retmax=batch,
            retstart=retstart,
        )
        record = Entrez.read(handle)
        pmids = record.get("IdList", [])
        handle.close()

        if not pmids:
            # no more results at all
            break

        # 2) for each PMID see if it links to a free PMC article
        for pmid in pmids:
            if len(collected) >= k:
                break

            pmcid = get_pmcid_for_pmid(pmid)

            if pmcid:
                collected.append((pmid, pmcid))

        # 3) advance the window
        retstart += batch

        # be kind to NCBI servers
        time.sleep(0.3)

    return collected[:k]
