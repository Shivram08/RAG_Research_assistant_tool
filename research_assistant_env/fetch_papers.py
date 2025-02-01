import arxiv

def fetch_research_papers(query, max_results=10):
    """
    Fetches research papers from arXiv based on the refined query.
    
    Args:
        query (str): Search query (e.g., "Large Language Models").
        max_results (int): Number of papers to retrieve.

    Returns:
        list: A list of dictionaries containing paper details.
    """
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    relevant_papers = []
    keywords = ["LLM", "Large Language Model", "GPT", "Transformer", "Deep Learning"]

    for result in search.results():
        # Check if any keyword is in the title or summary
        if any(kw.lower() in result.title.lower() or kw.lower() in result.summary.lower() for kw in keywords):
            paper_info = {
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "summary": result.summary,
                "pdf_url": result.pdf_url,
                "published": result.published.strftime("%Y-%m-%d"),
            }
            relevant_papers.append(paper_info)

    return relevant_papers

# Example: Fetch only LLM-related papers
if __name__ == "__main__":
    refined_query = '("Large Language Models" OR "LLM") AND ("Transformer" OR "GPT" OR "Deep Learning")'
    papers = fetch_research_papers(refined_query)

    for i, paper in enumerate(papers):
        print(f"\n🔹 Paper {i+1}: {paper['title']}")
        print(f"   📅 Published: {paper['published']}")
        print(f"   ✍️ Authors: {', '.join(paper['authors'])}")
        print(f"   📄 PDF: {paper['pdf_url']}")
        print(f"   🔍 Summary: {paper['summary'][:500]}...\n")  # Print first 500 characters of summary
