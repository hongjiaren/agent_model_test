from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
import websocket
import json
import uuid
import time
import numpy as np
from datetime import datetime


def on_open(ws):
    print(f'connected, {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print("WebSocket连接已打开")
    # 发送消息到服务器
    time.sleep(0.3)
    requestId = 'test_'+str(uuid.uuid4())
    # query = '钉钉发起一下明天下午 3 点到 5 点的会议，主题是 agent 优化，参会人员有阿亮'
    query = '到12306查询明天杭州到北京的单程高铁票'
    xx = {'action': 'ping', 'requestId': requestId, 'payload': {}, 'authorization': 'D4CE2B3C485193AF9C1E8FFE2322C2FEDF4350AA34130E12C7CF8BEBA5D4CA6D66C7493E731D9F88E98280B377AD9C76'}
    # print('send ping:  ', xx)
    ws.send(json.dumps(xx, ensure_ascii=False))
    # 
    # ws.send("Hello, WebSocket Server!")
    requestId = 'test_'+str(uuid.uuid4())
    data_json = {'authorization': 'D4CE2B3C485193AF9C1E8FFE2322C2FEDF4350AA34130E12C7CF8BEBA5D4CA6D9DC3AC624D87993C3984D96EDF32A4AB', 'action': 'chat', 'payload': {'isAtApplication': False, 'preUuid': '', 'packageId': '', 'action': 'init', 'componentInfo': {}, 'sessionId': '', 'autofill': True, 'factoryVersion': '7.1.0.0-develop-7.1.0', 'message': query, 'type': 'flow', 'userId': 36429, 'apps': []}, 'requestId': requestId, 'difyUrl': 'http://10.4.2.64'}
    # data_json = {'authorization': 'D4CE2B3C485193AF9C1E8FFE2322C2FEDF4350AA34130E12C7CF8BEBA5D4CA6D9DC3AC624D87993C3984D96EDF32A4AB', 'action': 'chat', 'payload': {'isAtApplication': True, 'preUuid': '', 'packageId': '', 'fileInfo': [], 'sessionId': '', 'factoryVersion': '7.1.0.2-develop-7.1.0', 'message': '孙悟空', 'type': 'flow', 'userId': 36429, 'action': 'init', 'componentInfo': {}, 'autofill': True, 'apps': [{'owner': False, 'is_process': False, 'icon_url': '', 'outputs': {'answer': {'label': {'zh_Hans': '回答', 'en_US': 'answer'}, 'type': 'string'}}, 'users_count': 2, 'author': '勾陈dify', 'icon': '🤖', 'description': '', 'created_at': 1742207337, 'icon_background': '#FFEAD5', 'cloneable': False, 'tags': [], 'mode': 'advanced-chat', 'publish_range': 'all_team_members', 'model_config': {'text_to_speech': {'voice': '', 'language': '', 'enabled': False}, 'speech_to_text': {'enabled': False}, 'retriever_resource': {'enabled': False}, 'suggested_questions': [], 'file_upload': {'image': {'number_limits': 10, 'transfer_methods': ['remote_url', 'local_file'], 'enabled': True}}, 'opening_statement': '您好，我是实在Agent，需要我帮您做什么呢？', 'sensitive_word_avoidance': {'enabled': False}, 'suggested_questions_after_answer': {'enabled': False}, 'support_file_types': [{'extensions': ['jpg', 'jpeg', 'png', 'webp', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt'], 'name': '文档'}]}, 'account_id': '76590', 'name': '生成人物的介绍（gpt3.5）', 'user_input_form': [], 'uiId': 'application_355391d0-3812-4c7a-967b-7b49a5a60e47', 'id': '355391d0-3812-4c7a-967b-7b49a5a60e47', 'is_online': True, 'published_at': 1742232522}]}, 'requestId':requestId, 'difyUrl': 'http://10.4.2.64'}
    
    # data_json = {'authorization': 'D4CE2B3C485193AF9C1E8FFE2322C2FEDF4350AA34130E12C7CF8BEBA5D4CA6D9DC3AC624D87993C3984D96EDF32A4AB', 'action': 'chat', 'payload': {'isAtApplication': True, 'preUuid': '', 'packageId': '', 'fileInfo': [], 'sessionId': '', 'factoryVersion': '7.1.0.2-develop-7.1.0', 'message': '5432', 'type': 'flow', 'userId': 36429, 'action': 'init', 'componentInfo': {}, 'autofill': True, 'apps': [{'owner': False, 'is_process': False, 'icon_url': '', 'outputs': {'answer': {'label': {'zh_Hans': '回答', 'en_US': 'answer'}, 'type': 'string'}}, 'users_count': 4, 'author': '勾陈dify', 'icon': '🤖', 'description': '', 'created_at': 1742207631, 'icon_background': '#FFEAD5', 'cloneable': False, 'tags': [], 'mode': 'advanced-chat', 'publish_range': 'all_team_members', 'model_config': {'text_to_speech': {'voice': '', 'language': '', 'enabled': False}, 'speech_to_text': {'enabled': False}, 'retriever_resource': {'enabled': False}, 'suggested_questions': [], 'file_upload': {'image': {'number_limits': 10, 'transfer_methods': ['remote_url', 'local_file'], 'enabled': True}}, 'opening_statement': '您好，我是实在Agent，需要我帮您做什么呢？', 'sensitive_word_avoidance': {'enabled': False}, 'suggested_questions_after_answer': {'enabled': False}, 'support_file_types': [{'extensions': ['jpg', 'jpeg', 'png', 'webp', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt'], 'name': '文档'}]}, 'account_id': '76590', 'name': '生成人物的介绍（deepseek）', 'user_input_form': [], 'uiId': 'application_5aa76316-a417-4c84-827d-7cf97eee5557', 'id': '5aa76316-a417-4c84-827d-7cf97eee5557', 'is_online': True, 'published_at': 1742215827}]}, 'requestId': requestId, 'difyUrl': 'http://10.4.2.64'}

    json_payload = json.dumps(data_json, ensure_ascii=False)
    ws.send(json_payload)
    # print('send request:  ', data_json)
    
    
def on_message(ws, message):
    print(f"接收到消息: {message}")
    # time.sleep(10)
    data = json.loads(message)
    # print('data:  ', data)
    if 'action' in data and data['action']=='streamMessage' and data['payload']['type']=='streamEnd':
        ws.close()
    if 'action' in data and data['action']=='streamMessage' and '<!DOCTYPE' in data['payload']['content']:
        ws.close()
    if 'action' in data and 'requestId' in data and 'payload' in data:
        ws.close()

def on_error(ws, error):
    print(f"发生错误: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket连接已关闭")

def agent_flow(idx):
    t1 = time.time()
    ws_url = 'ws://60.165.238.132:16580/nlp/chatRPA/api'
    # ws_url = 'ws://47.97.62.124:16580/nlp/chatRPA/api'
    print(f'start connect {idx}, {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                # keepalive=30,
                                )
    # ws.on_open=on_open
    # wss = websocket.WebSocket()
    # wss()
    # 启动WebSocket连接
    ws.run_forever(ping_timeout=10, ping_interval=20)
    # pass
    print('cost:  ', time.time()-t1)
    return time.time()-t1



if __name__ == "__main__":
    # agent_flow()
    
    
    process_pool = ProcessPoolExecutor(max_workers=20)
    pp_list = []
    for i in range(1):
        f = process_pool.submit(agent_flow, i)
        pp_list.append(f)
        
    tt_list = []
    for f in pp_list:
        tt = f.result()
        tt_list.append(tt)
    
    print('avg: ', np.mean(tt_list))
    print('max: ', np.max(tt_list))
    print('min: ', np.min(tt_list))
    
    # {'create_at': 1739409098000, 'description': '百度搜索关键词，查看第一条相关资讯', 'icon': '', 'icon_background': '', 'id': 'B0xeiAEZEz', 'mode': 'normal', 'name': '百度搜索并查看资讯', 'opening_statement': '百度搜索关键词，查看第一条相关资讯', 'packageLocalFullPath': 'C:\\Users\\罗\\AppData\\Roaming\\Z-Factory\\builtin-pkg\\百度搜索并查看资讯-0.0.1', 'suggested_questions': [123123], 'user_input_form': [{'text-input': {'label': '关键词', 'max_length': 48, 'options': [], 'required': False, 'type': 'text-input', 'variable': 'keywords'}}
    
    
#     avg:  17.929715378284456
# max:  35.749932527542114
# min:  3.449341058731079