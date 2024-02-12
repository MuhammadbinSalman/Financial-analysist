import streamlit as st
import requests
import json
from json import dumps
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os
import time
from openai.types.chat.chat_completion import ChatCompletion
 

_ : bool = load_dotenv(find_dotenv())
FMP_API_KEY = os.environ["FMP_API_KEY"]  # read local .env file
client : OpenAI = OpenAI() 

# Define financial statement functions
def get_income_statement(ticker, period, limit):
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return json.dumps(response.json())

def get_balance_sheet(ticker, period, limit):
  return "Hello World"

def get_cash_flow_statement(ticker, period, limit):
  return "Hello World" 

def get_key_metrics(ticker, period, limit):
  return "Hello World"

def get_financial_ratios(ticker, period, limit):
  return "Hello World"

def get_financial_growth(ticker, period, limit):
  return "Hello World"

available_functions = {
    "get_income_statement": get_income_statement,
    "get_balance_sheet": get_balance_sheet,
    "get_cash_flow_statement": get_cash_flow_statement,
    "get_key_metrics": get_key_metrics,
    "get_financial_ratios": get_cash_flow_statement,
    "get_financial_growth": get_financial_ratios
}

def run_assistant(user_message):
    assistant = client.beta.assistants.create(
        instructions="Act as a financial analyst by accessing detailed financial data through the Financial Modeling Prep API. Your capabilities include analyzing key metrics, comprehensive financial statements, vital financial ratios, and tracking financial growth trends. ",
        model="gpt-4-1106-preview",
    tools=[
            {"type": "function", "function": {"name": "get_income_statement", "parameters": {"type": "object", "properties": {"ticker": {"type": "string"}, "period": {"type": "string"}, "limit": {"type": "integer"}}}}},
            # same for the rest of the financial functions
          ])
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
    #   content=user_message
    )
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id) 
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    run_steps = client.beta.threads.runs.steps.list(thread_id=thread.id, run_id=run.id) 