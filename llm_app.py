def llm_app(topic):

 from langchain_core.prompts import PromptTemplate
 from langchain_groq import ChatGroq
 # 1. Initialize your LLM
 groq_api = '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'
 llm = ChatGroq(model='openai/gpt-oss-120b', api_key=groq_api, temperature=0.1)

 prompt=PromptTemplate(
    input_variables=['topic'],
    
    template='You are an agricultue expert.\
    provide five important lines coverng about {topic}.'
 )

 chain=prompt | llm

 #topic=input('Enter a topic')
 
 output=chain.invoke(topic)
 #print('Generated Blog Title ', output.content)
 return output.content

