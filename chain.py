from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq

from schemas import TailoredResume


# ==============================================================================
# 3. LLM Chain Setup (Using Output Parser to Prevent Tool Calling Errors)
# ==============================================================================

# Initialize parser with the Pydantic schema to inject exact formatting instructions
parser = PydanticOutputParser(pydantic_object=TailoredResume)

system_instruction = """
You are an expert technical career strategist and resume optimization specialist.

Your task is to analyze a candidate's master background and tailor it into a strictly focused, high-impact 1-page resume matching a target job description.

{format_instructions}

Operating Rules:
1. Ground Truth & Strict Integrity: Use ONLY experiences, achievements, credentials, and technical skills present in the base resume. Never invent tools or metrics.
2. 1-Page Fit: Select EXACTLY 3 distinct work experiences from the base resume that best align with the target job. Provide 2 to 3 concise, high-impact bullets per role.
3. Skills Categorization: Group relevant tools into their respective categories under professional_skills.
4. Military Service & Languages: Preserve military service and spoken languages exactly as given in the base resume.
"""

cv_prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_instruction.strip()),
    ("human", """Candidate Full Background & Base Resume:
\"\"\"
{base_cv}
\"\"\"

Target Job Description:
\"\"\"
{job_description}
\"\"\"

Please generate the tailored resume JSON matching the target job description.""")
]).partial(format_instructions=parser.get_format_instructions())

# Use a highly reliable Groq model for structured parsing
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.1,
    max_tokens=4096
)

# Construct standard chain: Prompt -> LLM (Text) -> Pydantic Parser
cv_chain = cv_prompt_template | llm | parser