Claro! Aquí tienes un archivo `README.md` completo para tu proyecto, incluyendo la información sobre la clave de Gemini API.

---

# Agent Conversacional Bàsic amb LangGraph i Google Gemini

Aquest projecte demostra una implementació bàsica d'un agent conversacional utilitzant LangChain, LangGraph i el model de llenguatge Google Gemini. L'agent té una memòria simple, el que li permet recordar el context de la conversa anterior amb l'usuari.

## Característiques

*   **Integració amb Google Gemini:** Utilitza el model `gemini-pro` per generar respostes.
*   **Memòria Conversacional:** L'agent manté un historial dels missatges intercanviats, permetent respostes contextualment rellevants.
*   **Estructura amb LangGraph:** Utilitza LangGraph per definir el flux de l'agent i la gestió de l'estat.
*   **Fàcil d'Entendre:** Dissenyat com a punt de partida introductori per a LangChain/LangGraph.

## Requisits

*   Python 3.8+
*   Accés a l'API de Google Gemini (necessitaràs una `GOOGLE_API_KEY`).

## Instal·lació

1.  **Clona el repositori (o crea els fitxers):**

    ```bash
    git clone <URL_DEL_TEU_REPOSITORI>
    cd <NOM_DEL_REPOSITORI>
    ```

    (Si no tens un repositori, simplement crea el fitxer `__init__.py` amb el codi proporcionat i `README.md`)

2.  **Crea un entorn virtual (recomanat):**

    ```bash
    python -m venv venv
    source venv/bin/activate # En Linux/macOS
    # o `venv\Scripts\activate` en Windows
    ```

3.  **Instal·la les dependències:**

    ```bash
    pip install -U langchain langgraph langchain_google_genai python-dotenv
    ```
    (`python-dotenv` és per carregar la clau API des d'un fitxer `.env`)

## Configuració de l'API de Google Gemini

Per utilitzar Google Gemini, necessites una clau d'API. Pots obtenir-la des de [Google AI Studio](https://aistudio.google.com/app/apikey).

Un cop tinguis la teva clau, has de configurar-la com a variable d'entorn. La manera **recomanada** per a aquest projecte és utilitzar un fitxer `.env`:

1.  **Crea un fitxer anomenat `.env`** a l'arrel del teu projecte (al mateix directori que `__init__.py` o el teu script principal).
2.  **Afegeix la teva clau API** a aquest fitxer amb el format següent:

    ```
    GOOGLE_API_KEY="AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ```
    **Assegura't de substituir el valor d'exemple per la teva clau API real.**

    ⚠️ **IMPORTANT:** No comparteixis el teu fitxer `.env` ni la teva clau API públicament (per exemple, no el pugis a GitHub). Per això, el fitxer `.env` hauria d'estar al teu `.gitignore`.

## Ús

Per executar l'agent i començar a conversar:

1.  Assegura't que el teu entorn virtual estigui activat i les dependències instal·lades.
2.  Assegura't que el fitxer `.env` estigui correctament configurat amb la teva `GOOGLE_API_KEY`.
3.  Executa el script principal de Python:

    ```bash
    python __init__.py
    ```
    (Si has anomenat el teu fitxer amb un nom diferent, substitueix `__init__.py` pel nom corresponent).

L'agent iniciarà un bucle de conversa on podràs escriure els teus missatges. Escriu `exit` per acabar la conversa.

### Exemple d'Interacció

```
--- Agent Bàsic amb Gemini ---
Escriu el teu missatge. Escriu 'exit' per acabar.

Tu: Hola, com et dius?
-> Agent: Crido a Gemini...
-> Agent: Gemini ha respost.
Agent: Sóc un model de llenguatge gran, entrenat per Google.

Tu: Quina és la capital de Catalunya?
-> Agent: Crido a Gemini...
-> Agent: Gemini ha respost.
Agent: La capital de Catalunya és Barcelona.

Tu: I de quina província és capital?
-> Agent: Crido a Gemini...
-> Agent: Gemini ha respost.
Agent: Barcelona és la capital de la província de Barcelona.

Tu: exit
```

Observeu com l'agent "recorda" la pregunta anterior (`Quina és la capital de Catalunya?`) per respondre correctament a la pregunta "I de quina província és capital?". Això es deu a la gestió de la memòria conversacional mitjançant LangGraph.

## Estructura del Codi (Fitxer `__init__.py`)

El codi (`__init__.py`) es divideix en les següents seccions principals:

1.  **Definició de l'Estat (`AgentState`):** Una `TypedDict` que defineix la forma de l'estat que l'agent utilitza per mantenir la memòria (en aquest cas, una llista de `BaseMessage`).
2.  **Inicialització de l'LLM (`ChatGoogleGenerativeAI`):** Carrega el model de Google Gemini per ser utilitzat per l'agent.
3.  **Node Principal (`call_gemini_agent`):** Una funció Python que representa un "pas" dins del `LangGraph`. Rep l'estat actual, invoca Gemini amb l'historial de missatges i retorna un diccionari amb la resposta de Gemini per actualitzar l'estat.
4.  **Construcció del Graph (`StateGraph`):** Defineix el flux de control de l'agent. En aquest projecte introductori, el flux és lineal: de l'inici al node de Gemini, i d'allí al final.
5.  **Compilació del Graph:** Transforma la definició del graph en una aplicació executable.
6.  **Bucle d'Interacció:** Gestiona l'entrada de l'usuari, invoca el graph amb l'estat de la conversa i mostra la resposta de l'agent. És important destacar com l'estat es passa entre les invocacions per mantenir la memòria.

