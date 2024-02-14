### chatgpt-on-wechat  插件

```
目前有
linkai积分签到
linkai总积分查看
配合定时任务timetask 运行  完美!!!
翻译   // 逆向破解有道翻译接口   翻译+要翻译的内容 + 是连接起来不是添加+这个符号
每日一言

gnomic ai api破解直接调用api 供机器人使用
# !!! 注意 该网站gpt40已经收费 使用不了是正常的
https://www.gnomic.cn/?216639
gpt40
绘画咒语
中药大师
起名大师
解名大师

gpt35 也是破解的某网站 可免费使用

消息添加盲水印    使用 https://github.com/guofei9987/text_blind_watermark

```

```
[INFO]
发送关键词执行对应操作
输入 '开启消息盲水印'， 消息文本开启添加盲水印
输入 '关闭消息盲水印'， 消息文本关闭添加盲水印
输入 'linkai签到'， 进行签到
输入 'linkai积分'， 进行总积分获取
输入 '翻译+内容'， 进行有道翻译
输入 '人品'， 随机获取人品分数
输入 '验证码识别cid'，获取验证码识别cid 
输入 'gpt35+内容'， 使用gpt35模型进行回答
输入 '触发验证码发送'，触发gnomic平台验证码发送 
输入 '验证码上传+手机验证码'，gnomic手机验证码上传并登录 
输入 'gpt40+内容'， 使用gpt40模型进行回答
输入 '每日一言'，每日一言 
输入 '绘画咒语'，mj绘画咒语 
输入 '中药大师'，中药大师 
输入 '起名大师'，起名大师 
输入 '解名大师'，解名大师 

```

```
克隆代码到插件目录 或者

安装仓库源记录的插件：#installp xinuo
安装指定仓库的插件：#installp https://github.com/wang-zhibo/xinuo.git 
安装依赖
pip install -r requirements.txt 

cp config.example.json config.json

修改 config.json 文件
填入 帐号密码


{
    "linkai_user": "xxx",    linkai 帐号
    "linkai_pwd": "xxx",     linkai 密码
    "linkai_authorization": "", linkai token   自动登录获取
    "gpt40_authorization": "Bearer xxx",   gnomic 网站的 token   可使用机器人 触发登录短信 ==操作自动设置
    "gpt40_abc12": "fbb1681d275c91435bd758ee85719880",   gnomic 网站的浏览器指纹   固定
    "gpt40_website_key": "huizhihuyu201707",             gnomic 网站的 加密key     固定
    "gpt40_phone": "xxx",                                gnomic 网站的 手机号
    "watermark_encryption_status": false,                             是否开启消息添加盲水印
    "watermark_encryption_password": "gm.zhibo.wang@gmail.com",       盲水印 加密密码
    "watermark_encryption_watermark": "github.com/wang-zhibo/xinuo/"  要添加的盲水印文本
}

```

