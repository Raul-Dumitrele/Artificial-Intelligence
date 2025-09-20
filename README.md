# Math AI - Intelligent Math Assistant

## Title and Description
**Math AI** is an intelligent assistant for mathematical operations and information searches. It can perform addition, subtraction, multiplication, division, text summarization, and provides support through integration with Wikipedia. This project is intended for developers and users who want a fast and accurate tool for complex mathematical calculations and information.
## Features
- Basic math operations: addition, subtraction, multiplication, division
- Advanced operations: handling decimal and negative numbers
- Text analysis: extract and calculate numbers from text strings
- Wikipedia integration for factual information
- Automated testing with dedicated functions for each agent type
- Modular agents: you can add, remove or modify tools without affecting the operation
## Appendix

Notes for developers: OPENAI_API_KEY setting is required.

The traditional_agent agent for simple calculations, math_agent_updated for complex operations and Wikipedia integration.

Limitations: does not support fractions or division by zero (returns error).
## Contributing

Contributions are welcome!

Fork repository

Create a branch (git checkout -b feature/xyz)

Commit changes (git commit -m 'Add feature')

Push branch (git push origin feature/xyz)

Open a Pull Request
## Demo

from math_ai import math_agent
response = math_agent.invoke({"messages": [("human", "Add 10, 20, 30")]})
print(response)

## Documentation

All functions and agents are documented with docstrings and code examples.

Environment Variables

OPENAI_API_KEY: API key for OpenAI

Optional: MODEL_NAME for choosing the GPT model
## FAQ

#### Can I use Math AI without internet?

No, because the OpenAI API requires a connection.

#### What happens if a number is not recognized?

It is ignored and the calculation continues with the remaining valid numbers.
## Authon Name:

[Raul Dumitrele](https://github.com/Raul-Dumitrele)

