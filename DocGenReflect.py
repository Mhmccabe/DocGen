from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

from rich import print

from dotenv import load_dotenv

load_dotenv()



OllamaLLM = ChatOllama(model="llama3.2", temperature=0.2)
#OllamaLLM = ChatOllama(model="deepseek-r1:14b", temperature=0.2)
#AnthopicLLM = ChatAnthropic(model_name="llama-3.2-90b-text-preview", temperature=0.7)
#OpenAILLM = ChatOpenAI(model="gpt-4o", temperature=0.7, max_tokens=None, max_retries=2)
#GroqLLM =  ChatGroq(model = "Deepseek-R1-Distill-llama-70b", temperature=0.7 )
#GroqLLM =  ChatGroq(model = "Deepseek-R1-Distill-llama-70b", temperature=0.7 )
GroqLLM =  ChatGroq(model = "llama-3.3-70b-Specdec", temperature=0.7 )

GenLLM = OllamaLLM
ReflextLLM = GroqLLM


#####  Generate ####################################################
## define the prompt

generatePrompt = ChatPromptTemplate(
    [
        (
            "system",
            """
            You are a technical author and architect, tasked with writing excellent component standards.
            Generate the best component standard possible for the user's request.
            
            you are creating the component standard to assist Solution architect to quickly understand of this component can meet to their functional and non-functional requirements
            if the user provides critique, respond with a revised version of the previous attempts.
            a component standard should follow the below layout and in markdown format.
            text that follow > are author notes and should be used to guide the content
            
            <component standard>
                 title 
                1. introduction
                    1.1 overview
                    
                    1.2 Technical Services 
                    
                    > the detailed technical  services should be presented in a table L1, L2, L3, Description with the definition               
                •	L1: The broadest category representing a high-level grouping of services.
                •	L2: enable the  L1 category, they represent key components or necessary services to deliver the L1 service.
                •	L3: More detailed services needed to support the  L2, offering a granular view of each L2 component.
                •	Description: Provide a detailed description of each L3 service.
                2. interfaces 
                    > list the interfaces that this component can interact with
                3. use cases  
                    2.1 Good use cases   > limit to use cases relevant to financial services 
                    2.2 bad use cases    > list use cases that this product should not be used for, keep this constrained to the financial services sector
                4. security best practice > encourage use to keep separation of concerns
                    3.1 roles   > list roles and descriptions
                    3.2 security    > over view of security stance , include a subsection that details the configuration setting to meet this defintion
                    3.2.1 data sensitivity > list the sensitivity of data that can be held, include a subsection that details the configuration setting to meet this defintion, produce a markdown table showing the setting
                5. Summary 
            </component standard>
            """,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

## generate the generate langchain
generateChain = generatePrompt | GenLLM

## define the question
OriginalDoc = ""
request = HumanMessage(
    content="Write a component standard on Grafana and prometheus"
)

## generate the request
print("\n📝 Generating document")
for chunk in generateChain.stream({"messages" : [request]}):
    #print( chunk.content, end="")
    print( ".", end="")
    OriginalDoc += chunk.content

with open("GeneratedDocs/OriginalDoc.md", "w", encoding="utf-8") as f:
    f.write(OriginalDoc)

#####  Reflect and improve ####################################################

reflectPrompt = ChatPromptTemplate(
    [
        (
            "system",
            """
            You are an expert Solution architect grading an component standard submission. Generate critique and recommendations for the user's submission. 
            Provide detailed recommendations, including requests for Technical accuracy, completeness, length, depth, style, etc.
            
            take into account the following principles
            
            - All internet access must go through the Inspection service and must not allow direct internet access
            - Pay close attention to separation of concerns to enhance security
            - include a recommendation of the sensitivity of data that can be held
            - Do not include code samples.
            - Do not include executive summary
            - the document should be focused towards architects
            - the document should be used to select the appropriate products for their designs
            - the document should refer to you own company 'PenCo', never simply refer to organisaion, always use the company name
            """
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

## generate the reflection


reflectChain = reflectPrompt | ReflextLLM

reflection = ""
## generate the reflection
print("\n📝 Reviewing document")
for chunk in reflectChain.stream({"messages" : [request, HumanMessage(content=OriginalDoc)]}):
    print( ".", end="")
    reflection += chunk.content
with open("GeneratedDocs/ReflectionDoc.md", "w", encoding="utf-8") as f:
    f.write(reflection)



finalDoc = ""
## re-generate taking into account he feedback
print("\n✍️ Editing document")
for chunk in generateChain.stream({"messages" :
    [
        request, 
        AIMessage(content=OriginalDoc),
        HumanMessage(content=reflection)
        ]}):
    finalDoc += chunk.content
    print( ".", end="")


with open("GeneratedDocs/finaldoc.md", "w", encoding="utf-8") as f:
    f.write(finalDoc)