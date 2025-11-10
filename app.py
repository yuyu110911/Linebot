# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 00:54:06 2025

@author: 鬱鬱
"""

import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    AudioSendMessage, VideoSendMessage, PostbackEvent,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate,
    PostbackTemplateAction, URITemplateAction,
    CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn,
    LocationSendMessage
)

app = Flask(__name__)

# --- 從環境變數讀取金鑰（Render 後台設定） ---
CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")
CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET", "")
if not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET:
    raise RuntimeError("請在環境變數設定 LINE_CHANNEL_ACCESS_TOKEN / LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# ---- 工具函式：把訊息分批送（一次最多 5 則） ----
def reply_and_push_in_chunks(event, messages):
    """先用 reply 回前 5 則，其餘用 push 分批送。"""
    if not isinstance(messages, list):
        messages = [messages]

    head = messages[:5]
    tail = messages[5:]

    # reply 第一批
    if head:
        line_bot_api.reply_message(event.reply_token, head)

    # push 其餘批次
    if tail:
        user_id = event.source.user_id  # 需要使用者已加好友
        for i in range(0, len(tail), 5):
            line_bot_api.push_message(user_id, tail[i:i+5])


# ---- Webhook ----
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# ---- 依照請求動態組 baseurl（Render 會有 https 網域）----
def get_baseurl():
    # request.url_root 例如：https://xxx.onrender.com/
    return request.url_root.rstrip('/') + '/static/'


# ---- 文字訊息處理 ----
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text.strip()

    if mtext == '@認識動物':
        baseurl = get_baseurl()
        try:
            messages = [
                TextSendMessage(text="這是驢的叫聲 🎵"),
                AudioSendMessage(original_content_url=baseurl + 'donkey.mp3', duration=17000),

                TextSendMessage(text="這是豬的叫聲 🎵"),
                AudioSendMessage(original_content_url=baseurl + 'pig.mp3', duration=7000),

                TextSendMessage(text="這是老虎的叫聲 🎵"),
                AudioSendMessage(original_content_url=baseurl + 'Tiger.mp3', duration=7000),

                TextSendMessage(text="這是牛的叫聲 🎵"),
                AudioSendMessage(original_content_url=baseurl + 'cow.mp3', duration=6000),
            ]
            reply_and_push_in_chunks(event, messages)

        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'發生錯誤！{e}'))

    elif mtext == '@動物園影片':
        baseurl = get_baseurl()
        try:
            messages = [
                TextSendMessage(text="這是動物介紹影片，請欣賞"),
                VideoSendMessage(
                    original_content_url=baseurl + 'videoplayback.mp4',
                    preview_image_url=baseurl + 'panda.jpg'   # 建議加預覽圖
                )
            ]
            reply_and_push_in_chunks(event, messages)

        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'發生錯誤！{e}'))

    elif mtext == '@動物介紹':
        baseurl = get_baseurl()
        try:
            message = TemplateSendMessage(
                alt_text='轉盤樣板',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url=baseurl + 'ma.jpg',
                            title='這是羊的圖片',
                            text='第一個轉盤樣板',
                            actions=[
                                # 如果要顯示在聊天室，用 MessageTemplateAction
                                MessageTemplateAction(
                                    label='文字訊息一',
                                    text='小羊真可愛'
                                ),
                                URITemplateAction(
                                    label='連結台北市立動物園網頁',
                                    uri='https://www.zoo.gov.taipei/'
                                ),
                                # Postback 是回給你程式，不會顯示在聊天室
                                PostbackTemplateAction(
                                    label='回傳訊息一',
                                    data='小羊是白色的喔!'   # 在 handle_postback 讀取
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url=baseurl + 'panda.jpg',
                            title='這是熊貓的圖片',
                            text='第二個轉盤樣板',
                            actions=[
                                MessageTemplateAction(
                                    label='文字訊息二',
                                    text='熊貓喜歡吃的是竹子'
                                ),
                                URITemplateAction(
                                    label='連結台北市立動物園網頁',
                                    uri='https://www.zoo.gov.taipei/'
                                ),
                                PostbackTemplateAction(
                                    label='回傳訊息二',
                                    data='熊貓有很深的黑眼圈!!!'
                                )
                            ]
                        ),
                        CarouselColumn(
                            thumbnail_image_url=baseurl + '刺蝟.jpeg',
                            title='這是刺蝟的圖片',
                            text='第三個轉盤樣板',
                            actions=[
                                MessageTemplateAction(
                                    label='文字訊息三',
                                    text='刺蝟生氣時會扎手!不要碰'
                                ),
                                URITemplateAction(
                                    label='連結台北市立動物園網頁',
                                    uri='https://www.zoo.gov.taipei/'
                                ),
                                PostbackTemplateAction(
                                    label='回傳訊息三',
                                    data='刺蝟的肚子很軟!?'
                                )
                            ]
                        ),
                    ]
                )
            )
            reply_and_push_in_chunks(event, [message])

        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'發生錯誤！{e}'))

    elif mtext == '@動物園地點':
        try:
            message = LocationSendMessage(
                title='台北市立動物園',
                address='台北市文山區新光路二段30號',
                latitude=24.9985,
                longitude=121.5800
            )
            reply_and_push_in_chunks(event, [message])

        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'發生錯誤！{e}'))

    #else:
        # 其他訊息回覆
        #line_bot_api.reply_message(event.reply_token, TextSendMessage(text='指令：@認識動物 / @動物園影片 / @動物介紹 / @動物園地點'))


# ---- Postback 事件處理（按下 Carousel 的 Postback 會來這裡）----
@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    # 讓使用者看得到他點了什麼
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'{data}'))


if __name__ == '__main__':
    # Render 會提供 $PORT 環境變數，需監聽 0.0.0.0
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
