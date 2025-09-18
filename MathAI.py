# main.py
import os
import re
from typing import Dict, Union, List
from langgraph.prebuilt import create_react_agent
from langchain.agents import initialize_agent, Tool
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# ==========================
# CONFIGURAȚIE DEEPSEEK
# ==========================
os.environ["OPENAI_API_KEY"] = "api-key"  
# ia cheia ta din https://platform.openai.com/account/api-keys

llm = ChatOpenAI(
    model="gpt-4.1-mini",  # model gratuit și rapid
    temperature=0
)



# ==========================
# DEFINIRE TOOLS
# ==========================

@tool
def add_numbers(inputs: str) -> dict:
    """Adună toate numerele dintr-un string."""
    numbers = [int(num) for num in re.findall(r'\d+', inputs)]
    return {"result": sum(numbers)}

@tool
def add_numbers_with_options(numbers: List[float], absolute: bool = False) -> float:
    """Adună o listă de numere. Dacă absolute=True, folosește valorile absolute."""
    if absolute:
        numbers = [abs(n) for n in numbers]
    return sum(numbers)

@tool
def sum_numbers_with_complex_output(inputs: str) -> Dict[str, Union[float, str]]:
    """Extrage și adună toate numerele întregi sau cu zecimale dintr-un string."""
    matches = re.findall(r'-?\d+(?:\.\d+)?', inputs)
    if not matches:
        return {"result": "No numbers found in input."}
    try:
        numbers = [float(num) for num in matches]
        return {"result": sum(numbers)}
    except Exception as e:
        return {"result": f"Error during summation: {str(e)}"}

@tool
def sum_numbers_from_text(inputs: str) -> float:
    """Extrage numerele dintr-un text și returnează suma lor."""
    numbers = [int(num) for num in re.findall(r'\d+', inputs)]
    return sum(numbers)

# ==========================
# CREARE AGENT + TESTE
# ==========================

add_tool = Tool(
    name="AddTool",
    func=add_numbers,
    description="Adds a list of numbers and returns the result."
)

# Agent 1 – cu tool-ul de bază
agent = initialize_agent([add_tool], llm, agent="zero-shot-react-description", verbose=True, handle_parsing_errors=True)
print("\n=== Test 1 ===")
print(agent.invoke("In 2023, the US GDP was approximately $27.72 trillion, while Canada's was around $2.14 trillion and Mexico's was about $1.79 trillion. What is the total?"))

# Agent 2 – cu tool simplu
agent_2 = initialize_agent([sum_numbers_from_text], llm, agent="structured-chat-zero-shot-react-description", verbose=True, handle_parsing_errors=True)
print("\n=== Test 2 ===")
print(agent_2.invoke({"input": "Add 10, 20 and 30"}))

# Agent 3 – cu GPT-4.1-nano
llm_ai = ChatOpenAI(model="gpt-4.1-nano")
agent_3 = initialize_agent([sum_numbers_with_complex_output], llm_ai, agent="openai-functions", verbose=True, handle_parsing_errors=True)
print("\n=== Test 3 ===")
print(agent_3.invoke({"input": "Add 10, 20 and 30"}))

# Agent 4 – cu absolute values
agent_4 = initialize_agent([add_numbers_with_options], llm, agent="structured-chat-zero-shot-react-description", verbose=True)
print("\n=== Test 4 ===")
print(agent_4.invoke({"input": "Add -10, -20, and -30 using absolute values."}))

# Agent 5 – OpenAI functions
agent_openai = initialize_agent([add_numbers_with_options], llm_ai, agent="openai-functions", verbose=True)
print("\n=== Test 5 ===")
print(agent_openai.invoke({"input": "Add -10, -20, and -30 using absolute values."}))
 
 