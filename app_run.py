from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import *
import os
from dbModel import *

app = Flask(__name__)

# get enviroment variables
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
# YOUR_CHANNEL_ACCESS_TOKEN = 'A1bAwdQQlNuXHr39n9FlIWJUNU9o9eKp7PgBRgcZvylPXrxYL2rL/EzFqyElim1EvlaNx0Q2TK8Q0NhS6rWh/UQf+zH5gFdhDa4gFQf30aTWBkHLF7bqM+qRSDB4BdA+tG4oEj3KnnIpzxynrfZwKgdB04t89/1O/w1cDnyilFU='
# YOUR_CHANNEL_SECRET = '4fa1cd3db4950fafcdcc4b10fc4abd78'

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# declare a dictionary
dict = {
    '50blue_name': '50嵐',
    '50blue_image': 'https://sites.google.com/site/50lanksu00/_/rsrc/1415903484528/config/customLogo.gif?revision=9', 
    '50nlue_recipe': 'https://bearteach.com/wp-content/uploads/02-149.jpg', 
    'yifang_name': '一芳 台灣水果茶',
    'yifang_image': 'https://foodtracer.taipei.gov.tw/Backend/upload/company/54591495/54591495_img2.jpg',
    'yifang_recipe': 'http://www.yifangtea.com.tw/upload/menu/1901020908450000001.jpg'
}

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
    
    if msg == '菜單':
        DrinkVenders = TemplateSendMessage(
            alt_text='DrinkVenders',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=dict['50blue_image'],
                        text=dict['50blue_name'],
                        actions=[
                            URIAction(
                                label='菜單',
                                uri=dict['50nlue_recipe']
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=dict['yifang_image'],
                        text=dict['yifang_name'],
                        actions=[
                            URIAction(
                                label='菜單',
                                uri=dict['yifang_recipe']
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, DrinkVenders)
    
    elif msg == '揪團':
        SelectDrinkVender = TemplateSendMessage(
            alt_text='SelectDrinkVender',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=dict['50blue_image'],
                        text=dict['50blue_name'],
                        actions=[
                            PostbackAction(
                                label='選擇',
                                text='我要喝 {0}}'.format(dict['50blue_name']),
                                data='action=SelectDrinkVender&item=50blue'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=dict['yifang_image'],
                        text=dict['yifang_name'],
                        actions=[
                            PostbackAction(
                                label='選擇',
                                text='我要喝 {0}'.format(dict['yifang_name']),
                                data='action=SelectDrinkVender&item=yifang'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, SelectDrinkVender)

    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=msg))

@handler.add(PostbackEvent)
def handle_postback(event):
    # postback message: action=%s&item=%s
    pattern = re.compile(r"(\S+)=(\S+)&(\S+)=(\S+)")
    match = pattern.match(event.postback.data)

    if match.group(2) == 'SelectDrinkVender':
        ConfirmGroupOrder = TemplateSendMessage(
            alt_text='ConfirmGroupOrder',
            template=ConfirmTemplate(
                text='您確定要揪[{0}]嗎？'.format(match.group(4)),
                actions=[
                    PostbackAction(
                        label='是',
                        text='是',
                        data='action=LaunchGroupOrder&item={0}}'.format(match.group(4))
                    ),
                    MessageAction(
                        label='否',
                        text='否'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, ConfirmGroupOrder)

    elif match.group(2) == 'LaunchGroupOrder':

        # query userID of all my friends from database
        ResultSet = UserData.query.all()

        # creat a list of userID before broadcast drink order message
        userID = []
        for _userid in ResultSet:
            userID.append(_userid)

        # Get launcher's profile
        try:
            profile = line_bot_api.get_profile(event.source.user_id)
        except LineBotApiError as e:
            print(e.status_code)
            print(e.error.message)
            print(e.error.details)

        drinkVender = '{0}_name'.format(match.group(4))
        broadcastMessage = '哈囉! {0}口渴想要喝{1}，有人要跟嗎？'.format('profile.display_name', dict[drinkVender])

        confirmLaunch = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url=dict[drinkVender],
                text='請選擇動作...',
                actions=[
                    PostbackAction(
                        label='postback',
                        text='postback text',
                        data='action=buy&itemid=1'
                    ),
                    MessageAction(
                        label='message',
                        text='message text'
                    ),
                    URIAction(
                        label='uri',
                        uri='http://example.com/'
                    )
                ]
            )
        )

        line_bot_api.multicast(userID, 
            messages=[
                TextSendMessage(text=broadcastMessage),

            ]
        )

    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.data))

@handler.add(FollowEvent)
def handle_follow(event):
    print ("FollowEvent occured.")
    user_id = event.source.user_id

    try:
        profile = line_bot_api.get_profile(user_id)
    except LineBotApiError as e:
        print(e.status_code)
        print(e.error.message)
        print(e.error.details)

    # check if the database already has this user
    result = UserData.query.filter_by(UserID=user_id).first()
    
    # if not, add it to database
    if result is None:
        print ("FollowEvent: Unregistered User")
        insert_data = UserData(DisplayName=profile.display_name
                             , UserID=profile.user_id
                             , PictureURL=profile.picture_url
                             , StatusMessage=profile.status_message
                              )
        db.session.add(insert_data)
        db.session.commit()

    print ("FollowEvent: " + profile.display_name + " added you as a friend.")

@handler.add(UnfollowEvent)
def handle_unfollow(event):
    print ("UnfollowEvent occured.")
    user_id = event.source.user_id

    # check if the database already has this user
    result = UserData.query.filter_by(UserID=user_id).first()

    # if yes, delete it to database
    if not result is None: 
        print ("UnfollowEvent: Registered User. Proceed to delete it from database")
        db.session.delete(result)
        db.session.commit()

    print ("UnfollowEvent: You are blocked by UserID: " + user_id)

# to avoid to let Heroku allocate port dynamically and then it will generate
# error r10 (boot timeout). Here to appoint port directly.
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