```
#scanp

#enablep xinuo


log

[INFO][2023-11-28 10:04:16][Xinuo.py:214] - linkai token 不存在将执行登录操作
[INFO][2023-11-28 10:04:17][Xinuo.py:146] - linkai登录成功token: xxxxxxxxxxxxxxxxxxxxxxxx
[INFO][2023-11-28 10:04:17][Xinuo.py:240] - linkai总积分:23411
[INFO][2023-11-28 10:04:17][wechat_channel.py:191] - [WX] sendMsg=Reply(type=TEXT, content=[🫶] linkai积分
linkai总积分:23411), receiver=@1d6231b36d7eb3b0fc35d5458ceae3478113062683aa812c12f69790017d0655
[INFO][2023-11-28 10:04:38][Xinuo.py:194] - linkai签到失败 req content:{"success":false,"code":834,"message":"今日已签到，请明日再来！","data":null}
[INFO][2023-11-28 10:04:39][wechat_channel.py:191] - [WX] sendMsg=Reply(type=TEXT, content=[🫶] linkai签到
linkai签到失败:今日已签到，请明日再来！), receiver=@1d6231b36d7eb3b0fc35d5458ceae3478113062683aa812c12f69790017d0655



[INFO][2023-12-15 16:20:47][Xinuo.py:89] - 有道翻译: 翻译一只桔黄色的猫
[INFO][2023-12-15 16:20:47][Xinuo.py:227] - 有道翻译: [[{'tgt': 'An orange cat', 'src': '一只桔黄色的猫', 'srcPronounce': 'yī zhī jié huáng sè demāo'}]]
[INFO][2023-12-15 16:20:47][wechat_channel.py:191] - [WX] sendMsg=Reply(type=TEXT, content=[🫶] 翻译
原始本文:一只桔黄色的猫
翻译后文本:An orange cat), receiver=@ee2a5dbeb0895072ec88005c9bcc36c68af9a959847ff3b1c325fbbcb3bc5449




1: 
input->
    linkai签到
output->
    linkai签到失败:今日已签到，请明日再来！
    linkai签到成功获得积分:123

2:
input->
    linkai积分
output->
    linkai积分
    linkai总积分:10405


gnomic 网站登录
bot 触发验证码发送
[DEBUG][2024-02-01 14:50:22][plugin_manager.py:187] - Plugin BANWORDS triggered by event Event.ON_DECORATE_REPLY
[DEBUG][2024-02-01 14:50:22][chat_channel.py:280] - [WX] ready to send reply: Reply(type=TEXT, content=[🤖] 触发验证码发送
成功


bot 验证码上传865830
[INFO][2024-02-01 14:50:55][Xinuo.py:531] - gnomic 登录: sms_code 865830
[INFO][2024-02-01 14:50:55][Xinuo.py:533] - gnomic 登录: url https://gnomic.cn/api/auth/oauth2/token?mobile=APP-SMS@xxxxx&grant_type=mobile&code=865830&scope=server
[INFO][2024-02-01 14:50:55][Xinuo.py:566] - gnomic 登录: response {"sub":"xxxx","iss":"https://www.baidu.com","active":true,"token_type":"Bearer","client_id":"app","access_token":"xxxx","refresh_token":"xxx","aud":["app"],"nbf":171110255.794000000,"scope":["server"],"id":111,"exp":1702229855.794000000,"expires_in":09600,"iat":1706770255.794000000,"jti":"xxx","username":"xxx"}
[INFO][2024-02-01 14:50:55][Xinuo.py:571] - gnomic 登录: 获取access_token 成功
[INFO][2024-02-01 14:50:55][Xinuo.py:449] - 修改配置文件: key gpt40_authorization, value: Bearer xxxxx
[DEBUG][2024-02-01 14:50:55][plugin_manager.py:192] - Plugin XINUO breaked event Event.ON_HANDLE_CONTEXT
[DEBUG][2024-02-01 14:50:55][chat_channel.py:170] - [WX] ready to decorate reply: Reply(type=TEXT, content=验证码上传
gnomic 登录: 成功)
[DEBUG][2024-02-01 14:50:55][plugin_manager.py:187] - Plugin BANWORDS triggered by event Event.ON_DECORATE_REPLY
[DEBUG][2024-02-01 14:50:55][chat_channel.py:280] - [WX] ready to send reply: Reply(type=TEXT, content=[🤖] 验证码上传
gnomic 登录: 成功


bot gpt40你是什么模型

[DEBUG][2024-02-01 15:02:38][Xinuo.py:77] - [xinuo] on_handle_context. content: gpt40你是什么模型
[INFO][2024-02-01 15:02:38][Xinuo.py:154] - GPT-4.0: 你是什么模型
[INFO][2024-02-01 15:02:39][Xinuo.py:711] - GPT-4.0: 创建任务成功
[ERROR][2024-02-01 15:02:44][Xinuo.py:701] - GPT-4.0获取结果: 服务器内部错误 can only concatenate str (not "NoneType") to str
[INFO][2024-02-01 15:02:44][Xinuo.py:715] - GPT-4.0: 获取结果成功
[DEBUG][2024-02-01 15:02:44][plugin_manager.py:192] - Plugin XINUO breaked event Event.ON_HANDLE_CONTEXT
[DEBUG][2024-02-01 15:02:44][chat_channel.py:170] - [WX] ready to decorate reply: Reply(type=TEXT, content=GPT-4.0
我是基于OpenAI的GPT-4版本模型。)
[DEBUG][2024-02-01 15:02:44][plugin_manager.py:187] - Plugin BANWORDS triggered by event Event.ON_DECORATE_REPLY
[DEBUG][2024-02-01 15:02:44][chat_channel.py:280] - [WX] ready to send reply: Reply(type=TEXT, content=[🤖] GPT-4.0
我是基于OpenAI的GPT-4版本模型。 

bot gpt35你是什么模型

[DEBUG][2024-02-01 15:03:27][Xinuo.py:77] - [xinuo] on_handle_context. content: gpt35你是什么模型
[INFO][2024-02-01 15:03:27][Xinuo.py:122] - GPT-3.5: 你是什么模型
[DEBUG][2024-02-01 15:03:33][plugin_manager.py:192] - Plugin XINUO breaked event Event.ON_HANDLE_CONTEXT
[DEBUG][2024-02-01 15:03:33][chat_channel.py:170] - [WX] ready to decorate reply: Reply(type=TEXT, content=GPT-3.5
我是一个基于OpenAI GPT-3.5模型的AI机器人，使用自然语言处理技术和深度学习算法来生成答案。我的训练数据来自于互联网上的大量文本，并经过了机器学习算法的学习和优化，可以根据用户的提问和输入进行智能回复。虽然我可以生成一些令人印象深刻的答案，但我仍然有很多限制，需要不断学习和改进。)
[DEBUG][2024-02-01 15:03:33][plugin_manager.py:187] - Plugin BANWORDS triggered by event Event.ON_DECORATE_REPLY
[DEBUG][2024-02-01 15:03:33][chat_channel.py:280] - [WX] ready to send reply: Reply(type=TEXT, content=[🤖] GPT-3.5
我是一个基于OpenAI GPT-3.5模型的AI机器人，使用自然语言处理技术和深度学习算法来生成答案。我的训练数据来自于互联网上的大量文本，并经过了机器学习算法的学习和优化，可以根据用户的提问和输入进行智能回复。虽然我可以生成一些令人印象深刻的答案，但我仍然有很多限制，需要不断学习和改进
-----------------------------------


bot 开启消息盲水印

[DEBUG][2024-02-07 10:34:44][Xinuo.py:94] - [xinuo] on_handle_context. session_id: @7a2684574e3f76a424e1cde2c68529d98b3a7286bd0c3b6e435b125618341904, content: 开启消息盲水印
[INFO][2024-02-07 10:34:44][Xinuo.py:289] - 消息已经开启添加盲水印正在处理...
[DEBUG][2024-02-07 10:34:44][plugin_manager.py:192] - Plugin XINUO breaked event Event.ON_HANDLE_CONTEXT
[DEBUG][2024-02-07 10:34:44][chat_channel.py:172] - [WX] ready to decorate reply: Reply(type=TEXT, content=盲水印:
 已开启)
[DEBUG][2024-02-07 10:34:44][plugin_manager.py:187] - Plugin BANWORDS triggered by event Event.ON_DECORATE_REPLY
[DEBUG][2024-02-07 10:34:44][chat_channel.py:282] - [WX] ready to send reply: Reply(type=TEXT, content=[🤖] 盲水印:
 已开启


bot 关闭消息盲水印

[DEBUG][2024-02-07 10:34:51][Xinuo.py:94] - [xinuo] on_handle_context. session_id: @7a2684574e3f76a424e1cde2c68529d98b3a7286bd0c3b6e435b125618341904, content: 关闭消息盲水印
[INFO][2024-02-07 10:34:51][Xinuo.py:508] - 修改配置文件: key watermark_encryption_status, value: False
[DEBUG][2024-02-07 10:34:51][plugin_manager.py:192] - Plugin XINUO breaked event Event.ON_HANDLE_CONTEXT
[DEBUG][2024-02-07 10:34:51][chat_channel.py:172] - [WX] ready to decorate reply: Reply(type=TEXT, content=盲水印:
 已关闭)
[DEBUG][2024-02-07 10:34:51][plugin_manager.py:187] - Plugin BANWORDS triggered by event Event.ON_DECORATE_REPLY
[DEBUG][2024-02-07 10:34:51][chat_channel.py:282] - [WX] ready to send reply: Reply(type=TEXT, content=[🤖] 盲水印:
 已关闭



```
