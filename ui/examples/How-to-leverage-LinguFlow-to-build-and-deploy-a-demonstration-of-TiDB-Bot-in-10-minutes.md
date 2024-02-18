# How to leverage LinguFlow to build and deploy a demonstration of TiDB Bot in 10 minutes

## 1. Prerequisites

### 1.1 What You Need

- Setting up LinguFlow in your local environment
- Getting an OpenAI API key
- Setting up Google custom search API and getting a key
- Better to have
  - Knowledge of Langchain core modules about prompts and models

### 1.2 Limitation

- In this example, we will use `GoogleSearch` block as a simplified retrieval for demonstration.
- This is just a demonstration without chat session management and revision.
- Only LLM from OpenAI is provided now. 

## 2. Designing the Business Logic of TiDB Bot Demonstration

The business logic shows as follows:

- Judge whether the question is related to TiDB
  - If it is not related to TiDB, refuse to answer it politely.
  - Otherwise, retrieve the corpus related to the question and answer it finally

> Notes:
> - Usually the best practice is to use RAG for the judging block and the refusing block too. 

## 3. Building the TiDB Bot Demonstration in LinguFlow

### 3.1 Normal procedure

What you should do is to implement the business logic in the above section block by block according to your intuition.

Or you can do as the following section and rea