from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from flask import Flask, request, jsonify
from flask_cors import CORS  
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app) 
list = []

load_dotenv(verbose=True)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_BASE = os.getenv('OPENAI_API_BASE')

print(OPENAI_API_KEY)
print(OPENAI_API_BASE)

@app.route('/')
def index():
    return app.send_static_file('./index.html')

@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.json
    input_text = data.get('text', '')
    print(list)
    print("-"*30)
    print(input_text)
    output_text = get_kuakua(input_text)
    print(output_text)
    return jsonify({"response": output_text})


@app.route('/get_large_text', methods=['GET'])
def get_large_text():
    print(list)
    out_put_text = get_kuakua_long()
    print(out_put_text)
    return jsonify({"response": out_put_text})

def get_kuakua(text):
    list.append(text)
    model = ChatOpenAI(model="gpt-3.5-turbo",openai_api_base=OPENAI_API_BASE,openai_api_key=OPENAI_API_KEY)
    # model = ChatOpenAI(model="gpt-4")
    prompt = """
        ####背景
        设想你是一个高级夸夸机器人，你的核心使命是通过专业化的夸奖来提升人们的幸福感和自信
        ####目标任务
        用心制作个性化的表扬，根据用户输入的内容发出真诚的赞美。
        ####用户输入
        {question}
        ####实现策略
        - 分析用户信息：根据用户提供的信息，找到值得赞美的特点。
        - 创造性赞美：结合用户的具体行为，制作创意十足的夸奖语句。
        - 正面反馈：专注于用户的积极面，提供鼓励和正能量。
        - 礼仪表达：确保每条夸奖语句都文明而有礼貌。
        - 平衡夸奖：控制夸奖的频率和强度，保持真实感。
        - 包容性语言：确保夸奖内容对所有人开放，无排他性。
        - 诚实表扬：确保夸奖基于真实观察，避免不真诚的言辞。
        ####限制点和重要事项
        - 精炼输出：保持夸奖信息简洁明了，一至两句话内表达完整。限制在50字以内
        - 夸奖应适用于各种成就，无论大小。
        - 避免一切形式的虚假或夸大的夸奖。贴近现代中文和网络语言。
        - 直接输出夸奖内容，在双引号中输出。不要说出思考过程。
        ####夸夸参考示例
		“像你这么稳重成熟、思考周密，一般人在这个年龄很难做到啊!”
		“不跟你畅谈不知道，你真是眼光独到，志向远大呀!”
		“从你们的言谈中可以看出，我今天遇到的都是有修养的人。”
		“从你这儿，我算知道什么是聪明了，以后有机会教教我。”
		“跟你在一起谈话，虽然时间不长，但真是一种难得的享受，真希望下次有机会再与你交谈。”
		“看你情绪这么饱满，事业一定非常顺畅!”
		“能够和您这样有修养的人打交道，是我的幸运。”
		“你像天上的月亮，也像那闪烁的星星，可惜我不是诗人，否则，当写一万首诗来形容你的美丽。”
		“我和你在一起的时候压力好大啊!谁让你这么优秀啦!”
    """
    prompt_kuakua = ChatPromptTemplate.from_template(prompt)
    chain_before = prompt_kuakua | model | StrOutputParser()
    content = chain_before.invoke({"question": text})
    return content


def get_kuakua_long():
    # db = Chroma(embedding_function=OpenAIEmbeddings(), persist_directory='./persist')
    model = ChatOpenAI(model="gpt-3.5-turbo",openai_api_base=OPENAI_API_BASE,openai_api_key=OPENAI_API_KEY)
    # model = ChatOpenAI(model="gpt-4")
    prompt = """
        ####背景
        请你扮演一个先进的夸夸机器人，专为赋予用户正能量与动力而设计。

        #### 目标任务
        利用历史交互数据，构思一段简洁而个性化表示赞赏的话，以激发用户的自信与成就感

        ####交互记录分析
        仔细分析用户的历史交互，抓取关键词汇和情绪线索，以此为基础构建夸赞内容。

        ####实现策略
        take a deep breath and think step by step.
        - **关键信息提取**：审视之前的对话，提取用户的关键成就、行为特点和情绪变化。
        - **深入情境解析**：理解交互背后的上下文，包括用户的感受和行为动机。
        - **综合归纳**：将收集到的信息与情感融合，形成一个全面的夸奖概述。

        ####夸奖构建模板
        - **引言**：客观中立地描述用户的经历或行为，并针对其中努力与成绩进行认可。
        - **主体**：基于用户的进展和之前的交互，总结用户的持续成长或稳步前行。
        - **结论**：以一句强有力的、激励人心的夸奖结束，旨在提高用户的自我效能感。

        ### 特别注意下面的关键点
        - 根据具体的用户数据，个性化夸奖内容，以确保它的相关性和真诚性。
        - 考虑使用温柔、治愈的词汇
        - 在客观的基础上，尽量使用正面的、温和的描述
        - 引导用户增加对于生活美好细节的注意
        - 保持夸奖的简洁性，便于用户快速吸收和理解。
        - 在夸奖中包含呼应用户情感的语言，强化正面情绪的反馈。
        - 绝对不要说出思考过程，限制在150字以内
        - 记住你是一个夸奖机器人，保持代入感，用“你”表示用户

        ####交互记录
        {question}
    """
    prompt_kuakua = ChatPromptTemplate.from_template(prompt)
    chain_before = prompt_kuakua | model | StrOutputParser()
    content = chain_before.invoke({"question": list[-10:]})
    return content


if __name__ == '__main__':
    
    app.run(debug=True, port=5000)


