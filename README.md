# Lou’s Tavern 🍻
### AI-Powered Learning Platform

Lou’s Tavern is a personal software development project exploring how Large Language Models (LLMs) can transform educational content into structured, study-ready materials.

By combining AI APIs with Python-based data processing, the project aims to simplify study preparation through automated content transformation, structured summaries, and flashcard generation.

## Overview

Preparing effective study materials can be time-consuming. Lou’s Tavern explores how generative AI and software automation can help streamline this process.

The platform is designed to process academic content, use LLMs to generate organized learning resources, and transform structured outputs into formats suitable for studying and reviewing.

## Features

- **LLM Integration:** Connects to language models through APIs to process educational content.
- **Structured Data Processing:** Uses JSON to organize and handle AI-generated information.
- **Automated Summaries:** Explores the generation of clear, structured summaries from academic material.
- **Flashcard Generation:** Supports the development of AI-assisted flashcards for active recall.
- **Document Generation:** Explores exporting structured learning content to Markdown and PDF.
- **Python Automation:** Uses Python to connect processing steps and automate parts of the workflow.

*Feature availability depends on the current implementation.*

## How It Works

The intended workflow is organized into the following stages:

1. **Input:** Provide academic content for processing.
2. **AI Processing:** Send relevant content to an LLM through an API.
3. **Structured Output:** Organize the generated information into JSON.
4. **Data Transformation:** Process and validate the structured data using Python.
5. **Study Materials:** Convert the processed content into formats such as summaries, flashcards, Markdown documents, or PDFs.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and data processing |
| LLM APIs | AI-powered content generation |
| JSON | Structured data representation |
| Markdown | Readable and portable study documents |
| Pandoc | Document conversion and PDF generation, where configured |
| HTML | Web content or interface components, where implemented |
| Visual Studio Code | Development environment |

## Project Structure

The repository structure may evolve as the project grows. The main components are intended to separate AI integration, data processing, and document generation.

```text
lou-tavern/
├── README.md
├── main.py
├── src/
│   ├── config.py (insert your API key)
│   ├── generator.py
│   └── textos_to_data.py
├── output/
│   └── pdf documents generated
└── documentos/
|   └── example pdf documents. you can make study-ready material out of them
└── multiple folders with various things (non relevant)
```

## Getting Started

### Prerequisites

Before running the project, make sure you have:

- Python installed.
- Access to a compatible LLM API, if required by the implementation.
- Pandoc installed if the PDF generation workflow relies on it.


## Example Workflow

A typical use case is transforming a section of academic material into organized study resources.

**Input:** Academic notes or course material.

**Processing:** AI-assisted content generation followed by Python-based data handling.

**Output:** Structured JSON containing learning content, potentially converted into summaries, flashcards, or study documents.

Add representative input and output examples to the `examples/` directory so that visitors can understand the results without needing to configure an API first.

## Learning Objectives

Lou’s Tavern provides an opportunity to explore:

- Integrating external AI services through APIs.
- Developing Python-based processing workflows.
- Working with structured data and JSON.
- Automating document generation.
- Applying generative AI to a practical educational use case.

## Project Status

**Status:** Personal development project — under development.

The scope and available features may change as development progresses.
