# !pip install langchain-openai langchain-community wikipedia
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_community.utilities import WikipediaAPIWrapper
from typing import Dict, Union, List
import re
import os
import json

# ==========================
# CONFIGURATION
# ==========================
os.environ["OPENAI_API_KEY"] = "api-key"

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
llm_ai = ChatOpenAI(model="gpt-4.1-nano")

# ==========================
# MATH TOOLS
# ==========================

@tool
def add_numbers(inputs: str) -> dict:
    """Adds numbers from input string and returns sum."""
    numbers = [int(num) for num in re.findall(r'\d+', inputs)]
    return {"result": sum(numbers)}

@tool
def add_numbers_with_options(numbers: List[float], absolute: bool = False) -> float:
    """Adds numbers with option to use absolute values."""
    if absolute:
        numbers = [abs(n) for n in numbers]
    return sum(numbers)

@tool
def sum_numbers_with_complex_output(inputs: str) -> Dict[str, Union[float, str]]:
    """Extracts and sums integers and decimals from input string."""
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
    """Extracts and sums numbers from text input."""
    numbers = [int(num) for num in re.findall(r'\d+', inputs)]
    return sum(numbers)

@tool
def subtract_numbers(inputs: str) -> dict:
    """Subtracts numbers sequentially (first number minus subsequent numbers)."""
    numbers = [int(num) for num in inputs.replace(",", "").split() if num.isdigit()]
    if not numbers:
        return {"result": 0}
    
    result = numbers[0]
    for num in numbers[1:]:
        result -= num
    return {"result": result}

@tool
def multiply_numbers(inputs: str) -> dict:
    """Multiplies numbers from input string."""
    numbers = [int(num) for num in inputs.replace(",", "").split() if num.isdigit()]
    if not numbers:
        return {"result": 1}
    
    result = 1
    for num in numbers:
        result *= num
    return {"result": result}

@tool
def divide_numbers(inputs: str) -> dict:
    """Divides numbers sequentially (first number divided by subsequent numbers)."""
    numbers = [int(num) for num in inputs.replace(",", "").split() if num.isdigit()]
    if not numbers:
        return {"result": 0}
    
    result = numbers[0]
    for num in numbers[1:]:
        if num == 0:
            return {"result": "Error: Division by zero"}
        result /= num
    return {"result": result}

@tool
def new_subtract_numbers(inputs: str) -> dict:
    """Alternative subtraction implementation."""
    numbers = [int(num) for num in inputs.replace(",", "").split() if num.isdigit()]
    if not numbers:
        return {"result": 0}
    
    result = numbers[0]
    for num in numbers[1:]:
        result -= num
    return {"result": result}

# ==========================
# WIKIPEDIA TOOL
# ==========================

@tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for factual information."""
    wiki = WikipediaAPIWrapper()
    return wiki.run(query)

# ==========================
# AGENT SETUP
# ==========================

# Basic math tools
basic_tools = [add_numbers, subtract_numbers, multiply_numbers, divide_numbers]

# Updated tools with new subtraction
updated_tools = [add_numbers, new_subtract_numbers, multiply_numbers, divide_numbers]

# Tools with Wikipedia
wiki_tools = [add_numbers, new_subtract_numbers, multiply_numbers, divide_numbers, search_wikipedia]

# Create agents
math_agent = create_react_agent(
    model=llm,
    tools=basic_tools,
    prompt="You are a helpful mathematical assistant. Use tools precisely."
)

math_agent_new = create_react_agent(
    model=llm,
    tools=updated_tools,
    prompt="You are a helpful mathematical assistant. Use tools precisely."
)

math_agent_updated = create_react_agent(
    model=llm,
    tools=wiki_tools,
    prompt="You are a helpful assistant for math and information lookup."
)

# Traditional LangChain agents
add_tool = Tool(name="AddTool", func=add_numbers, description="Adds a list of numbers and returns the result.")

traditional_agent = initialize_agent(
    [add_tool], llm, agent="zero-shot-react-description", verbose=True, handle_parsing_errors=True
)

agent_2 = initialize_agent(
    [sum_numbers_from_text], llm, agent="structured-chat-zero-shot-react-description", 
    verbose=True, handle_parsing_errors=True
)

agent_3 = initialize_agent(
    [sum_numbers_with_complex_output], llm_ai, agent="openai-functions", 
    verbose=True, handle_parsing_errors=True
)

agent_openai = initialize_agent(
    [add_numbers_with_options], llm_ai, agent="openai-functions", verbose=True
)

# ==========================
# TEST FUNCTIONS 
# ==========================

def run_original_tests():
    """Run all the original test cases from your code"""
    print("=== ORIGINAL TESTS ===")
    
    # Test 1: Tool metadata
    print("\n--- Test 1: Tool Metadata ---")
    print("Name:", add_numbers.name)
    print("Description:", add_numbers.description)
    print("Args:", add_numbers.args)
    
    # Test 2: Individual tool invocation
    print("\n--- Test 2: Individual Tool Test ---")
    test_input = "what is the sum between 10, 20 and 30" 
    print("Input:", test_input)
    print("Output:", add_numbers.invoke(test_input))
    
    # Test 3: add_numbers_with_options
    print("\n--- Test 3: add_numbers_with_options ---")
    print("Args Schema:", add_numbers_with_options.args_schema.schema())
    print("Normal:", add_numbers_with_options.invoke({"numbers": [-1.1, -2.1, -3.0], "absolute": False}))
    print("Absolute:", add_numbers_with_options.invoke({"numbers": [-1.1, -2.1, -3.0], "absolute": True}))
    
    # Test 4: subtract_numbers tool details
    print("\n--- Test 4: Subtract Numbers Tool ---")
    print("Name:", subtract_numbers.name)
    print("Description:", subtract_numbers.description)
    print("Args:", subtract_numbers.args)
    test_input = "10 20 30 and four a b"
    print("Calling with:", test_input)
    print("Result:", subtract_numbers.invoke(test_input))
    
    # Test 5: Multiply and Divide tools directly
    print("\n--- Test 5: Multiply & Divide Direct ---")
    multiply_test_input = "2, 3, and four"
    multiply_result = multiply_numbers.invoke(multiply_test_input)
    print("Multiply Input:", multiply_test_input)
    print("Multiply Output:", multiply_result)
    
    divide_test_input = "100, 5, two"
    divide_result = divide_numbers.invoke(divide_test_input)
    print("Divide Input:", divide_test_input)
    print("Divide Output:", divide_result)

def run_agent_tests():
    """Run agent-based tests"""
    print("\n=== AGENT TESTS ===")
    
    # Test GDP calculation
    print("\n--- GDP Calculation Test ---")
    try:
        response = traditional_agent.invoke(
            "In 2023, the US GDP was approximately $27.72 trillion, while Canada's was around $2.14 trillion and Mexico's was about $1.79 trillion what is the total."
        )
        print("GDP Result:", response)
    except Exception as e:
        print("GDP Test Error:", e)
    
    # Test basic addition
    print("\n--- Basic Addition Test ---")
    try:
        response = traditional_agent.invoke({"input": "Add 10, 20, two and 30"})
        print("Addition Result:", response)
    except Exception as e:
        print("Addition Test Error:", e)
    
    # Test sum_numbers_from_text
    print("\n--- Sum Numbers Test ---")
    try:
        response = agent_2.invoke({"input": "Add 10, 20 and 30"})
        print("Sum Result:", response)
    except Exception as e:
        print("Sum Test Error:", e)
    
    # Test complex output
    print("\n--- Complex Output Test ---")
    try:
        response = agent_3.invoke({"input": "Add 10, 20 and 30"})
        print("Complex Output Result:", response)
    except Exception as e:
        print("Complex Output Error:", e)
    
    # Test with options
    print("\n--- Options Test ---")
    try:
        response = agent_openai.invoke({"input": "Add -10, -20, and -30 using absolute values."})
        print("Options Result:", response)
    except Exception as e:
        print("Options Error:", e)

def run_react_agent_tests():
    """Run LangGraph react agent tests"""
    print("\n=== LANGGRAPH REACT AGENT TESTS ===")
    
    # Test division
    print("\n--- Division Test ---")
    try:
        response = math_agent.invoke({"messages": [("human", "What is 25 divided by 4?")]})
        final_answer = response["messages"][-1].content
        print("Division Result:", final_answer)
    except Exception as e:
        print("Division Error:", e)
    
    # Test subtraction
    print("\n--- Subtraction Test ---")
    try:
        response_2 = math_agent.invoke({"messages": [("human", "Subtract 100, 20, and 10.")]})
        if len(response_2["messages"]) >= 2:
            final_answer_2 = response_2["messages"][-2].content
            print("Subtraction Result:", final_answer_2)
    except Exception as e:
        print("Subtraction Error:", e)
    
    # Test multiplication
    print("\n--- Multiplication Test ---")
    try:
        response = math_agent.invoke({"messages": [("human", "Multiply 2, 3, and four.")]})
        print("Multiplication Result:", response["messages"][-1].content)
    except Exception as e:
        print("Multiplication Error:", e)
    
    # Test division
    print("\n--- Division Test ---")
    try:
        response = math_agent.invoke({"messages": [("human", "Divide 100 by 5 and then by 2.")]})
        print("Division Result:", response["messages"][-1].content)
    except Exception as e:
        print("Division Error:", e)

def run_structured_test_cases():
    """Run structured test cases"""
    print("\n=== STRUCTURED TEST CASES ===")
    
    test_cases = [
        {
            "query": "Subtract 100, 20, and 10.",
            "expected": {"result": 70},
            "description": "Testing subtraction tool with sequential subtraction."
        },
        {
            "query": "Multiply 2, 3, and 4.",
            "expected": {"result": 24},
            "description": "Testing multiplication tool for a list of numbers."
        },
        {
            "query": "Divide 100 by 5 and then by 2.",
            "expected": {"result": 10.0},
            "description": "Testing division tool with sequential division."
        },
        {
            "query": "Subtract 50 from 20.",
            "expected": {"result": -30},
            "description": "Testing subtraction tool with negative results."
        }
    ]
    
    correct_tasks = []
    
    for index, test in enumerate(test_cases, start=1):
        print(f"\n--- Test Case {index}: {test['description']} ---")
        print(f"Query: {test['query']}")
        
        try:
            response = math_agent_new.invoke({"messages": [("human", test["query"])]})
            
            tool_message = None
            for msg in response["messages"]:
                if hasattr(msg, 'name') and msg.name in ['add_numbers', 'new_subtract_numbers', 'multiply_numbers', 'divide_numbers']:
                    tool_message = msg
                    break
            
            if tool_message:
                tool_result = json.loads(tool_message.content)["result"]
                expected_result = test["expected"]["result"]
                
                print(f"Tool Result: {tool_result}")
                print(f"Expected Result: {expected_result}")
                
                if tool_result == expected_result:
                    print("✅ Test Passed")
                    correct_tasks.append(test["description"])
                else:
                    print("❌ Test Failed")
            else:
                print("❌ No tool was called")
                
        except Exception as e:
            print(f"❌ Error during test: {e}")
    
    print(f"\nCorrectly passed tests: {len(correct_tasks)}/{len(test_cases)}")
    for task in correct_tasks:
        print(f"  ✅ {task}")

def run_wikipedia_tests():
    """Run Wikipedia integration tests"""
    print("\n=== WIKIPEDIA TESTS ===")
    
    # Test Wikipedia directly
    print("\n--- Direct Wikipedia Test ---")
    wiki_result = search_wikipedia.invoke("What is tool calling?")
    print("Wikipedia Result (first 200 chars):", wiki_result[:200] + "...")
    
    # Test agent with Wikipedia
    print("\n--- Wikipedia Agent Test ---")
    query = "What is the population of Canada? Multiply it by 0.75"
    
    try:
        response = math_agent_updated.invoke({"messages": [("human", query)]})
        
        print("\nMessage sequence:")
        for i, msg in enumerate(response["messages"]):
            print(f"\n--- Message {i+1} ---")
            print(f"Type: {type(msg).__name__}")
            if hasattr(msg, 'content'):
                print(f"Content: {msg.content[:100]}...")
            if hasattr(msg, 'name'):
                print(f"Name: {msg.name}")
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                print(f"Tool calls: {msg.tool_calls}")
                
    except Exception as e:
        print(f"Wikipedia Agent Error: {e}")

# ==========================
# MAIN EXECUTION
# ==========================

def main():
    """Main function to run all tests"""
    print("🤖 COMPREHENSIVE MATH ASSISTANT TEST SUITE")
    print("=" * 60)
    
    # Run all test categories
    run_original_tests()
    run_agent_tests()
    run_react_agent_tests()
    run_structured_test_cases()
    run_wikipedia_tests()
    
    print("\n" + "=" * 60)
    print("🎯 ALL ORIGINAL TESTS PRESERVED AND EXECUTED")

if __name__ == "__main__":

    main()
