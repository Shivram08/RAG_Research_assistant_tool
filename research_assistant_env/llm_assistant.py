from langchain.memory import ConversationBufferMemory
from search_papers import search_papers
from langchain.memory import ConversationBufferMemory
from langchain_ollama import OllamaLLM  # Updated import

# Initialize DeepSeek R1
llm = OllamaLLM(model="deepseek-r1:7b")

\

memory = ConversationBufferMemory(return_messages=True)

def critique_research_paper(paper_text):
    """
    Uses DeepSeek R1 to critique a research paper.

    Args:
        paper_text (str): The full text of the research paper.

    Returns:
        str: AI-generated critique with suggestions for improvement.
    """
    prompt = f"""
    You are an expert research paper reviewer. Critique the following paper.

    **Paper Content:**
    {paper_text[:5000]}  # Limiting to 5000 characters to avoid overload

    Provide a structured critique including:
    - Strengths of the paper
    - Weaknesses and areas of improvement
    - Suggestions for better clarity, argumentation, or citations
    - Any potential issues with methodology or results
    """

    response = llm.invoke(prompt)
    return response


def answer_query_with_citations(query):
    """
    Streams DeepSeek R1 response as it is generated.
    """
    research_context = search_papers(query)
    conversation_history = memory.load_memory_variables({}).get("history", "")

    prompt = f"""
    You are an AI assistant specializing in machine learning.
    
    **Previous Conversation:**
    {conversation_history}

    **User Query:** {query}

    **Relevant Research Papers:**
    {research_context}

    Provide a well-structured, **concise** answer with **numbered citations**.
    """

    # Stream the response from DeepSeek R1
    def generate_response():
        for chunk in llm.stream(prompt):
            yield chunk

    return generate_response()


