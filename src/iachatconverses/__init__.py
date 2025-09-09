import os
from dotenv import load_dotenv
from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI # Importem Gemini
from langgraph.graph import StateGraph, START, END

# --- 1. Definir l'Estat de l'Agent (Sería com una pissarra) ---
# Definim l'estructura de l'estat de l'agent utilitzant TypedDict, aquesta serà la nostra "pissarra"
# on guardarem els missatges intercanviats entre l'usuari i l'agent.
class AgentState(TypedDict):
    messages: List[BaseMessage]

def call_gemini_agent(state: AgentState) -> AgentState:

    # Carrega les variables d'entorn des del fitxer .env.
    # Això permet mantenir les claus d'API i les cadenes de connexió fora del codi.
    load_dotenv()
    # Comprova si la clau de l'API de Google s'ha carregat correctament. Si no, llança un error.
    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError("No s'ha trobat la GOOGLE_API_KEY. Assegura't que el fitxer .env existeix i conté la clau.")
    
    # Inicialitza el model de llenguatge (LLM) que farem servir.
    # Model: "gemini-2.0-flash" és ràpid i eficient.
    # Temperature: 0 fa que les respostes del model siguin el més deterministes i factuals possible, sense creativitat.
    gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

    """
    Nodi que invoca el model Gemini amb l'historial de missatges actual
    i afegeix la resposta de Gemini a la llista de missatges.
    """
    print("-> Agent: Crido a Gemini...")
    
    # Agafa tots els missatges de l'estat actual.
    # Això és la "memòria" de la conversa.
    current_messages = state["messages"] 
    
    # Invoca el model Gemini amb els missatges actuals.
    response = gemini_llm.invoke(current_messages)
    
    print(f"-> Agent: Gemini ha respost.")
    print(f"*********************************************************************")
    print(f"Estat complert final despres invocacio: {state}")
    print(f"*********************************************************************")

    # Retorna un diccionari amb la clau 'messages'.
    # LangGraph (gràcies al seu reductor per defecte per a llistes)
    # afegirà automàticament aquesta nova 'response' a la llista 'messages' existent a l'estat.
    return {"messages": [response]}
# --- 4. Construir el Graph (El Flux de Treball) ---
# Un LangGraph defineix com es connecten els nodes i com flueix l'estat.
workflow = StateGraph(AgentState)

# Afegim el nostre únic node al flux de treball.
workflow.add_node("gemini_node", call_gemini_agent)

# Definim els "edges" (connexions) del nostre graph:
# - Comencem ('START') sempre anant al nostre 'gemini_node'.
# - Després que el 'gemini_node' ha processat, el flux de treball s'acaba ('END').
workflow.add_edge(START, "gemini_node")
workflow.add_edge("gemini_node", END)

# --- 5. Compilar el Graph ---
# Compilem el workflow per obtenir una aplicació executable.
app = workflow.compile()

# --- 6. Interacció amb l'Agent ---
print("--- Agent Bàsic amb Gemini ---")
print("Escriu el teu missatge. Escriu 'exit' per acabar.")

# Aquesta variable mantindrà l'estat de la conversa entre les teves interaccions.
# Comencem amb una llista de missatges buida.
current_conversation_state: AgentState = {"messages": []}

while True:
    user_input = input("\nTu: ")
    if user_input.lower() == 'exit':
        break

    # 1. Preparem l'entrada de l'usuari:
    # Cream un nou missatge d'usuari i l'afegim a l'estat actual.
    current_conversation_state["messages"].append(HumanMessage(content=user_input))
    
    # 2. Invoquem el graph:
    # Li passem l'estat de la conversa fins ara.
    # L'execució del graph (el nostre 'gemini_node') s'encarregarà de cridar a Gemini
    # i afegir la seva resposta a la llista de missatges.
    final_state_of_turn = app.invoke(current_conversation_state)

    print(f"Estat complert final despres invocacio: {final_state_of_turn}")  # Per depuració: mostra l'estat complet després de la invocació
    
    # 3. Actualitzem l'estat per al següent torn:
    # Assignem el nou estat retornat pel graph (que ja conté la resposta de Gemini)
    # a la nostra variable 'current_conversation_state'.
    current_conversation_state = final_state_of_turn
    
    # 4. Mostrem la resposta de Gemini a l'usuari:
    # La resposta de Gemini serà l'últim missatge a la llista 'messages'.
    if current_conversation_state["messages"]:
        gemini_response = current_conversation_state["messages"][-1]
        if isinstance(gemini_response, AIMessage):
            print(f"Agent: {gemini_response.content}")