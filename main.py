import os
from dotenv import load_dotenv

from utils.extract import extract_pages_from_file
from utils.llm_selector import get_llm
from models.milestone_models import MilestoneExtractionResult

from langchain.prompts import ChatPromptTemplate

def analyze_milestones(file_path: str, provider: str = "gemini"):
    # Load API keys
    load_dotenv()

    # Extract pages from file (returns list[str])
    pages = extract_pages_from_file(file_path)

    # Combine all pages into one string for analysis
    full_text = "\n\n".join(pages)

    # Get chosen LLM (OpenAI or Gemini)
    llm = get_llm(provider)

    # Force LLM to return our Pydantic model
    structured_llm = llm.with_structured_output(MilestoneExtractionResult)

    # Build prompt
    prompt = ChatPromptTemplate.from_template("""
You are an AI assistant that analyzes the Proposal documents for final year projects for bachelors of engineering students. 
                                              

Read the text and extract the following informtion:

1. If there are clearly defined milestones with deliverables and due dates, return:
   - status: "success"
   - tasks: A list of tasks, each having title, description, deliverable, and due_date (YYYY-MM-DD)
   - message: "" (empty string)

2. If these details are not clearly mentioned, return:
   - status: "failed"
   - tasks: null
   - message: Explain briefly why milestone extraction failed. Like a due date not mentioned for the milestone, the deliverable if not mentioned clearly etc.

Notes: 
- If any proposal document mentions that they plan to publist a paper in a journal or conference so, you must extract that as a task. The deadline for the conference should be clearly mentioned. If it is not mentioned, you may reject the extraction process, return a failed status and ask the user in message to provide the required details.
- For invalid dates like Feb 31st, You may normalize them to valid dates like to Feb 28th.
- You MUST set the status to "failed" if the due date is not mentioned or is unclear.
- You MUST set the status to "failed" if the description or deliverable is unclear.
Here is the proposal document's extracted text:
{text}
""")

    # Chain prompt + model
    chain = prompt | structured_llm

    # Run chain
    result = chain.invoke({"text": full_text})

    return result


if __name__ == "__main__":
    # Example usage
    file_path = "/home/salman/Desktop/Rag service/FYP Proposal Document.docx"  # or .docx / .txt
    provider = "openai"       # or "gemini"

    output = analyze_milestones(file_path, provider)
    print(output.model_dump_json(indent=2))
