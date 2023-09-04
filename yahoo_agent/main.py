from dotenv import load_dotenv
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
import streamlit as st
from tools import (
    StockPriceTool, 
    StockPercentageChangeTool, 
    StockGetBestPerformingTool,
    StockSMATool,
    StockEMATool,
)
from api_functions import get_stock_df


def main():
    load_dotenv(override=True)
    tools = [
        StockPriceTool(), 
        StockPercentageChangeTool(), 
        StockGetBestPerformingTool(),
        StockSMATool(),
        StockEMATool(),
    ]
    llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo-0613')
    open_ai_agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
    )
    st.title('Time Series Agent')
    query = st.text_input('Please enter your question here')
    if query:
        response = open_ai_agent.run(query)
        st.write(response)


if __name__ == "__main__":
    main()
    # df = get_stock_df('AAPL', 7)
    # print(df.head())
    # print(df.columns)
