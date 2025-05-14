import requests
import re
import time
import pandas as pd
import json
from datetime import datetime
from open_client import create_local_qwen_client, get_answer_async, get_answer_async_reasoning, create_qwen_4b_client, create_qwen_72b_client, create_qwen_7b_client, create_tars_67b_client
import asyncio

def get_answer_qwen2(client, system_prompt, query):

    # 记录开始时间
    start_time = time.time()
    # 不带think过程
    # query = f"{query}/no_think"
    response_content = asyncio.run(get_answer_async(client, system_prompt, query))
    # print(reasoning_content)
    # 记录结束时间
    end_time = time.time()
    # 计算总推理时间
    total_time = end_time - start_time
    return response_content, total_time

def get_answer_qwen3(client, system_prompt, query):

    # 记录开始时间
    start_time = time.time()
    # 不带think过程
    # query = f"{query}/no_think"
    reasoning_content, response_content = asyncio.run(get_answer_async(client, system_prompt, query)).split("</think>")
    # print(reasoning_content)
    # 记录结束时间
    end_time = time.time()
    # 计算总推理时间
    total_time = end_time - start_time
    return response_content, total_time


if __name__ == '__main__':

    system_prompt = "现在你是一个机器人流程自动化（RPA）专家，你有根据instruction,input和history对应内容生成目标执行步骤的能力，instruction中补充知识的内容是对应于具体应用程序的离线地图。请理解离线地图的拆解逻辑，理解其中的每一步和相邻前后步骤的关系。在理解每一次输入内容的意图的基础上，能够根据离线地图对每一个执行步骤做出正确选择，最终输出正确的执行步骤。不要错误执行，进入非目标步骤，不要多执行，也不要少执行。每一个步骤的内容要与离线地图中的保持一致。输出格式要规范统一，固定为1.xxx\n2.yyy\n3.zzz...这种格式。如果进入离线地图后无法完成目标，输出固定文本'离线地图无法完成目标'。理解多意图并成功执行步骤拆解，比如钉钉搜索联系人阿良和仙道，那么再执行第二个意图时要从头开始，即'1.启动钉钉\n2.搜索联系人<参数26>\n3.启动钉钉\n4.搜索联系人<参数26>。参数编号需与补充知识中的内容保持一致。学会对后续新加入的补充知识中的离线地图进行正确拆解。学会正确的反思，节点逻辑关系正确。完成最后一步时添加"
    query = """
    "用户输入:
帮我打开腾讯视频，查看我的动态
补充知识:
{'打开腾讯视频网页': {'点击进入个人中心': {'查看观看历史': [], '清空观看历史': [], '找到并查看加追': [], '点击收藏': {'查看收藏的综艺': [], '查看收藏的电视剧': [], '查看收藏的电影': [], '查看收藏的动漫': [], '查看收藏的纪录片': [], '查看收藏的直播': [], '清除全部收藏': []}, '找到并查看订阅': [], '找到并查看钻石余额': [], '找到并查看钻石交易记录': [], '找到并查看钻石充值记录': [], '找到并点击订单': {'查看待发货订单': [], '查看待收货订单': [], '查看待支付订单': [], '查看待评价订单': []}, '找到并查看我的动态': []}, '搜索<参数1>': {'找到并关注首个用户': [], '找到并播放第一集': []}, '点击进入搜索页面': {'清除搜索记录': []}, '点击电影': {'找到并进入电影片库': {'筛选高分好评、免费的电影': [], '筛选最新的内地电影': [], '筛选动作类型、即将上线的电影': []}}, '点击电视剧': {'找到并进入电视剧片库': {'筛选高分好评、内地的电视剧': [], '筛选最新上架、奇幻类型的电视剧': []}}, '点击动漫': {'找到并进入动漫片库': {'筛选最近更新、3D动画的动漫': [], '筛选内地、武侠类型的动漫': []}}}}
输出格式为:1.xxx...其中xxx为拆解后的自动化流程。"
    """
    qwen3_client = create_local_qwen_client()
    qwen3_4b_client = create_qwen_4b_client()
    qwen2_72b_client = create_qwen_72b_client()
    qwen2_7b_client = create_qwen_7b_client()
    tars_67b_client = create_tars_67b_client()
    response_content, total_time = get_answer_qwen2(tars_67b_client, system_prompt, query)

    # response_content, total_time = get_answer_gpt_4o(query)
    print(f"模型输出是：{response_content}")
    print(f"回答耗时：{total_time}")
