from transformers import pipeline
from pprint import pprint
from pydantic import BaseModel, ConfigDict
from typing import Any, Callable, Generic, TypeVar
import json


# create a Model inherit BaseModel - fields and dataTypes
# Validate data, convert dataTypes automatically , Clear Errors

I = TypeVar("I")
O = TypeVar("O")
M = TypeVar("M")
class Runnable(BaseModel, [I, O]):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    pass

    def invoke(self, data: Any) -> Any:
        raise NotImplemented

    def __or__(self, other: Any) -> 'RunnableSequence':
        if isinstance(other, Runnable):
            return RunnableSequence(first=self, second=other)
        if callable(other):
            return RunnableSequence(first=self, second=RunnableLambda(func=other))
        return NotImplemented
    
    def __ror__(self, other: Any) -> Any:
        if callable(other): 
            return RunnableSequence(first=RunnableLambda(func=other), second=self)
        return NotImplemented
    
class RunnableLambda(Runnable, [I, O]):
    func: callable[[Any], Any]

    def invoke(self, data:Any) -> Any:
        return self.func(data)

class RunnableSequence(Runnable, [I, O], Generic[I, M , O]):
    self: Runnable
    second: Runnable

    def invoke(self, data: Any) -> Any: 
        return self.second.invoke(self.first.invoke(data))

class TicketInput(BaseModel):
    customer_id: int
    message: str

class ProcessedTicket(BaseModel):
    customer_id: int
    sentiment: str
    urgency: str
    summary: str
class SentimentAnalyser(Runnable):
    def invoke(self, ticket: TicketInput) -> dict:
        msg_lower = ticket.message.lower()
    
        # stimulate NLP sentiment
        sentiment = "negative" if "broken" in msg_lower or "angry" in msg_lower else "neutral"
        urgency = "high" if "broken" in msg_lower or "urgent" in msg_lower else "low"

        return {
            "customer_id": ticket.customer_id,
            "sentiment": sentiment,
            "urgency": urgency,
            "summary": ticket.message[:40]+ "..."
        } 

class TicketParser(Runnable):
    def invoke(self, raw_dict: dict) -> ProcessedTicket:
        return ProcessedTicket(*raw_dict)
    
    def route_ticket(ticket: ProcessedTicket) -> dict:
        destination = "engineering_team" if "high" in ticket.urgency else "generatic" 
        return{
            status: "routed",
            "assigned_to": destination,
            "ticket_details": ticket.model_dump()
        }

ticket_pipeline = SentimentAnalyser() | route_ticket






# _______ Not pydantic _____________
class SmolLLM:
    def __init__(self, model_name="HuggingFaceTB/SmolLM2-135M-Instruct"):
        print(f"Loading {model_name} into mempory. This may take a while....")
        self.pipe = pipeline("text-generation", model=model_name)
        print("Model loaded successfuly")

    def invoke(self, prompt:str) -> str:
        messages = [{"role": "user", "content": prompt}]
        output = self.pipe(messages, max_new_tokens=150)
        return output[0]['generated_text'][-1]['content'].strip()
    
class PromptTemplate:
    def __init__(self, template_str: str):
        self.template_str = template_str

    def format(self, **kwargs): # alla argument
        return self.template_str.format(**kwargs)
    def __or__(self, other): # overload
        if isinstance(other, SmolLLM):
            return LLMChain(prompt_template=self, llm=other)
        raise TypeError("A PromptTemplate can only be piped into LLMChain.")
    
class LLMChain:
    def __init__(self, prompt_template: PromptTemplate, llm=SmolLLM):
        self.prompt_template = prompt_template
        self.llm = llm

    def invoke(self, **kwargs):
        formatted_prompt = self.prompt_template.format(**kwargs)
        return self.llm.invoke(formatted_prompt)
    
llm = SmolLLM()

# skapa prompt
recipe_prompt = PromptTemplate(
    template_str="Give me a quick 2-steps recipe for a {dish} using only {ingredients_count} ingrediens")

recipe_chain = recipe_prompt | llm # here overload we __or__ -- langchain

result = recipe_chain.invoke(dish="cake", ingredients_count="three")

pprint(result)