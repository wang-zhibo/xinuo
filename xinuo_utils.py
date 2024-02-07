#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author: zhibo.wang
# E-mail: gm.zhibo.wang@gmail.com
# Date  :
# Desc  :


from config import global_config
from bridge.reply import Reply, ReplyType
from plugins.event import EventContext, EventAction
from text_blind_watermark import TextBlindWatermark2


class Util:
    @staticmethod
    def is_admin(e_context: EventContext) -> bool:
        """
        判断消息是否由管理员用户发送
        :param e_context: 消息上下文
        :return: True: 是, False: 否
        """
        context = e_context["context"]
        if context["isgroup"]:
            actual_user_id = context.kwargs.get("msg").actual_user_id
            for admin_user in global_config["admin_users"]:
                if actual_user_id and actual_user_id in admin_user:
                    return True
            return False
        else:
            return context["receiver"] in global_config["admin_users"]

    @staticmethod
    def set_reply_text(content: str, e_context: EventContext, level: ReplyType = ReplyType.ERROR):
        reply = Reply(level, content)
        e_context["reply"] = reply
        e_context.action = EventAction.BREAK_PASS

    @staticmethod
    def encryption_text(input_str: str, password: str, watermark: str) -> str:
        """
        文本添加盲水印
        :input_str: 要添加盲水印的文本
        :password: 盲水印密码
        :watermark: 盲水印文本
        """
        text_with_wm = input_str
        try:
            text_blind_wm = TextBlindWatermark2(password=password)
            text_with_wm = text_blind_wm.embed(text=input_str, watermark=watermark)
        except Exception as e:
            print(f"encryption_text error: {e}")
            pass
        return text_with_wm

