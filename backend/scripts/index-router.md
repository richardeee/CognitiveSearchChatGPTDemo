```python
from llama_index.tools.query_engine import QueryEngineTool

query_engine_tools = []

# add vector index tools
for product in products:
    index = vector_indices[product]
    summary = index_summaries[product]
    
    query_engine = index.as_query_engine(service_context=service_context)
    vector_tool = QueryEngineTool.from_defaults(query_engine, description=summary)
    query_engine_tools.append(vector_tool)


# add graph tool
graph_description = (
    "This tool contains information about multiple products. "
    "Use this tool if you want to compare multiple products. "
)
graph_tool = QueryEngineTool.from_defaults(graph_query_engine, description=graph_description)
query_engine_tools.append(graph_tool)
```