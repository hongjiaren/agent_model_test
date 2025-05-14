import requests
import re
import time
import pandas as pd
import json
from datetime import datetime
from open_client import create_local_qwen_client, get_answer_async, get_answer_async_reasoning, create_qwen_4b_client, create_qwen_72b_client, create_tars_67b_client
GPT4O_ENDPOINT = "https://szzn10.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-10-21"
GPT4_1_ENDPOINT = "https://szzn7.openai.azure.com/openai/deployments/gpt-4.1/chat/completions?api-version=2025-01-01-preview"
import asyncio
step_split_prompt = """
你是一个步骤规划的专家，请根据用户输入的query，结合相关app的条件知识，拆解出满足用户需求的步骤。

## 目标
今天是{date}，星期{week}。根据用户输入，严格按以下流程生成操作步骤：
- 第一阶段：基于补充知识和历史信息生成最小可行操作路径。补充知识中使用字典结构描述，字典key是根结点，value是根结点下的子节点，同一个value里面的元素在页面上是同一级的，{"a": {"b": [], "c": []}, "d": {"f": []}}中a和d同级，b c属于a的下一级，和d也不同级。路径规划要求：
   - 必须从根节点开始，作为第一步操作（如“打开软件”、“进入网页”），注意不要修改根结点的描述。例如，根结点是打开xxx，不要改成启动xxx。
   - 逐层向下选择子节点，每一步均需基于当前节点和用户需求，选择逻辑最简且连续的操作路径。
   - 当前步骤和补充知识中的节点内容完全一致时，直接引用完整的节点内容，内容中的形参占位符（如<参数x>，<参数y>等）保持原样，不作替换。注意，<参数x>中的x要和补充知识中的保持一致，不要对参数的编号进行修改，不要编纂一个新的编号。
   - 如果已经完成了用户所有的意图，但是没有走到叶子节点，立即停止向下探索，返回规划好的步骤。并不是每一个用户的query都需要完全走到叶子节点。
   - 如果到达了叶子节点，完成了用户意图的一部分，但是剩余部分意图在另外的分支上。这种情况需要重新回到根节点（如“打开软件”、“进入网页”），对未完成的意图进行新的规划。
   - 当出现多个分支时，选择符合用户需求且逻辑连贯的路径，确保各步骤之间有明确的先后顺序。
   - 如果输入内容在补充知识中没有相关路径实现，请参照补充知识形式，但不受其路径影响，按照自己的理解进行拆解，注意不要丢失用户输入的关键信息。
   - 路径规划过程应确保关键节点不缺失，且路径中不出现重复或冗余操作，严格按照用户操作边界拆解。
   - 循环操作（如多选成员或者循环发送信息）保持一条步骤即可，不要拆分为多个步骤，例如钉钉给xxx发送消息，你好和你吃饭了吗。只需要输出一条 '发送个人消息<参数x>'。

- 第二阶段：反思检查: 在生成具体的步骤之后, 需进行以下检查：
    - 拆解完的步骤是连贯性和具有操作可行性。确保拆解完的步骤不存在缺失必要节点，如果两个节点之间无法直接连通，可以回到根节点，开启一个新的步骤接在原始步骤之后。
    - 拆解完的步骤内容是完全基于用户输入的。补充知识中的节点内容是起到辅助作用，要根据实际情况对节点内容进行修改。
    - 拆解完的步骤完全满足用户的意图，没有丢失用户输入的关键信息。如果用户输入内容在补充知识中没有相关路径实现，请参照补充知识形式，但不受其路径影响，按照自己的理解进行拆解，注意也不要丢失用户输入的关键信息。
    - 每个步骤中保留形参占位符（如<参数x>，<参数y>），不根据用户输入进行实际替换。注意，<参数x>中的x要和补充知识中的保持一致，不要对参数的编号进行修改，不要编纂一个新的编号。



## 输出格式
输出应严格按照如下 JSON 格式，仅包含生成的操作步骤，步骤中的形参占位符（如<参数1>，<参数2>等）保持原样，不作替换：
```json
{
  "步骤输出": ["xxx<参数x>","yyy<参数x>","zzz"]
}
```

## 注意事项
1. 输出必须严格采用补充知识中的节点内容，形参占位符不要替换，不改动语句顺序及空格格式。遇到<参数x>这种形参占位符一定要保留，不要根据用户query做任何的替换。
2、如果输入内容在补充知识中没有相关路径实现，请参照补充知识形式，但不受其路径影响，按照自己的理解进行拆解，注意也不要丢失用户输入的关键信息。
3、补充知识中的节点内容是起到辅助作用，实际用户真实意图的优先级是最高的。例如，用户的输入是点击第二条新闻，而节点内容只有点击第一条新闻，这种情况下就需要根据用户意图进行修改，正确的输出为点击第二条新闻。
4、不要给出任何解释,输出应严格按照JSON 格式，仅包含生成的操作步骤。
5、注意，<参数x>中的x要和补充知识中的保持一致，不要对参数的编号进行修改，不要编纂一个新的编号。

## 用户输入和补充知识
{input}

"""

