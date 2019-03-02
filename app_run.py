from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import *
import os, re
from dbModel import *
import datetime

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
    '50blue_recipe': 'https://bearteach.com/wp-content/uploads/02-149.jpg', 
    'yifang_name': '一芳 台灣水果茶',
    'yifang_image': 'https://foodtracer.taipei.gov.tw/Backend/upload/company/54591495/54591495_img2.jpg',
    'yifang_recipe': 'http://www.yifangtea.com.tw/upload/menu/1901020908450000001.jpg'
}

ORDER_EXPIRED_TIME = 120  # minute

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
    
    msg = event.message.text
    # message: 團號/尺寸/品名/甜度/冰塊
    pattern = re.compile(r"(\S+)/(\S+)/(\S+)/(\S+)/(\S+)")
    match = pattern.match(msg)
    
    if msg == '招喚菜單':
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
    
    elif msg == '我要揪團':
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
                                data='action=SelectDrinkVender&item=yifang'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, SelectDrinkVender)

    elif not match is None:

        # Check if the order_id is correct or not.
        ExpireDatetime = datetime.datetime.now() - datetime.timedelta(minutes=ORDER_EXPIRED_TIME)
        ResultSet1 = OrderList.query.\
                filter(OrderList.Id==match.group(1)).\
                filter(OrderList.CreateDate > ExpireDatetime).\
                first()

        # Check if there is repeated orderer in the same order.
        ResultSet2 = OrderDetail.query.\
                filter(OrderDetail.Order_Index==match.group(1)).\
                filter(OrderDetail.Orderer==event.source.user_id).\
                first()

        if ResultSet1 is None:
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text='團號 {0} 有誤，可能是錯誤輸入或者是該團號之揪團已過期。'.format(match.group(1))
                    )
            )
        elif not ResultSet1 is None and ResultSet2 is None:
            try:
                # message: 團號/尺寸/品名/甜度/冰塊
                insert_data = OrderDetail(Order_Index = match.group(1)
                                        , Orderer = event.source.user_id
                                        , Drink_Size = match.group(2)
                                        , Drink_Item = match.group(3)
                                        , Drink_Ice = match.group(4)
                                        , Drink_Sugar = match.group(5)
                                         )
                db.session.add(insert_data)
                db.session.commit()

                ResultSet = UserData.query.\
                    filter(UserData.UserID==event.source.user_id).\
                    first()

                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text='點單訊息收到，已統計至 {0} 的揪團中，後續狀況請洽詢揪團發起人。'.\
                        format(ResultSet.DisplayName)
                    )
                )

            except LineBotApiError as e:
                print(e.status_code)
                print(e.error.message)
                print(e.error.details)



    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=msg))

@handler.add(PostbackEvent)
def handle_postback(event):
    # postback message: action=%s&item=%s
    pattern = re.compile(r"(\S+)=(\S+)&(\S+)=(\S+)")
    match = pattern.match(event.postback.data)

    if match.group(2) == 'SelectDrinkVender':
        drinkVender = '{0}_name'.format(match.group(4))
        ConfirmGroupOrder = TemplateSendMessage(
            alt_text='ConfirmGroupOrder',
            template=ConfirmTemplate(
                text='您確定要揪 {0} 嗎？'.format(dict[drinkVender]),
                actions=[
                    PostbackAction(
                        label='是',
                        data='action=LaunchGroupOrder&item={0}'.format(match.group(4))
                    ),
                    PostbackAction(
                        label='否',
                        data='action=None&item=False'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, ConfirmGroupOrder)

    elif match.group(2) == 'LaunchGroupOrder':

        # Get launcher's profile
        try:
            profile = line_bot_api.get_profile(event.source.user_id)
        except LineBotApiError as e:
            print(e.status_code)
            print(e.error.message)
            print(e.error.details)

        # Check if there is repeated order.
        # The order created within 4 hours is valid.
        ExpireDatetime = datetime.datetime.now() - datetime.timedelta(minutes=ORDER_EXPIRED_TIME)
        ResultSet = OrderList.query.\
            filter(OrderList.Creator==profile.user_id).\
            filter(OrderList.CreateDate > ExpireDatetime).\
            first()

        if not ResultSet is None:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="你曾在四小時以內揪團過了，請查看揪團狀況。"))
        else:

            # query userID of all my friends from database
            ResultSet = UserData.query.all()

            # creat a list of userID before broadcast drink order message
            userIDs = []
            for _userid in ResultSet:
                userIDs.append(_userid.UserID)


            drinkVender = '{0}_name'.format(match.group(4))
            recipeURL = '{0}_recipe'.format(match.group(4))
            broadcastMessage = '哈囉! {0}口渴想要喝{1}，有人要跟嗎？'.\
                format(profile.display_name, dict[drinkVender])

            # Insert a new drink order into database 'OrderList'.
            insert_data = OrderList(Creator=profile.user_id
                                  , DrinkVender=dict[drinkVender]
                                  )
            db.session.add(insert_data)
            db.session.commit()

            ResultSet = OrderList.query.\
                filter(OrderList.Creator==profile.user_id).\
                filter(OrderList.CreateDate > ExpireDatetime).\
                first()

            # PostbackAction carry order list id.
            confirmLaunch = TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url=dict[drinkVender],
                    text='請選擇動作或者是忽視這則訊息',
                    actions=[
                        URIAction(
                            label='菜單',
                            uri=dict[recipeURL]
                        ),
                        PostbackAction(
                            label='跟團',
                            data='action=FollowOrder&itemid={0}'.format(ResultSet.Id)
                        )
                    ]
                )
            )

            line_bot_api.multicast(userIDs, 
                messages=[
                    TextSendMessage(text=broadcastMessage),
                    confirmLaunch
                ]
            )

    elif match.group(2) == 'FollowOrder':

        # Check this order whether expired or not.
        ExpireDatetime = datetime.datetime.now() - datetime.timedelta(minutes=ORDER_EXPIRED_TIME)
        ResultSet = OrderList.query.\
                filter(OrderList.Id==match.group(4)).\
                filter(OrderList.CreateDate > ExpireDatetime).\
                first()

        if ResultSet is None:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="這次的揪團已經過期，請追蹤其他的揪團。"))
        else:
            line_bot_api.reply_message(
                event.reply_token, 
                TextSendMessage(text='''
                    請按照下面的字串格式進行點單： 
                    團號/尺寸/品名/甜度/冰塊
                    Ex: 1/大/珍珠奶茶/半糖/去冰
                    '''
                ),
                TextSendMessage(text='你所選擇的揪團團號是: {0}'.format(match.group(4))
                )
            )

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
