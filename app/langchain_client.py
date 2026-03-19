import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from utils.paths import SERVER_SCRIPT, PYTHON_EXE

def get_server_params() -> StdioServerParameters:
    """Configura e retorna os parametros do servidor MCP local."""
    return StdioServerParameters(command=PYTHON_EXE, args=[SERVER_SCRIPT])

def get_llm():
    """Inicializa a LLM Gemini."""
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("A variável de ambiente GOOGLE_API_KEY não está definida!")
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

async def process_query(agent, prompt: str):
    """Envia a query para a LLM e imprime a resposta."""
    print(f"\nInstrução enviada ao Gemini: '{prompt}'\n")
    resultado = await agent.ainvoke({"messages": [("user", prompt)]})
    print("\n=== Resposta Final do Gemini ===")
    print(resultado["messages"][-1].content)

async def main():
    print("Iniciando MCP Client e Agente Langchain com Gemini...")
    server_params = get_server_params()

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 1. Carrega as tools do MCP
            mcp_tools = await load_mcp_tools(session)        
            print(f"Ferramentas MCP carregadas: {[t.name for t in mcp_tools]}")

            try:
                # 2. Configura a LLM e o Agente
                llm = get_llm()
                agent = create_react_agent(llm, tools=mcp_tools)

                # 3. Executa as tarefas
                prompt1 = "Crie um novo usuário chamado Maicon, email maicon@tech.com com a descricao 'Especialista em desenvolvimento back end'."
                await process_query(agent, prompt1)
                
                
                prompt2 = "Busque por usuários que conhecem devops e desenvolvimento fullstack"
                await process_query(agent, prompt2)

                
                print("-" * 50)

            except ValueError as ve:
                print(f"\nERRO: {ve}")
            except Exception as e:
                print(f"\nERRO ao processar a instrução: {e}")

if __name__ == "__main__":
    load_dotenv()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nEncerrado pelo usuário.")
