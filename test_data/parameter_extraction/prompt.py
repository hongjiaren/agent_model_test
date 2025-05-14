

def param_select_qwen14b_batch(query_batch, step_list_batch, history):
    SYSTEM_PROMPT = "你是一个参数提取的专家，请扫描生成的所有操作步骤，识别步骤中的形参占位符，构建详细的参数描述体系。然后从用户的query中提取出对应的参数的值，写入对应的参数值。"
    param_select_prompt = """
    ## 用户输入
    {query}
    ## 已生成步骤
    {step_list}
    ## 历史信息
    {history}
    今天是{date}，星期{week}。参数涉及到日期的时候，根据当前日期进行推理。
    ## 思维过程（CoT)
    1. 参数解析：扫描生成的所有操作步骤，识别步骤中的形参占位符，并构建详细的参数描述体系：
       - 只提取步骤中的形参占位符作为参数，如果步骤中不存在形参占位符，不要自己编撰参数。例如，步骤的名称是设置会议时间，没有形参占位符，不要编撰会议时间这个参数。
       - 对每个形参根据上下文自动生成参数描述，说明参数用途、格式要求、有效值范围及业务规则。注意，可能存在多个不同的参数占位符指向同一个参数的情况，即不同的参数占位符对应的参数的描述和参数值是一样的。
    2. 参数匹配：将用户输入内容以及历史信息中的内容与生成的参数描述进行语义匹配，提取具体参数值：
       - 显式匹配：若用户输入中直接给出参数值，直接映射至对应形参。
       - 隐式匹配：若参数值需要根据上下文推导（如“明天下午”推导为具体日期和时间），则进行合理推理。
       - 同一个参数存在多个值的时候不要进行参数的拆分，使用list来存放多个值。例如会议的参会人员有kevin，eric和ray，那么parameter就是['kevin','eric','ray']
       - 对无法推导的参数，标记为unknown或者是空列表，并在参数描述中注明应该提供的参数的具体描述。
       - 历史信息中的参数和内容可以直接引用，以提高参数填充的准确度。例如：
           历史信息：已完成内容：生成一段中秋节祝福（这是变量名，可直接使用，无需补充）。
           用户query：写一段中秋节祝福，微信上发给xxx
           存在一个参数是微信发送消息<参数2>。这个<参数2>的parameter就是"已完成内容：生成一段中秋节祝福"
        
    ## 输出格式
    输出应严格按照如下 JSON 格式，仅包含参数映射，不要输出其他的任何内容：
    ```json
    {
      "参数输出": [
        {
          "name": "<参数1>",
          "description": "参数描述示例_1",
          "parameter": "unknown"  
        },
        {
          "name": "<参数6>",
          "description": "参数描述示例_2",
          "parameter": []  
        }
      ]
    }
    ```
    注意事项：
    1. 参数值必须完全来自用户输入，禁止虚构或复制示例中的占位符；
    2. 若用户未提供参数值，则设为 "unknown"（如会议主题）或空列表（同一个参数存在多个值,如参会人员）；
    3. 可能存在多个不同的参数占位符指向同一个参数的情况，即不同的参数占位符对应的参数的描述和参数值是一样的。
    4. description 字符串里只需要解释清楚这个参数是什么，不用将用户query中的内容在这里面展示，也不要在输出的参数描述体系中，加入任何注释。。
    例如："description": "用户搜索的话剧歌剧类型，\"开心麻花\"是一类话剧歌剧的名字。"就是一个错误的写法，正确的写法为："description": "用户搜索的话剧歌剧类型"，不需要举例说明。
    5. 参数描述体系中的name一定要用<>包裹住参数的名称，例如"<参数1>"是正确的，"参数1"是错误的。
    """

    # 替换模板中的占位符
    date = "2025-03-18"
    week = "星期二"
    input_batch = []
    for idx, query in enumerate(query_batch):
        input_batch.append(param_select_prompt.replace("{query}", str(query)).replace("{step_list}", str(step_list_batch[idx])).replace("{date}",
                                                                                                        date).replace(
            "{week}", week).replace("{history}", str(history[idx])))
    sampling_params = {
        "temperature": 0.7,
        "top_p": 0.8,
        "max_tokens": 2048
    }
    data = {"system_prompt":SYSTEM_PROMPT,
        "prompt": input_batch,
        "sampling_params": sampling_params}
    start_time = time.time()
    try:
        response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            end = time.time()
            total_time = end - start_time
            results = response.json()  # 解析 JSON 响应

            generated_text_batch = results['outputs']

            return generated_text_batch, total_time
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None, None
    except requests.exceptions.RequestException as e:
        print("Request failed:", str(e))
        return None, None


# 参数提取的时间不要修改，会有针对时间的推理
# date = "2025-03-18"
#     week = "星期二"