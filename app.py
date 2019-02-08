from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os
# from Modules.DefinedMessages import *

app = Flask(__name__)

# get enviroment variables
# YOUR_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
# YOUR_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
YOUR_CHANNEL_ACCESS_TOKEN = 'A1bAwdQQlNuXHr39n9FlIWJUNU9o9eKp7PgBRgcZvylPXrxYL2rL/EzFqyElim1EvlaNx0Q2TK8Q0NhS6rWh/UQf+zH5gFdhDa4gFQf30aTWBkHLF7bqM+qRSDB4BdA+tG4oEj3KnnIpzxynrfZwKgdB04t89/1O/w1cDnyilFU='
YOUR_CHANNEL_SECRET = '4fa1cd3db4950fafcdcc4b10fc4abd78'

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# callback function. Line will send 'POST' message to 
# webhook url whenever user send chatbot some messages.
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print (event)
    
    msg = event.message.text
    
    if msg == '揪團':
        line_bot_api.reply_message(event.reply_token,DefinedMessages.DrinkVenders)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))

    
    

# to avoid to let Heroku allocate port dynamically and then it will generate
# error r10 (boot timeout). Here to appoint port directly.
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


class DefinedMessages:
    DrinkVenders = TemplateSendMessage(
        alt_text='DrinkVenders',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://sites.google.com/site/50lanksu00/_/rsrc/1415903484528/config/customLogo.gif?revision=9',
                    text='50嵐',
                    actions=[
                        URIAction(
                            label='菜單',
                            uri='https://bearteach.com/wp-content/uploads/02-149.jpg'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://foodtracer.taipei.gov.tw/Backend/upload/company/54591495/54591495_img2.jpg',
                    text='一芳 台灣水果茶',
                    actions=[
                        URIAction(
                            label='菜單',
                            uri='http://www.yifangtea.com.tw/upload/menu/1901020908450000001.jpg'
                        )
                    ]
                )
            ]
        )
    )