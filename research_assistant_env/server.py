import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import pypdf
from llm_assistant import answer_query_with_citations, critique_research_paper

app = FastAPI()

@app.get("/ask")
async def ask(query: str):
    return StreamingResponse(answer_query_with_citations(query), media_type="text/plain")

@app.post("/upload-paper")
async def upload_paper(file: UploadFile = File(...)):
    """
    Uploads a research paper (PDF) and sends it for critique.
    """
    try:
        pdf_reader = pypdf.PdfReader(file.file)
        paper_text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        critique = critique_research_paper(paper_text)
        return {"critique": critique}
    except Exception as e:
        return {"error": f"Failed to process paper: {str(e)}"}

# Run FastAPI correctly
if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
