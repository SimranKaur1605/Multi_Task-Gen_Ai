"""
Multi-Task GenAI System using LangChain + Google Gemini (Free)
===============================================================
Supports: Summarization, Q&A, Quiz Generation, Study Plan, Code Explanation
"""

import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

load_dotenv()



def get_llm(model: str = "llama-3.3-70b-versatile", temperature: float = 0.7):
    import os
    from langchain_groq import ChatGroq
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY environment variable is not set.")

    return ChatGroq(
        model=model,
        temperature=temperature,
        groq_api_key=api_key
    )

PROMPTS = {
    "summarize": PromptTemplate(
        input_variables=["document"],
        template="""You are an expert summarizer.
Given the following document or text, produce a clear and concise summary.
Highlight the main ideas, key points, and any important conclusions.

Document:
{document}

Summary:"""
    ),

    "qa": PromptTemplate(
        input_variables=["document", "question"],
        template="""You are a knowledgeable assistant that answers questions strictly based on the provided context.
If the answer cannot be found in the context, say "I don't know based on the provided content."

Context:
{document}

Question: {question}

Answer:"""
    ),

    "quiz": PromptTemplate(
        input_variables=["document", "num_questions"],
        template="""You are an expert quiz generator and educator.
Based on the following content, generate {num_questions} multiple-choice questions.

Format each question as:
Q[n]. <Question>
A) <Option>
B) <Option>
C) <Option>
D) <Option>
Answer: <Correct letter>
Explanation: <Brief explanation>

Content:
{document}

Quiz:"""
    ),

    "study_plan": PromptTemplate(
        input_variables=["document", "duration_days"],
        template="""You are an academic coach and curriculum designer.
Based on the following content, create a structured {duration_days}-day study plan.

For each day include:
- Day number and theme
- Topics to cover
- Recommended activities (reading, practice, review)
- Learning objectives

Content:
{document}

Study Plan:"""
    ),

    "explain_code": PromptTemplate(
        input_variables=["document"],
        template="""You are a senior software engineer and technical educator.
Analyze and explain the following code clearly for a developer audience.

Provide:
1. **Overview** - What the code does at a high level
2. **Line-by-line / block-by-block explanation** - Walk through key sections
3. **Key concepts used** - Libraries, patterns, algorithms
4. **Potential improvements** - Suggestions for better code quality or performance

Code:
{document}

Explanation:"""
    ),
}


def build_chain(task: str, llm):
    if task not in PROMPTS:
        raise ValueError(f"Unknown task '{task}'. Available: {list(PROMPTS.keys())}")
    prompt = PROMPTS[task]
    return prompt | llm | StrOutputParser()




def run_summarize(document: str, llm) -> str:
    return build_chain("summarize", llm).invoke({"document": document})

def run_qa(document: str, question: str, llm) -> str:
    return build_chain("qa", llm).invoke({"document": document, "question": question})

def run_quiz(document: str, num_questions: int, llm) -> str:
    return build_chain("quiz", llm).invoke({"document": document, "num_questions": num_questions})

def run_study_plan(document: str, duration_days: int, llm) -> str:
    return build_chain("study_plan", llm).invoke({"document": document, "duration_days": duration_days})

def run_explain_code(code: str, llm) -> str:
    return build_chain("explain_code", llm).invoke({"document": code})




TASK_REGISTRY = {
    "1": {
        "name": "Summarize Document",
        "key": "summarize",
        "handler": lambda doc, llm, **kw: run_summarize(doc, llm),
        "extra_params": [],
    },
    "2": {
        "name": "Question & Answer",
        "key": "qa",
        "handler": lambda doc, llm, **kw: run_qa(doc, kw["question"], llm),
        "extra_params": [("question", "Enter your question: ")],
    },
    "3": {
        "name": "Generate Quiz",
        "key": "quiz",
        "handler": lambda doc, llm, **kw: run_quiz(doc, int(kw["num_questions"]), llm),
        "extra_params": [("num_questions", "How many questions? (e.g. 5): ")],
    },
    "4": {
        "name": "Create Study Plan",
        "key": "study_plan",
        "handler": lambda doc, llm, **kw: run_study_plan(doc, int(kw["duration_days"]), llm),
        "extra_params": [("duration_days", "Study plan duration in days (e.g. 7): ")],
    },
    "5": {
        "name": "Explain Code",
        "key": "explain_code",
        "handler": lambda doc, llm, **kw: run_explain_code(doc, llm),
        "extra_params": [],
    },
}


def dispatch_task(task_id: str, document: str, llm) -> str:
    if task_id not in TASK_REGISTRY:
        return "Invalid task selection."
    task = TASK_REGISTRY[task_id]
    kwargs = {}
    for param_key, prompt_text in task["extra_params"]:
        kwargs[param_key] = input(prompt_text).strip()
    print(f"\n⏳ Running: {task['name']}...\n")
    return task["handler"](document, llm, **kwargs)




def print_menu():
    print("\n" + "═" * 52)
    print("   🤖 Multi-Task GenAI System (LangChain + Gemini)")
    print("═" * 52)
    for key, task in TASK_REGISTRY.items():
        print(f"  [{key}] {task['name']}")
    print("  [q] Quit")
    print("═" * 52)

def get_document() -> str:
    print("\nPaste your document/text/code below.")
    print("When done, type END on a new line and press Enter:\n")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    return "\n".join(lines)

def main():
    print("\n🚀 Initializing Multi-Task GenAI System (Gemini)...")
    llm = get_llm()
    print("✅ Gemini LLM ready.\n")
    document = ""
    while True:
        print_menu()
        choice = input("Select a task: ").strip().lower()
        if choice == "q":
            print("\n👋 Goodbye!\n")
            break
        if choice not in TASK_REGISTRY:
            print("❌ Invalid choice. Try again.")
            continue
        if document:
            reuse = input("\nReuse previous document? (y/n): ").strip().lower()
            if reuse != "y":
                document = get_document()
        else:
            document = get_document()
        if not document.strip():
            print("⚠️  No document provided.")
            continue
        result = dispatch_task(choice, document, llm)
        print("\n" + "─" * 50)
        print("📄 RESULT:")
        print("─" * 50)
        print(result)
        print("─" * 50)
        save = input("\nSave result to file? (y/n): ").strip().lower()
        if save == "y":
            filename = f"output_{TASK_REGISTRY[choice]['key']}.txt"
            with open(filename, "w") as f:
                f.write(result)
            print(f"✅ Saved to {filename}")

if __name__ == "__main__":
    main()
