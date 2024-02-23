#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author: zhibo.wang
# E-mail: gm.zhibo.wang@gmail.com
# Date  :
# Desc  :

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


import requests
import json


def fun_qanything_chat(question):
    tag = "知识库"
    msg = f"{tag}: 服务器睡着了,请稍后再试"
    if 1:
        url = "https://ai.youdao.com/saas/api/q_anything/saas/chat_stream"
        params = None
        payload = json.dumps({
           "kbIds": [
              "KB31cad7f5c4944905bab6b105a7ae409a"
           ],
           "history": [],
           "question": question
        })
        headers = {
           'authority': 'ai.youdao.com',
           'accept': 'text/event-stream,application/json, text/event-stream',
           'accept-language': 'zh-CN,zh;q=0.9',
           'origin': 'https://ai.youdao.com',
           'referer': 'https://ai.youdao.com/saas/qanything/',
           'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
           'sec-ch-ua-mobile': '?0',
           'sec-ch-ua-platform': '"Linux"',
           'sec-fetch-dest': 'empty',
           'sec-fetch-mode': 'cors',
           'sec-fetch-site': 'same-origin',
           'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
           # 'Cookie': "JSESSIONID_NEW=935be01b-1e93-4a63-9cb3-c23d836cf2bc",
           'Cookie': "JSESSIONID_NEW=bac865bc-e3bb-4b9d-8b48-3476236d9a31",
           'content-type': 'application/json'
        }
        response = requests.request("POST", url, stream=True,
                                    headers=headers, params=params,
                                    data=payload, verify=True,
                                    timeout=(5, 90))
        if response.status_code == 200:
            response.encoding = "utf-8"
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        event_field = parts[0].strip()
                        data_field = parts[1].strip()
                        if event_field == "data":
                            if data_field and data_field[:1] == "{":
                                # print([data_field])
                                data_field_json = json.loads(data_field)
                                if data_field_json.get("result").get("question"):
                                    response = data_field_json.get("result").get("response")
                                    msg = f"{response}"
    return msg


a = fun_qanything_chat("行李问题")
print(a)


def upload_file():
    import requests

    url = "https://ai.youdao.com/saas/api/q_anything/saas/upload_file"

    payload = {'kbId': 'KB31cad7f5c4944905bab6b105a7ae409a'}
    files = [
      ('file', ('在过去的一年里.docx',open('/home/yu/文档/WeChat Files/wxid_dtsg9sidbaw812/FileStorage/File/2024-01/在过去的一年里.docx','rb'),'application/vnd.openxmlformats-officedocument.wordprocessingml.document'))
    ]
    headers = {
      'authority': 'ai.youdao.com',
      'accept': '*/*',
      'accept-language': 'zh-CN,zh;q=0.9',
      'cookie': 'JSESSIONID_NEW=935be01b-1e93-4a63-9cb3-c23d836cf2bc; NTES_YD_SESS=dwDDVVYe3O4uZ3G2Qf_0i7pi4jb5VmuWL80EZm5HDDNuqC5iqgFBt6G.QYrPeBiJ7la08YKlQhpMGkYGAe7sq5vEh_leLBieBDSNqt7yQ4QOEWSWWtofGOnTr85uI0d2349oj6NK0.TtI6lpnOlZ7FxiqA3FD.t07x3IZgoPZ8qhGtneL2x.qvXy3Mk5l45Iw6z3jCq0zEDPAp7VMtOrVoqFj2IVuc9PnOx_rdmbPkaxP; S_INFO=1707213204|0|0&60##|18089261693; P_INFO=18089261693|1707213204|1|youdao_zhiyun2018|00&99|sxi&1707212776&youdao_zhiyun2018#sxi&610100#10#0#0|&0|null|18089261693; csrfToken=618427f7; ISLOGIN=1',
      'origin': 'https://ai.youdao.com',
      'referer': 'https://ai.youdao.com/saas/qanything/',
      'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Linux"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)





