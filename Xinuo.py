#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author : zhibo.wang
# E-mail : gm.zhibo.wang@gmail.com
# Date   :
# Desc   :


try:
    from common.log import logger
    from plugins import *
    from bridge.context import ContextType
    from bridge.reply import Reply, ReplyType
    import os
    import re
    import json
    import time
    import execjs
    import base64
    import random
    import hashlib
    import plugins
    import datetime
    import requests
    from Crypto.Cipher import AES
    from fake_useragent import UserAgent
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    import base64
    from .xinuo_utils import Util

    import uuid
    import pymongo
    import hashlib
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except Exception as e:
    logger.error(f"[Xinuo] import error: {e}")


@plugins.register(
    name="Xinuo",                         # 插件的名称
    desire_priority=1,                    # 插件的优先级
    hidden=False,                         # 插件是否隐藏
    desc="个人开发的一些常用工具",        # 插件的描述
    version="0.0.4",                      # 插件的版本号
    author="gm.zhibo.wang@gmail.com",                       # 插件的作者
)



class Xinuo(Plugin):

    mongodb_config = {
                  "host": "127.0.0.1",
                  "port": 27017,
                  "db": "ocr_datas_db",
                  "user": "",
                  "pwd": ""
                 }

    def __init__(self):
        super().__init__()
        tag = "xinuo 初始化"
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        try:
            self.conf = super().load_config()
            self.linkai_user = self.conf["linkai_user"]
            self.linkai_pwd = self.conf["linkai_pwd"]
            self.linkai_authorization = self.conf["linkai_authorization"]
            self.gpt40_authorization = self.conf["gpt40_authorization"]
            self.gpt40_abc12 = self.conf["gpt40_abc12"]
            self.gpt40_website_key = self.conf["gpt40_website_key"]
            self.gpt40_phone = self.conf["gpt40_phone"]
            logger.info("[Xinuo] inited")
        except Exception as e:
            log_msg = f"{tag}: error: {e}"
            logger.error(log_msg)
            raise self.handle_error(e, "[Xinuo] init failed, ignore ")

    def handle_error(self, error, message):
        logger.error(f"{message}，错误信息：{error}")
        return message

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type not in [
            ContextType.TEXT
        ]:
            return
        context = e_context['context']
        content = context.content.strip()
        session_id = context["session_id"]
        logger.debug(f"[xinuo] on_handle_context. session_id: {session_id}, content: {content}")
        if content.lower() == "linkai签到":
            msg = self.linkai_sign_in()
            content = "linkai签到\n"
            content += f"{msg}"
            reply = self.create_reply(ReplyType.TEXT, content)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        elif content.lower() == "linkai积分":
            msg = self.linkai_balance()
            content = "linkai积分\n"
            content += f"{msg}"
            reply = self.create_reply(ReplyType.TEXT, content)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        elif content.lower() == "验证码识别cid":
            msg = self.create_cid()
            content = "验证码识别\n"
            content += f"CID:{msg}"
            reply = self.create_reply(ReplyType.TEXT, content)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        elif content.lower() == "每日一言":
            msg = self.daily_api()
            content = "每日一言\n"
            content += f"{msg}"
            reply = self.create_reply(ReplyType.TEXT, content)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        elif content[:2] == "翻译":
            logger.info(f"有道翻译: {content}")
            fanyi_text = content[2:]
            msg = self.youdao_fanyi(fanyi_text)
            content = "翻译\n"
            content += f"{msg}"
            reply = self.create_reply(ReplyType.TEXT, content)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        elif content[:5].lower() == "gpt35":
            gpt_text = content[5:].strip()
            logger.info(f"GPT-3.5: {gpt_text}")
            msg = self.fun_gpt35(gpt_text)
            content = "GPT-3.5\n"
            content += f"{msg}"
            reply = self.create_reply(ReplyType.TEXT, content)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        #### gnomic ####
        elif content.lower() == "触发验证码发送":
            tag = '触发验证码发送'
            if not Util.is_admin(e_context):
                Util.set_reply_text(f"{tag}: 需要管理员权限执行", e_context, level=ReplyType.ERROR)
                return
            msg = self.trigger_SMS()
            content = f"{tag}\n"
            content += f"{msg}"
            reply = self.create_reply(ReplyType.TEXT, content)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        elif content[:5].lower() == "验证码上传":
            gpt_text = content[5:].strip()
            tag = '验证码上传'
            if not Util.is_admin(e_context):
                Util.set_reply_text(f"{tag}: 需要管理员权限执行", e_context, level=ReplyType.ERROR)
                return
            msg = self.upload_SMS(gpt_text)
            content = f"{tag}\n"
            content += f"{msg}"
            reply = self.create_reply(ReplyType.TEXT, content)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        elif content[:5].lower() == "gpt40":
            gpt_text = content[5:].strip()
            tag = 'GPT-4.0'
            agSn = "AG2023121818230490XOYB"
            logger.info(f"{tag}: {gpt_text}")
            msg = self.fun_gpt40(gpt_text, tag, agSn)
            content = f"{tag}\n"
            content += f"{msg}"
            reply = self.create_reply(ReplyType.TEXT, content)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        elif content[:4].lower() == "绘画咒语":
            gpt_text = content[4:].strip()
            tag = "绘画咒语"
            agSn = "AG2023121816029247JEQM"
            logger.info(f"{tag}: {gpt_text}")
            msg = self.fun_gpt40(gpt_text, tag, agSn)
            content = f"{tag}\n"
            content += f"{msg}"
            reply = self.create_reply(ReplyType.TEXT, content)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        elif content[:4].lower() == "中药大师":
            gpt_text = content[4:].strip()
            tag = "中药大师"
            agSn = "AG2023120816303472AVHB"
            logger.info(f"{tag}: {gpt_text}")
            msg = self.fun_gpt40(gpt_text, tag, agSn)
            content = f"{tag}\n"
            content += f"{msg}"
            reply = self.create_reply(ReplyType.TEXT, content)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        elif content[:4].lower() == "起名大师":
            gpt_text = content[4:].strip()
            tag = "起名大师"
            agSn = "AG2023121816029247GCSA"
            logger.info(f"{tag}: {gpt_text}")
            msg = self.fun_gpt40(gpt_text, tag, agSn)
            content = f"{tag}\n"
            content += f"{msg}"
            reply = self.create_reply(ReplyType.TEXT, content)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        elif content[:4].lower() == "解名大师":
            gpt_text = content[4:].strip()
            tag = "解名大师"
            agSn = "AG2023121816029247XRMI"
            logger.info(f"{tag}: {gpt_text}")
            msg = self.fun_gpt40(gpt_text, tag, agSn)
            content = f"{tag}\n"
            content += f"{msg}"
            reply = self.create_reply(ReplyType.TEXT, content)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        #### gnomic ####
        elif content == "人品":
            praise_words = [
                           "你这个小机灵鬼！[炸弹]",
                           "你至少比蜗牛快一点。",
                           "你是个好人，但也不用太好。",
                           "虽然不是最棒的，但也不算最烂的。",
                           "你的人品还可以，但是你的智商呢？",
                           "你的人品和智商都还不错，就是有点懒。",
                           "你的人品和智商都不错，就是有点逗比。",
                           "你的人品和智商都很不错，就是有点二。",
                           "你的人品和智商都非常不错，就是有点吹牛。",
                           "你的人品和智商都是天生的神仙级别。[烟花]"
            ]
            # score = random.randint(0, 100)
            # stair = score // 10
            # praise = praise_words[stair]
            score = 100
            praise = "你的人品和智商都是天生的神仙级别。[烟花]"
            content = f"🦉 您今天的人品为【{score}】\n"
            content += f"🦉 {praise}"
            reply = self.create_reply(ReplyType.TEXT, content)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
        """
        #
        weather_match = re.match(r'^(?:(.{2,7}?)(?:市|县|区|镇)?|(\d{7,9}))(?:的)?天气$', content)
        if weather_match:
            # 如果匹配成功，提取第一个捕获组
            city_or_id = weather_match.group(1) or weather_match.group(2)
            if not self.alapi_token:
                self.handle_error("alapi_token not configured", "天气请求失败")
                reply = self.create_reply(ReplyType.TEXT, "请先配置alapi的token")
            else:
                content = self.get_weather(self.alapi_token, city_or_id, content)
                reply = self.create_reply(ReplyType.TEXT, content)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
        """

    def create_reply(self, reply_type, content):
        reply = Reply()
        reply.type = reply_type
        reply.content = content
        return reply

    def get_help_text(self, verbose=False, **kwargs):
        help_text = "发送关键词执行对应操作\n"
        if not verbose:
            return help_text
        help_text += "输入 'linkai签到'， 进行签到\n"
        help_text += "输入 'linkai积分'， 进行总积分获取\n"
        help_text += "输入 '翻译+内容'， 进行有道翻译\n"
        help_text += "输入 '人品'， 随机获取人品分数\n"
        help_text += "输入 'gpt35+内容'， 使用gpt35模型进行回答\n"
        help_text += "输入 '验证码识别cid'，获取验证码识别cid \n"
        help_text += "输入 '每日一言'，每日一言 \n"
        help_text += "输入 '绘画咒语'，mj绘画咒语 \n"
        help_text += "输入 '中药大师'，中药大师 \n"
        help_text += "输入 '起名大师'，起名大师 \n"
        help_text += "输入 '解名大师'，解名大师 \n"
        return help_text

    def get_timestamp(self, n=13):
        # 获取时间戳  返回13位或者10位时间戳
        if n == 13:
            return str(int(time.time()*1000))
        else:
            return str(int(time.time()))

    def random_user_agent(self):
        U = UserAgent()
        return U.random

    def random_youdao_cookie(self):
        # 有道翻译cookies 生成
        user_id = random.randrange(100000000, 999999999)
        ip_address = ".".join(str(random.randrange(0, 256)) for _ in range(4))
        cookie = f"OUTFOX_SEARCH_USER_ID={user_id}@{ip_address}"
        return cookie

    def youdao_fanyi(self, fanyi_text):
        tag = '有道翻译'
        msg = f"{tag}: 服务器睡着了,请稍后再试"
        try:
            cookie = self.random_youdao_cookie()
            ua = self.random_user_agent()
            headers = {
                'user-agent': ua,
                'Cookie': cookie,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json, text/plain, */*',
                'Origin': 'https://fanyi.youdao.com',
                'Referer': 'https://fanyi.youdao.com/',
                'Host': 'dict.youdao.com',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
            }
            mysticTime = str(int(time.time() * 1000))
            url = 'https://dict.youdao.com/webtranslate'
            client = "fanyideskweb"
            keyid = "webfanyi"
            pointParam = "client,mysticTime,product"
            appVersion = "1.0.0"
            vendor = "web"
            keyfrom = "fanyi.web"
            key_ = 'fsdsogkndfokasodnaso'
            encoding='gb18030'
            md5_text = f'client={client}&mysticTime={mysticTime}&product={keyid}&key={key_}'
            md5 = hashlib.md5(md5_text.encode(encoding)).hexdigest()
            payload = {
                'i': fanyi_text,
                'from': 'auto',
                'to': '',
                'domain': '0',
                'dictResult': 'true',
                'keyid': keyid,
                'sign': md5,
                'client': client,
                'product': keyid,
                'appVersion': appVersion,
                'vendor': vendor,
                'pointParam': pointParam,
                'mysticTime': mysticTime,
                'keyfrom': keyfrom,
                'mid': '1',
                'screen': '1',
                'model': '1',
                'network': 'wifi',
                'abtest': '0',
                'yduuid': 'abcdefg',
            }
            response = requests.post(url, data=payload, headers=headers, timeout=30)
            r_code = response.status_code
            if r_code == 200:
                res_text = response.text
                decodeiv = "ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4"
                decodekey = "ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl"
                key = hashlib.md5(decodekey.encode(encoding=encoding)).digest()
                iv = hashlib.md5(decodeiv.encode(encoding=encoding)).digest()
                aes_en = AES.new(key, AES.MODE_CBC, iv)
                data_new = base64.urlsafe_b64decode(res_text)
                result_text = aes_en.decrypt(data_new).decode('utf-8')
                remove_text = "}".join(result_text.split("}")[:-1]) + "}"
                res_json = json.loads(remove_text)
                """
                {
                   "code":0,
                   "dictResult":{

                   },
                   "translateResult":[
                       [
                           {
                               "tgt":"Automatic production test",
                               "src":"自动生编测试",
                               "srcPronounce":"zì dòng shēng biān cèshì"
                           }
                       ]
                   ],
                   "type":"zh-CHS2en"
               }
                """
                r_json_code = res_json.get("code")
                if r_json_code == 0:
                    translateResult = res_json.get("translateResult")
                    if len(translateResult) > 0:
                        end_fanyi  = translateResult[0][0].get("tgt")
                        if end_fanyi:
                            msg = f"原始本文:{fanyi_text}\n翻译后文本:{end_fanyi}"
                        else:
                            log_msg = f"{tag}: 数据解析失败: {translateResult[0]}"
                            logger.info(log_msg)
                    else:
                        log_msg = f"{tag}: 数据解析失败: {translateResult}"
                        logger.info(log_msg)
                else:
                    log_msg = f"{tag}: 返回状态码异常 code:{r_json_code}"
                    logger.info(log_msg)
            else:
                log_msg = f"{tag}: 请求状态码异常 code:{r_code}"
                logger.info(log_msg)
        except Exception as e:
            log_msg = f"{tag}: error: {e}"
            logger.error(log_msg)
        return msg

    def fun_gpt35(self, gpt_text):
        # GPT-35
        tag = 'GPT-35'
        msg = f"{tag}: 服务器睡着了,请稍后再试"
        try:
            url = "https://api.binjie.fun/api/generateStream"
            headers = {
                       'authority': 'api.binjie.fun',
                       'accept': 'application/json, text/plain, */*',
                       'accept-language': 'zh-CN,zh;q=0.9',
                       'content-type': 'application/json',
                       'dnt': '1',
                       'origin': 'https://chat18.aichatos.xyz',
                       'referer': 'https://chat18.aichatos.xyz/',
                       'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                       'sec-ch-ua-mobile': '?0',
                       'sec-ch-ua-platform': '"macOS"',
                       'sec-fetch-dest': 'empty',
                       'sec-fetch-mode': 'cors',
                       'sec-fetch-site': 'cross-site',
                       'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                     }
            payload = json.dumps({
                      "prompt": gpt_text,
                      "userId": "#/chat/1705071409703",
                      "network": True,
                      "system": "",
                      "withoutContext": False,
                      "stream": False
                    })

            response = requests.post(url, data=payload, headers=headers, timeout=60)
            r_code = response.status_code
            if r_code == 200:
                response.encoding = "utf-8"
                res_text = response.text
                if res_text:
                    msg = res_text
                else:
                    log_msg = f"{tag}: 返回异常 msg:{res_text}"
                    logger.info(log_msg)
            else:
                log_msg = f"{tag}: 请求状态码异常 code:{r_code}"
                logger.info(log_msg)
        except Exception as e:
            logger.error(f"{tag}: 服务器内部错误 {e}")
        return msg


    def edit_config_json(self, key, value):
        curdir = os.path.dirname(__file__)
        config_path = os.path.join(curdir, "config.json")
        # 修改配置文件信息
        with open(config_path, 'r') as file:
            data = json.load(file)
        data[key] = value
        with open(config_path, 'w') as file:
            json.dump(data, file, indent=4)
        logger.info(f"修改配置文件: key {key}, value: {value}")


    ###### gnomic PGT-4.0 #####
    def get_keyid(self):
        # headers keyid
        code = """
        "" + Math.round(Math.random()) + Math.random().toString(36).substring(2, 32)
        """
        ctx = execjs.compile(code)
        result = ctx.eval(code)
        return result

    def get_passid(self):
        # headers passid
        return str(round(1e10 * random.random()))

    def get_aee(self, timestamp, website_key, abc12):
        #
        key = website_key[:8] + timestamp[:3] + timestamp[-5:]
        iv = key
        cipher = Cipher(algorithms.AES(key.encode()), modes.CBC(iv.encode()),
                        backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(abc12.encode()) + encryptor.finalize()
        return base64.b64encode(ciphertext).decode('utf-8')

    def trigger_SMS(self):
        # gnomic 触发验证码发送
        tag = "gnomic 触发验证码发送"
        msg = f"{tag}: 服务器睡着了,请稍后再试"
        try:
            url = f"https://gnomic.cn/api/app/appmobile/{self.gpt40_phone}?randomStr=blockPuzzle&grant_type=password"
            payload={}
            timestamp = self.get_timestamp()
            passid = self.get_passid()
            keyid = self.get_keyid()
            aee = self.get_aee(timestamp, self.gpt40_website_key, self.gpt40_abc12)
            headers = {
               'authority': 'gnomic.cn',
               'abc12': self.gpt40_abc12,
               'accept': 'application/json, text/plain, */*',
               'accept-language': 'zh-CN,zh;q=0.9',
               'aee': aee,
               'authorization': 'Basic YXBwOmFwcA==',
               'cache-control': 'no-cache',
               'client-toc': 'Y',
               'dnt': '1',
               'keyid': keyid,
               'passid': passid,
               'referer': 'https://gnomic.cn/agentCenter/index',
               'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
               'sec-ch-ua-mobile': '?0',
               'sec-ch-ua-platform': '"macOS"',
               'sec-fetch-dest': 'empty',
               'sec-fetch-mode': 'cors',
               'sec-fetch-site': 'same-origin',
               'tenant-id': '1',
               'tenant_id': '1',
               'timestamp': timestamp,
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }

            response = requests.request("GET", url, headers=headers, data=payload,
                                        verify=False, timeout=(5, 30))

            if response.status_code == 200:
                res_json = response.json()
                if res_json.get("code") == 0:
                    result = res_json.get("data")
                    msg = "成功"
            # print(response.text)
            # {"code":0,"message":"ok","data":true}
        except Exception as e:
            logger.error(f"{tag}: 服务器内部错误 {e}")
        return msg

    def upload_SMS(self, sms_code):
        # gnomic 验证码上传
        tag = "gnomic 登录"
        msg = f"{tag}: 服务器睡着了,请稍后再试"
        try:
            logger.info(f"{tag}: sms_code {sms_code}")
            url = f"https://gnomic.cn/api/auth/oauth2/token?mobile=APP-SMS@{self.gpt40_phone}&grant_type=mobile&code={sms_code}&scope=server"
            logger.info(f"{tag}: url {url}")
            payload={}
            timestamp = self.get_timestamp()
            passid = self.get_passid()
            keyid = self.get_keyid()
            aee = self.get_aee(timestamp, self.gpt40_website_key, self.gpt40_abc12)
            headers = {
               'authority': 'gnomic.cn',
               'abc12': self.gpt40_abc12,
               'accept': 'application/json, text/plain, */*',
               'accept-language': 'zh-CN,zh;q=0.9',
               'aee': aee,
               'authorization': 'Basic YXBwOmFwcA==',
               'cache-control': 'no-cache',
               'client-toc': 'Y',
               'dnt': '1',
               'keyid': keyid,
               'passid': passid,
               'referer': 'https://gnomic.cn/agentCenter/index',
               'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
               'sec-ch-ua-mobile': '?0',
               'sec-ch-ua-platform': '"macOS"',
               'sec-fetch-dest': 'empty',
               'sec-fetch-mode': 'cors',
               'sec-fetch-site': 'same-origin',
               'tenant-id': '1',
               'tenant_id': '1',
               'timestamp': timestamp,
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }

            response = requests.request("POST", url, headers=headers, data=payload,
                                        verify=False, timeout=(5, 30))
            logger.info(f"{tag}: response {response.text}")
            if response.status_code == 200:
                res_json = response.json()
                if res_json.get("sub"):
                    access_token = res_json.get("access_token")
                    logger.info(f"{tag}: 获取access_token 成功")
                    self.gpt40_authorization = f"Bearer {access_token}"
                    key = "gpt40_authorization"
                    self.edit_config_json(
                        key,
                        self.gpt40_authorization)
                    msg = f"{tag}: 成功"
        except Exception as e:
            logger.error(f"{tag}: 服务器内部错误 {e}")
        return msg


    def run_gpt40_put_prompt(self, input_prompt, tag, agSn):
        result = None
        tag_ = f"{tag}创建任务"
        try:
            timestamp = self.get_timestamp()
            passid = self.get_passid()
            keyid = self.get_keyid()
            aee = self.get_aee(timestamp, self.gpt40_website_key, self.gpt40_abc12)
            url = "https://gnomic.cn/api/bbs/front/im/chat/history/application/pre/chat"
            payload = {
                "inputText": input_prompt,
                "scene": 0,
                "agSn": agSn,
                "modelType": 2,
                "maxTokens": 2048,
                "temperature": 0.75,
                "presencePenalty": 0,
                "frequencyPenalty": 0,
                "numberOfMessagesWithHistory": 4,
                "maxOutputTokens": 1024,
                "topK": 40,
                "topP": 0.8,
                "memoryRoundNum": 2,
                "initImages": []
            }
            payload = json.dumps(payload)
            headers = {
              'Host': 'gnomic.cn',
              'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
              'aee': aee,
              'dnt': '1',
              'authorization': self.gpt40_authorization,
              'sec-ch-ua-platform': '"macOS"',
              'abc12': self.gpt40_abc12,
              'sec-ch-ua-mobile': '?0',
              'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
              'content-type': 'application/json; charset=UTF-8',
              'accept': 'application/json, text/plain, */*',
              'client-toc': 'Y',
              'cache-control': 'no-cache',
              'timestamp': timestamp,
              'keyid': keyid,
              'tenant-id': '1',
              'passid': passid,
              'origin': 'https://gnomic.cn',
              'sec-fetch-site': 'same-origin',
              'sec-fetch-mode': 'cors',
              'sec-fetch-dest': 'empty',
              'referer': f'https://gnomic.cn/agentCenter/detail?schemeNo={agSn}&type=1',
              'accept-language': 'zh-CN,zh;q=0.9'
            }
            response = requests.request("POST", url,
                                        headers=headers, data=payload,
                                        verify=False, timeout=(5, 30))
            if response.status_code == 200:
                res_json = response.json()
                if res_json.get("code") == 0:
                    result = res_json.get("data")
        except Exception as e:
            logger.error(f"{tag_}: 服务器内部错误 {e}")
        return result

    def run_gpt40_get_data(self, _id, tag, agSn):
        result_text = ""
        tag_ = f"{tag}获取结果"
        try:
            timestamp = self.get_timestamp()
            passid = self.get_passid()
            keyid = self.get_keyid()
            aee = self.get_aee(timestamp, self.gpt40_website_key, self.gpt40_abc12)
            url = "https://gnomic.cn/api/bbs/front/im/chat/history/application/chat"
            params = {"key": _id}
            payload = {}
            headers = {
              'Host': 'gnomic.cn',
              'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
              'aee': aee,
              'dnt': '1',
              'authorization': self.gpt40_authorization,
              'sec-ch-ua-platform': '"macOS"',
              'abc12': self.gpt40_abc12,
              'sec-ch-ua-mobile': '?0',
              'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
              'content-type': 'application/json; charset=utf-8',
              'accept': 'text/event-stream',
              'client-toc': 'Y',
              'cache-control': 'no-cache',
              'timestamp': timestamp,
              'keyid': keyid,
              'tenant-id': '1',
              'passid': passid,
              'sec-fetch-site': 'same-origin',
              'sec-fetch-mode': 'cors',
              'sec-fetch-dest': 'empty',
              'referer': f'https://gnomic.cn/agentCenter/detail?schemeNo={agSn}&type=1',
              'accept-language': 'zh-CN,zh;q=0.9'
            }

            response = requests.request("GET", url, stream=True,
                                        headers=headers, params=params, verify=False,
                                        timeout=(5, 90))
            result_text = ""
            if response.status_code == 200:
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
                                    result_text += data_field_json.get("content")
                            elif event_field == "event" and data_field == "newline":
                                result_text += "\n"
        except Exception as e:
            logger.error(f"{tag_}: 服务器内部错误 {e}")
        return result_text


    def fun_gpt40(self, gpt_text, tag, agSn):
        # GPT-4.0
        msg = f"{tag}: 服务器睡着了,请稍后再试"
        try:
            _id = self.run_gpt40_put_prompt(gpt_text, tag, agSn)
            if _id:
                logger.info(f"{tag}: 创建任务成功")
                time.sleep(5)
                result = self.run_gpt40_get_data(_id, tag, agSn)
                if result:
                    logger.info(f"{tag}: 获取结果成功")
                    msg = result
                else:
                    logger.info(f"{tag}: 获取结果失败")
            else:
                logger.info(f"{tag}: 创建任务失败")
        except Exception as e:
            logger.error(f"{tag}: 服务器内部错误 {e}")
        return msg

    ###### gnomic PGT-4.0 #####



    def daily_api(self):
        # 每日一言
        tag = '每日一言'
        msg = f"{tag}: 服务器睡着了,请稍后再试"
        try:
            url = "https://oiapi.net/API/Daily"
            payload = {}
            headers = {
              'authority': 'oiapi.net',
              'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
              'accept-language': 'zh-CN,zh;q=0.9',
              'cache-control': 'max-age=0',
              'dnt': '1',
              'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
              'sec-ch-ua-mobile': '?0',
              'sec-ch-ua-platform': '"macOS"',
              'sec-fetch-dest': 'document',
              'sec-fetch-mode': 'navigate',
              'sec-fetch-site': 'cross-site',
              'sec-fetch-user': '?1',
              'upgrade-insecure-requests': '1',
              'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            """
            {
                  "code": 1,
                  "message": "lt's fun to have a challenge,isnt it？\n\n有挑战才有意思，不是么？",
                  "data": {
                      "en": "lt's fun to have a challenge,isnt it？",
                      "zh": "有挑战才有意思，不是么？",
                      "tts": "https://staticedu-wps.cache.iciba.com/audio/86f17926be6c081799afe9fa5fd512c3.mp3",
                      "image": "https://staticedu-wps.cache.iciba.com/image/32ba4c91b459c9ec5cc5209a40e35e4b.png"
                  }
              }
            """

            response = requests.request("GET", url, headers=headers, data=payload, timeout=30)
            r_code = response.status_code
            if r_code == 200:
                res_json = response.json()
                if res_json.get("code") == 1:
                    msg = res_json.get("message").replace("\n\n", "\n")
                else:
                    message = res_json.get("message")
                    log_msg = f"{tag}: response message:{message}"
                    logger.info(log_msg)
            else:
                r_code = response.status_code
                log_msg = f"{tag}: response status_code:{r_code}"
                logger.info(log_msg)
        except Exception as e:
            logger.error(f"{tag}: 服务器内部错误 {e}")
        return msg


    def link_ai_login(self):
        # linkai 登录
        token = ""
        tag = "linkai登录"
        msg = f"{tag}: 服务器睡着了,请稍后再试"
        try:
            url = "https://link-ai.tech/api/login"
            payload = f"username={self.linkai_user}&password={self.linkai_pwd}"
            headers = {
              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
              'Accept': 'application/json, text/plain, */*',
              'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
              'Accept-Encoding': 'gzip, deflate, br',
              'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
              'Authorization': 'Bearer',
              'Origin': 'https://link-ai.tech',
              'Connection': 'keep-alive',
              'Referer': 'https://link-ai.tech/console/factory',
              'Sec-Fetch-Dest': 'empty',
              'Sec-Fetch-Mode': 'cors',
              'Sec-Fetch-Site': 'same-origin'
            }
            response = requests.request("POST", url, headers=headers, data=payload, timeout=30)
            if response.status_code == 200:
                res_json = response.json()
                if res_json.get("code") == 200:
                    token = res_json.get("data").get("token")
                    if token:
                        log_msg = f"{tag}成功token: {token}"
                        self.linkai_authorization = f"Bearer {token}"
                        key = "linkai_authorization"
                        self.edit_config_json(key, self.linkai_authorization)
                        logger.info(log_msg)
                else:
                    message = res_json.get("message")
                    log_msg = f"{tag}失败:{message}"
                    logger.info(log_msg)
            else:
                r_code = response.status_code
                log_msg = f"{tag}失败 response status_code:{r_code}"
                logger.info(log_msg)
        except Exception as e:
            logger.error(f"{tag}: error: {e}")
        return token


    def linkai_sign_in(self):
        # linkai 每日签到
        tag = "linkai 每日签到"
        msg = f"{tag}: 服务器睡着了,请稍后再试"
        try:
            if self.linkai_authorization == "":
                logger.info("linkai token 不存在将执行登录操作")
                self.link_ai_login()
            for i in range(2):
                url = "https://chat.link-ai.tech/api/chat/web/app/user/sign/in"
                payload = {}
                headers = {
                  'Accept': 'application/json, text/plain, */*',
                  'Accept-Language': 'zh-CN,zh;q=0.9',
                  'Authorization': self.linkai_authorization,
                  'Connection': 'keep-alive',
                  'Referer': 'https://chat.link-ai.tech/home',
                  'Sec-Fetch-Dest': 'empty',
                  'Sec-Fetch-Mode': 'cors',
                  'Sec-Fetch-Site': 'same-origin',
                  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
                  'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
                  'sec-ch-ua-mobile': '?0',
                  'sec-ch-ua-platform': '"Linux"'
                }
                response = requests.request("GET", url, headers=headers, data=payload, timeout=20)
                if response.status_code == 200:
                    res_json = response.json()
                    if res_json.get("code") == 200:
                        score = res_json.get("data").get("score")
                        msg = f"{tag}成功获得积分:{score}"
                        logger.info(msg)
                    else:
                        message = res_json.get("message")
                        msg = f"{tag}失败:{message}"
                        logger.info(msg)
                    break
                else:
                    r_code = response.status_code
                    log_msg = f"{tag}失败 response status_code:{r_code}"
                    logger.info(log_msg)
                    # 重新获取 token
                    time.sleep(2)
                    self.link_ai_login()
                time.sleep(2)
        except Exception as e:
            log_msg = "{tag}: error: {e}"
            logger.error(log_msg)
        return msg

    def linkai_balance(self):
        # linkai 总积分查看
        tag = "linkai 总积分"
        msg = f"{tag}: 服务器睡着了,请稍后再试"
        try:
            if self.linkai_authorization == "":
                logger.info("linkai token 不存在将执行登录操作")
                self.link_ai_login()
            for i in range(2):
                url = "https://chat.link-ai.tech/api/chat/web/app/user/get/balance"
                payload = {}
                headers = {
                  'Accept': 'application/json, text/plain, */*',
                  'Accept-Language': 'zh-CN,zh;q=0.9',
                  'Authorization': self.linkai_authorization,
                  'Connection': 'keep-alive',
                  'Host': 'chat.link-ai.tech',
                  'Referer': 'https://chat.link-ai.tech/console/account',
                  'Sec-Fetch-Dest': 'empty',
                  'Sec-Fetch-Mode': 'cors',
                  'Sec-Fetch-Site': 'same-origin',
                  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
                  'sec-ch-ua': '"Chromium";v="117", "Not;A=Brand";v="8"',
                  'sec-ch-ua-mobile': '?0',
                  'sec-ch-ua-platform': '"Linux"'
                }
                response = requests.request("GET", url, headers=headers, data=payload, timeout=20)
                if response.status_code == 200:
                    res_json = response.json()
                    if res_json.get("code") == 200:
                        score = res_json.get("data").get("score")
                        msg = f"{tag}:{score}"
                        logger.info(msg)
                    else:
                        message = res_json.get("message")
                        log_msg = f"{tag}失败:{message}"
                        logger.info(log_msg)
                    break
                else:
                    r_code = response.status_code
                    log_msg = f"{tag}失败 response status_code:{r_code}"
                    logger.info(log_msg)
                    # 重新获取 token
                    time.sleep(2)
                    self.link_ai_login()
                time.sleep(2)
        except Exception as e:
            log_msg = f"{tag}: error: {e}"
            logger.error(log_msg)
        return msg


    def get_md5(self, input_str):
        # MD5
        return hashlib.md5(input_str.encode(encoding='UTF-8')).hexdigest()


    def get_uuid(self):
        # 生成uuid
        return str(uuid.uuid1()).replace("-", "")


    def mongo_con_parse(self):
        confing=self.mongodb_config
        conn = pymongo.MongoClient(confing['host'], confing['port'])
        conn = conn[confing['db']]
        if confing.get('user'):
            conn.authenticate(confing['user'], confing['pwd'])
        return conn

    def get_now_time(self, strftime_str="%Y-%m-%d %H:%M:%S"):
        # 获取当前时间
        now_ = datetime.datetime.now()
        now_date = now_.strftime(strftime_str)
        return now_date

    def create_cid(self):
        tag = "验证码识别CID"
        msg = f"{tag}: 服务器睡着了,请稍后再试"
        try:
            CID_TAB = "ocr_cids_tab"
            uuid_ = self.get_uuid()
            create_time = self.get_now_time(strftime_str="%Y-%m-%d %H:%M:%S")
            cid = self.get_md5(f"HHHhhhXXXxxx123~!@{uuid_}").upper()
            cid_dict = {"cid": cid, "status": 1, "type": "day", "create_time": create_time}
            db = self.mongo_con_parse()
            db.get_collection(CID_TAB).insert_one(cid_dict)
            msg = cid
            logger.info(msg)
        except Exception as e:
            log_msg = f"{tag}: error: {e}"
            logger.error(log_msg)
        return msg


