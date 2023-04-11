import openai
from approaches.approach import Approach
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
from text import nonewlines

# Simple retrieve-then-read implementation, using the Cognitive Search and OpenAI APIs directly. It first retrieves
# top documents from search, then constructs a prompt with them, and then uses OpenAI to generate an completion 
# (answer) with that prompt.
class RetrieveThenReadApproach(Approach):

    template = \
"你是一个智能助手，可帮助SGS员工解决其食品行业检测问题。" + \
"使用'你'来指代提出问题的个人，即使他们用'我'提问。" + \
"仅使用以下来源中提供的数据回答以下问题。" + \
"每个源都有一个名称，后跟冒号和实际信息，始终包括您在响应中使用的每个事实的源名称。" + \
"如果您无法使用以下来源回答，请说您不知道。" + \
"""

###
问题: '荞麦、燕麦、藜麦是否可以进行GI测试?'

来源:
info1.txt: 荞麦燕麦藜麦本身GI值非常接近55，所以通过物理实验没办法精确计算最后的食物GI值..
info2.pdf: 如果客户想认证低GI食品，这个是没法保证的，必须做完临床试验后根据最终的结果判定.
info3.pdf: 认证中心也只以临床试验的报告作为参考标准.

Answer:
荞麦燕麦藜麦本身GI值非常接近55，所以通过物理实验没办法精确计算最后的食物GI值. [info1.txt] 如果客户想认证低GI食品，这个是没法保证的，必须做完临床试验后根据最终的结果判定 [info2.pdf]认证中心也只以临床试验的报告作为参考标准。.[info3.pdf].

###
问题: '{q}'?

来源:
{retrieved}

回答:
"""

    def __init__(self, search_client: SearchClient, openai_deployment: str, sourcepage_field: str, content_field: str):
        self.search_client = search_client
        self.openai_deployment = openai_deployment
        self.sourcepage_field = sourcepage_field
        self.content_field = content_field

    def run(self, q: str, overrides: dict) -> any:
        use_semantic_captions = True if overrides.get("semantic_captions") else False
        top = overrides.get("top") or 3
        exclude_category = overrides.get("exclude_category") or None
        filter = "category ne '{}'".format(exclude_category.replace("'", "''")) if exclude_category else None

        if overrides.get("semantic_ranker"):
            r = self.search_client.search(q, 
                                          filter=filter,
                                          query_type=QueryType.SEMANTIC, 
                                          query_language="en-US", 
                                          query_speller="lexicon", 
                                          semantic_configuration_name="default", 
                                          top=top, 
                                          query_caption="extractive|highlight-false" if use_semantic_captions else None)
        else:
            r = self.search_client.search(q, filter=filter, top=top)
        if use_semantic_captions:
            results = [doc[self.sourcepage_field] + ": " + nonewlines(" . ".join([c.text for c in doc['@search.captions']])) for doc in r]
        else:
            results = [doc[self.sourcepage_field] + ": " + nonewlines(doc[self.content_field]) for doc in r]
        content = "\n".join(results)

        prompt = (overrides.get("prompt_template") or self.template).format(q=q, retrieved=content)
        completion = openai.Completion.create(
            engine=self.openai_deployment, 
            prompt=prompt, 
            temperature=overrides.get("temperature") or 0.9, 
            max_tokens=1500, 
            n=1, 
            stop=["\n"])

        return {"data_points": results, "answer": completion.choices[0].text, "thoughts": f"Question:<br>{q}<br><br>Prompt:<br>" + prompt.replace('\n', '<br>')}
