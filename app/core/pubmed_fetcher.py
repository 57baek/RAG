from pathlib import Path
from Bio import Entrez
import time

from ..configs.parameters import (
    fetch_top_k_papers,
    fetch_batch_size,
    sleep_time_for_each_fetching,
)

from app.models.chatting_model import get_chatting_model_openai
from app.configs.prompts import REWRITE_QUERY_FOR_PUBMED_SEARCH
from ..configs.paths import DATA_PATH


def get_pmcid_from_pmid(pmid: str) -> str | None:
    """
    Given a PubMed ID (PMID), find out if there’s a PMC ID (i.e. full-text open-access version).
    """
    handle = Entrez.elink(dbfrom="pubmed", db="pmc", id=pmid)
    linksets = Entrez.read(handle)
    handle.close()

    for block in linksets[0].get("LinkSetDb", []):
        if block.get("DbTo", "").lower() == "pmc" and block.get("Link"):
            return block["Link"][0]["Id"]

    return None


def download_pmc_fulltext_xml(pmcid: str, out_path: Path) -> None:
    try:
        handle = Entrez.efetch(db="pmc", id=pmcid, rettype="xml", retmode="text")
        xml_data = handle.read()
        handle.close()

        # Handle bytes if for some reason we get it
        if isinstance(xml_data, bytes):
            xml_data = xml_data.decode("utf-8")

        if not xml_data.strip():
            raise ValueError("Empty XML returned.")

        out_path.write_text(xml_data, encoding="utf-8")
        print(f"✅ XML saved to {out_path}")

    except Exception as e:
        print(f"❌ Failed to download XML for PMC{pmcid}: {e}")


def rewrite_pubmed_query(query_text: str) -> str:
    """
    Use an LLM to turn a natural question into a concise PubMed search string.
    """
    llm = get_chatting_model_openai()

    messages = [
        {"role": "system", "content": REWRITE_QUERY_FOR_PUBMED_SEARCH},
        {"role": "user", "content": query_text},
    ]

    resp = llm.invoke(messages)
    query = getattr(resp, "content", resp).strip()

    print(f"🔄 Rewritten PubMed query: {query}")
    return query


def fetch_top_k_pmc_papers(query: str) -> list[tuple[str, str]]:
    """
    Return a list of (PMID, PMC ID) for the first k papers in PubMed that have a free PMC PDF.
    Internally pages through results until k are found or the result set is exhausted.
    """
    collected = []
    retstart = 0
    batch = fetch_batch_size  # how many PMIDs to fetch at a time from PubMed

    while len(collected) < fetch_top_k_papers:
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
            if len(collected) >= fetch_top_k_papers:
                break

            pmcid = get_pmcid_from_pmid(pmid)

            if pmcid:
                collected.append((pmid, pmcid))

        # 3) advance the window
        retstart += batch

        # Let's be kind to NCBI servers
        time.sleep(sleep_time_for_each_fetching)

    return collected[:fetch_top_k_papers]


def download_xml(results):
    for pmid, pmcid in results:
        xml_path = Path(DATA_PATH) / f"{pmid}.xml"
        if xml_path.exists():
            print(f"📂 {xml_path.name} already exists, skipping.")
            continue

        print(f"⬇️ Downloading full text XML for PMC{pmcid}...")
        download_pmc_fulltext_xml(pmcid, xml_path)
