# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 19:45:24 2025

@author: 鬱鬱
"""

from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, AudioSendMessage, VideoSendMessage, PostbackEvent, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn,LocationSendMessage

line_bot_api = LineBotApi('K8HmKWzCG9SY8CCARvhIRUQogYMipLHyskI87esFcFh89PIymhWQeC3LfEv9OSB50U2F3v05FYEdfI4sZ9FIuTAHl0UThfNhJBSemZe4CPvRyWZukDlra2oLPkoJMlF5JqUP1xs6wgCnQZaSetcCVgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('dd3e255491f797dd4af308fabcac2f18')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

baseurl = 'https://unrepined-jeanette-unhefted.ngrok-free.dev/static/'  #靜態檔案網址

@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data  # 這裡會拿到 data='小羊是白色的喔!'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f'{data}')
    )
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    if mtext == '@認識動物':
        try:
            message = [
                TextSendMessage(text="這是驢的叫聲，請聆聽 🎶"),
                AudioSendMessage(
                original_content_url=baseurl + 'donkey.mp3',  #聲音檔置於static資料夾
                duration=17000  #聲音長度17秒
                ),
                TextSendMessage(text="這是豬的叫聲，請聆聽 🎶"),
                AudioSendMessage(
                original_content_url=baseurl + 'pig.mp3',  #聲音檔置於static資料夾
                duration=7000  #聲音長度7秒
                ),
                TextSendMessage(text="這是老虎的叫聲，請聆聽 🎶"),
                AudioSendMessage(
                original_content_url=baseurl + 'Tiger.mp3',  #聲音檔置於static資料夾
                duration=7000  #聲音長度7秒
                ),
                TextSendMessage(text="這是牛的叫聲，請聆聽 🎶"),
                AudioSendMessage(
                original_content_url=baseurl + 'cow.mp3',  #聲音檔置於static資料夾
                duration=6000  #聲音長度6秒
                )
                ]
            #line_bot_api.reply_message(event.reply_token, message)
            # 回覆前五個（避免超出限制）
            line_bot_api.reply_message(event.reply_token, message[:5])
            # 再用 push_message 另外發送剩下的
            user_id = event.source.user_id
            for i in range(5, len(message), 5):
                line_bot_api.push_message(user_id, message[i:i+5])
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    elif mtext == '@動物園影片':
        try:
            message =[
                TextSendMessage(text="這是動物介紹影片，請欣賞 "),
                VideoSendMessage(
                original_content_url=baseurl + 'videoplayback.mp4',  #影片檔置於static資料夾
                preview_image_url=baseurl + 'panda.jpg'
            )
            ]
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    
    elif mtext == '@動物介紹':
        try:
            message = [
                TemplateSendMessage(
                alt_text='轉盤樣板',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url = baseurl + 'ma.jpg',
                            title='這是羊的圖片',
                            text='第一個轉盤樣板',
                            actions=[
                                MessageTemplateAction(
                                    label='文字訊息一',
                                    text='小羊真可愛'
                                ),
                                URITemplateAction(
                                    label='連結台北市立動物園網頁',
                                    uri='https://www.zoo.gov.taipei/'
                                ),
                                PostbackTemplateAction(
                                    label='回傳訊息一',
                                    data='小羊是白色的喔!'
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
                        )
                    ]
                )
            )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
    elif mtext == '@動物園地點':
        try:
            message = LocationSendMessage(
                title = '台北市立動物園',
                address='台北市文山區新光路二段30號',
                latitude=24.9985,   # 緯度
                longitude=121.5800  # 經度
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
           line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

if __name__ == '__main__':
    app.run()