def get_answer_gpt_4o(query):
    date = str(datetime.now().strftime('%Y-%m-%d'))
    week = str(datetime.now().weekday() + 1)
    input = step_split_prompt.replace("{input}", str(query)).replace("{date}", date).replace("{week}", week)
    payload = {"messages": [{"role": "user", "content": [{"type": "text", "text": input}]}], "temperature": 0}
    headers = {
        "Content-Type": "application/json",
        "api-key": "97a01332ed5b4951af46bc489b011f9f",
    }
    # 记录开始时间
    start_time = time.time()
    response = requests.post(GPT4O_ENDPOINT, headers=headers, json=payload)
    response_content = response.json()["choices"][0]["message"]["content"]
    response_json = eval(re.sub(r"```json|```", "", response_content))
    # print(response_json, "response_text")
    step_list = response_json["步骤输出"]
    # 记录结束时间
    end_time = time.time()
    # 计算总推理时间
    total_time = end_time - start_time
    return step_list, total_time

def get_answer_gpt_4_1(query):
    date = str(datetime.now().strftime('%Y-%m-%d'))
    week = str(datetime.now().weekday() + 1)
    input = step_split_prompt.replace("{input}", str(query)).replace("{date}", date).replace("{week}", week)
    payload = {"messages": [{"role": "user", "content": [{"type": "text", "text": input}]}], "temperature": 0}
    headers = {
        "Content-Type": "application/json",
        "api-key": "c1bda9d190df4bc2887a2955c8d61d51",
    }
    # 记录开始时间
    start_time = time.time()
    response = requests.post(GPT4_1_ENDPOINT, headers=headers, json=payload)
    response_content = response.json()["choices"][0]["message"]["content"]
    response_json = eval(re.sub(r"```json|```", "", response_content))
    # print(response_json, "response_text")
    step_list = response_json["步骤输出"]
    # 记录结束时间
    end_time = time.time()
    # 计算总推理时间
    total_time = end_time - start_time
    return step_list, total_time

def get_answer_qwen2_72b(client, query):
    date = str(datetime.now().strftime('%Y-%m-%d'))
    week = str(datetime.now().weekday() + 1)
    input = step_split_prompt.replace("{input}", str(query)).replace("{date}", date).replace("{week}", week)
    input = input.split("输出格式为")[0]
    system_prompt = ""
    # 记录开始时间
    start_time = time.time()

    response_content = asyncio.run(get_answer_async(client, system_prompt, input))

    # print(response_content, "response_text")
    response_json = eval(re.sub(r"```json|```", "", response_content))
    step_list = response_json["步骤输出"]
    # 记录结束时间
    end_time = time.time()
    # 计算总推理时间
    total_time = end_time - start_time
    return step_list, total_time


def get_answer_qwen3(qwen3_client, query):
    date = str(datetime.now().strftime('%Y-%m-%d'))
    week = str(datetime.now().weekday() + 1)
    input = step_split_prompt.replace("{input}", str(query)).replace("{date}", date).replace("{week}", week)
    system_prompt = ""
    # 记录开始时间
    start_time = time.time()
    # 不带think过程
    # input = f"{input}/no_think"
    reasoning_content, response_content = asyncio.run(get_answer_async(qwen3_client, system_prompt, input)).split("</think>")

    # print(response_json, "response_text")
    response_json = eval(re.sub(r"```json|```", "", response_content))
    step_list = response_json["步骤输出"]
    # 记录结束时间
    end_time = time.time()
    # 计算总推理时间
    total_time = end_time - start_time
    return step_list, total_time


if __name__ == '__main__':
    # 使用文档测试
    query = """
    "用户输入:
去到中国移动，查看我本月的账单
补充知识:
{'打开中国移动': {'点击进入个人中心页面': {'点击我的移动查看账户余额': [], '点击账单查询': [], '点击套餐余量查询': [], '找到并进入话费充值页面': [], '点击缴费记录查询': {'选择查询最近半年的缴费记录': [], '选择查询最近一个月的缴费记录': []}, '找到并点击我的F码': {'查看尚未使用的F码列表': []}, '点击积分明细查询': {'选择查询最近半年的积分明细': []}, '找到并进入消息订阅页面（查看订阅消息时只需要执行到此步骤）': [], '找到并进入消息查看页面': {'点击查看账户消息': [], '点击查看服务消息': [], '点击查看活动消息': [], '点击查看订单消息': [], '点击查看商品消息': []}, '找到并进入我的发票页面': {'查看月结发票信息': []}, '找到并进入宽带充值页面': [], '找到并进入业务查询页面': {'查看套餐详情': [], '查看增值业务详情': [], '查看其他业务列表': [], '查看账户拥有的基本功能（需要找到并进入业务查询页面）': []}}, '找到并点击进入积分商城': {'浏览可兑换的商品信息': []}, '进入网上营业厅页面': {'点击查看当前提供的流量业务': [], '点击查看当前可办理的5G套餐': [], '点击查看当前提供的数据业务': []}, '点击进入我的邮箱（不需要点击进入我的移动页面）': []}}
输出格式为:1.xxx...其中xxx为拆解后的自动化流程。"
    """
    qwen3_client = create_local_qwen_client()
    qwen3_4b_client = create_qwen_4b_client()
    qwen2_72b_client = create_qwen_72b_client()
    tars67b_client = create_tars_67b_client()
    response_content, total_time = get_answer_qwen2_72b(tars67b_client, query)

    # response_content, total_time = get_answer_gpt_4o(query)
    print(f"模型输出是：{response_content}")
    print(f"回答耗时：{total_time}")
