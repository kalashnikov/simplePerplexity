from openai import OpenAI
import os,requests,json
from bs4 import BeautifulSoup

## 在platform.openai.com申请
os.environ["OPENAI_API_KEY"] = "sk-"

## 在serper.dev申请
XAPIKEY = "xxx"
## 1. 问题的举一反三
def askMoreQuestion(question):
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "根據原始問題提出3個相關且蘇格拉底式的進一步問題，注意問題不要重復，有價值的，可以跟進，並寫出的每個問題不超過 20 個字。"},
        {"role": "user", "content": question}
    ]
    )

    print(completion.choices[0].message.content)

## 2. 重写问题
def reWriteQuestion(question):
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "退一步思考，理解問題後，將問題轉化成2個可以用於搜索引擎搜索的關鍵詞,使用空格隔開,以便我可以用於google進行搜索.只需要說關鍵詞，不需要說其他內容"},
        {"role": "user", "content": question}
    ]
    )

    print(completion.choices[0].message.content)
    return(completion.choices[0].message.content)

## 3. 获取搜索引擎单页面结果(略)
def html_to_markdown(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功
        soup = BeautifulSoup(response.text, 'html.parser')

        markdown_content = ""

        # 抽取并转换标题
        if soup.title:
            markdown_content += f"# {soup.title.string}\n\n"

        # 抽取并转换段落
        for p in soup.find_all('p'):
            markdown_content += f"{p.get_text()}\n\n"

        return markdown_content
    except requests.RequestException as e:
        return f"Error: {e}"

## 4. 检索搜索引擎，并获得全文内容.
def searchWeb(keyword):
    url = "https://google.serper.dev/search"
    payload = json.dumps(
        [
        {
            "q": keyword,
            "num": 4
        }

        ]
    )
    headers = {
    'X-API-KEY': XAPIKEY,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    md = json.loads(response.text)
    for gg in (md):
        for item in gg['organic']:
            print(item['link'])
            completeContent = html_to_markdown(item['link'])
            if len(completeContent) > 0:
                aa.append(completeContent)
            else:
                aa.append("nothing")

## 检索答案合成
def AnswerGen(aa,question):
    realQuestion = """
使用提供的由三重引號引起來的文章來回答問題。 如果在文章中找不到答案，請寫“我找不到答案”。

\"\"\"{}\"\"\"
\"\"\"{}\"\"\"
\"\"\"{}\"\"\"

问题：{}
""".format(aa[0],aa[1],aa[2],question)
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "you are a helpful assistant"},
        {"role": "user", "content": realQuestion}
    ]
    )

    print(completion.choices[0].message.content)

aa = []

def main():
    question = input()
    print("下面重寫關鍵詞======")
    keyword = reWriteQuestion(question)
    print("下面進行web搜索得到答案======")
    searchWeb(keyword)
    print("下面生成合成內容======")
    AnswerGen(aa,question)
    print("下面生成3個新問題======")
    askMoreQuestion(question)

main()
