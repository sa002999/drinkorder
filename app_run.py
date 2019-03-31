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

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

ORDER_EXPIRED_TIME = 120  # minute

# declare a dictionary
dict = {
    '50blue_name': '50嵐',
    '50blue_image': 'https://sites.google.com/site/50lanksu00/_/rsrc/1415903484528/config/customLogo.gif?revision=9', 
    '50blue_recipe': 'https://bearteach.com/wp-content/uploads/02-149.jpg', 
    '50blue_branch': '平鎮中豐店',
    '50blue_branch_phone': '03-419-5500',
    '50blue_branch_note': '滿400元外送',

    'yifang_name': '一芳 台灣水果茶',
    'yifang_image': 'https://foodtracer.taipei.gov.tw/Backend/upload/company/54591495/54591495_img2.jpg',
    'yifang_recipe': 'http://www.yifangtea.com.tw/upload/menuen/1803311733250000001.jpg',
    'yifang_branch': '中壢龍岡店',
    'yifang_branch_phone': '03-465-8989',
    'yifang_branch_note': '滿?元外送',

    'tp-tea_name': '茶湯會',
    'tp-tea_image': 'https://tw.tp-tea.com/images/logo_h.png',
    'tp-tea_recipe': 'https://tw.tp-tea.com/menu/index.php?index_m1_id=17',
    'tp-tea_branch': '中壢龍岡店',
    'tp-tea_branch_phone': '03-465-9090',
    'tp-tea_branch_note': '滿?元外送',

    '85cafe_name': '85度C',
    '85cafe_image': 'https://upload.wikimedia.org/wikipedia/zh/thumb/c/cd/Logo_85度C.png/200px-Logo_85度C.png',
    '85cafe_recipe': 'https://www.85cafe.com/Product.php?datatid=9',
    '85cafe_branch': '平鎮中豐店',
    '85cafe_branch_phone': '03-419-2246',
    '85cafe_branch_note': '滿300元外送',

    'coco-tea_name': 'CoCo都可',
    'coco-tea_image': 'https://foodtracer.taipei.gov.tw/Backend/upload/company/12915964/12915964_img2.png',
    'coco-tea_recipe': 'http://www.coco-tea.com/product-price',
    'coco-tea_branch': '平鎮金陵店',
    'coco-tea_branch_phone': '03-457-5299',
    'coco-tea_branch_note': '滿?元外送',

    'chingshin_name': '清心',
    'chingshin_image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTPCGQU9jpsTWuV-PefjZeiArzqXnawYGXf1gDVqhukDRiYaboI',
    'chingshin_recipe': 'https://img.apoarea.tw/uploads/20171207095138_25.jpg',
    'chingshin_branch': '平鎮金隆店',
    'chingshin_branch_phone': '03-459-6611',
    'chingshin_branch_note': '滿?元外送'
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
    
    msg = event.message.text

    # message: 團號/尺寸/品名/甜度/冰塊
    pattern = re.compile(r"(\S+)/(\S+)/(\S+)/(\S+)/(\S+)")
    match = pattern.match(msg)

    # message: 團號7
    pattern = re.compile(r"(\S+)(\d+)")
    match1 = pattern.match(msg)
    
    if msg == '我要揪團':

        # ready to launch order message
        SelectDrinkVender = FlexSendMessage(
            alt_text='SelectDrinkVender',
            contents=
                CarouselContainer(
                    contents=[
                        BubbleContainer(
                            # image
                            hero=ImageComponent(
                                url=dict['50blue_image'],
                                size='full',
                                aspect_ratio='20:13',
                                aspect_mode='cover'
                            ),
                            # body
                            body=BoxComponent(
                                layout='vertical',
                                spacing='sm',
                                contents=[
                                    # branch
                                    TextComponent(
                                        text=dict['50blue_branch'], 
                                        size='xl', 
                                        weight='bold', 
                                        color='#000000'
                                    ),
                                    # telphone
                                    BoxComponent(
                                        layout='horizontal',
                                        contents=[
                                            TextComponent(
                                                text='電話: ', 
                                                size='lg', 
                                                weight='bold', 
                                                color='#000000'
                                            ),
                                            TextComponent(
                                                text=dict['50blue_branch_phone'], 
                                                size='lg', 
                                                weight='bold', 
                                                color='#000000'
                                            )
                                        ]
                                    ),
                                    # note
                                    TextComponent(
                                        text=dict['50blue_branch_note'], 
                                        size='xxs', 
                                        margin="md", 
                                        color='#FF0000'
                                    )
                                ]
                            ),
                            footer=BoxComponent(
                                layout='vertical',
                                spacing='sm',
                                contents=[
                                    # recipe
                                    ButtonComponent(
                                        style='secondary',
                                        action=URIAction(
                                            label='菜單', 
                                            uri=dict['50blue_recipe']
                                        )
                                    ),
                                    # launch order
                                    ButtonComponent(
                                        style='primary',
                                        action=PostbackAction(
                                            label='揪團', 
                                            data='action=SelectDrinkVender&item=50blue'
                                        )
                                    )
                                ]
                            )
                        ),
                        BubbleContainer(
                            # image
                            hero=ImageComponent(
                                url=dict['yifang_image'],
                                size='full',
                                aspect_ratio='20:13',
                                aspect_mode='cover'
                            ),
                            # body
                            body=BoxComponent(
                                layout='vertical',
                                spacing='sm',
                                contents=[
                                    # branch
                                    TextComponent(
                                        text=dict['yifang_branch'], 
                                        size='xl', 
                                        weight='bold', 
                                        color='#000000'
                                    ),
                                    # telphone
                                    BoxComponent(
                                        layout='horizontal',
                                        contents=[
                                            TextComponent(
                                                text='電話: ', 
                                                size='lg', 
                                                weight='bold', 
                                                color='#000000'
                                            ),
                                            TextComponent(
                                                text=dict['yifang_branch_phone'], 
                                                size='lg', 
                                                weight='bold', 
                                                color='#000000'
                                            )
                                        ]
                                    ),
                                    # note
                                    TextComponent(
                                        text=dict['yifang_branch_note'], 
                                        size='xxs', 
                                        margin="md", 
                                        color='#FF0000'
                                    )
                                ]
                            ),
                            footer=BoxComponent(
                                layout='vertical',
                                spacing='sm',
                                contents=[
                                    # recipe
                                    ButtonComponent(
                                        style='secondary',
                                        action=URIAction(
                                            label='菜單', 
                                            uri=dict['yifang_recipe']
                                        )
                                    ),
                                    # launch order
                                    ButtonComponent(
                                        style='primary',
                                        action=PostbackAction(
                                            label='揪團', 
                                            data='action=SelectDrinkVender&item=yifang'
                                        )
                                    )
                                ]
                            )
                        ),
                        BubbleContainer(
                            # image
                            hero=ImageComponent(
                                url=dict['tp-tea_image'],
                                size='full',
                                aspect_ratio='20:13',
                                aspect_mode='cover'
                            ),
                            # body
                            body=BoxComponent(
                                layout='vertical',
                                spacing='sm',
                                contents=[
                                    # branch
                                    TextComponent(
                                        text=dict['tp-tea_branch'], 
                                        size='xl', 
                                        weight='bold', 
                                        color='#000000'
                                    ),
                                    # telphone
                                    BoxComponent(
                                        layout='horizontal',
                                        contents=[
                                            TextComponent(
                                                text='電話: ', 
                                                size='lg', 
                                                weight='bold', 
                                                color='#000000'
                                            ),
                                            TextComponent(
                                                text=dict['tp-tea_branch_phone'], 
                                                size='lg', 
                                                weight='bold', 
                                                color='#000000'
                                            )
                                        ]
                                    ),
                                    # note
                                    TextComponent(
                                        text=dict['tp-tea_branch_note'], 
                                        size='xxs', 
                                        margin="md", 
                                        color='#FF0000'
                                    )
                                ]
                            ),
                            footer=BoxComponent(
                                layout='vertical',
                                spacing='sm',
                                contents=[
                                    # recipe
                                    ButtonComponent(
                                        style='secondary',
                                        action=URIAction(
                                            label='菜單', 
                                            uri=dict['tp-tea_recipe']
                                        )
                                    ),
                                    # launch order
                                    ButtonComponent(
                                        style='primary',
                                        action=PostbackAction(
                                            label='揪團', 
                                            data='action=SelectDrinkVender&item=tp-tea'
                                        )
                                    )
                                ]
                            )
                        ),
                        # BubbleContainer(
                        #     # image
                        #     hero=ImageComponent(
                        #         url=dict['85cafe_image'],
                        #         size='full',
                        #         aspect_ratio='20:13',
                        #         aspect_mode='cover'
                        #     ),
                        #     # body
                        #     body=BoxComponent(
                        #         layout='vertical',
                        #         spacing='sm',
                        #         contents=[
                        #             # branch
                        #             TextComponent(
                        #                 text=dict['85cafe_branch'], 
                        #                 size='xl', 
                        #                 weight='bold', 
                        #                 color='#000000'
                        #             ),
                        #             # telphone
                        #             BoxComponent(
                        #                 layout='horizontal',
                        #                 contents=[
                        #                     TextComponent(
                        #                         text='電話: ', 
                        #                         size='lg', 
                        #                         weight='bold', 
                        #                         color='#000000'
                        #                     ),
                        #                     TextComponent(
                        #                         text=dict['85cafe_branch_phone'], 
                        #                         size='lg', 
                        #                         weight='bold', 
                        #                         color='#000000'
                        #                     )
                        #                 ]
                        #             ),
                        #             # note
                        #             TextComponent(
                        #                 text=dict['85cafe_branch_note'], 
                        #                 size='xxs', 
                        #                 margin="md", 
                        #                 color='#FF0000'
                        #             )
                        #         ]
                        #     ),
                        #     footer=BoxComponent(
                        #         layout='vertical',
                        #         spacing='sm',
                        #         contents=[
                        #             # recipe
                        #             ButtonComponent(
                        #                 style='secondary',
                        #                 action=URIAction(
                        #                     label='菜單', 
                        #                     uri=dict['85cafe_recipe']
                        #                 )
                        #             ),
                        #             # launch order
                        #             ButtonComponent(
                        #                 style='primary',
                        #                 action=PostbackAction(
                        #                     label='揪團', 
                        #                     data='action=SelectDrinkVender&item=85cafe'
                        #                 )
                        #             )
                        #         ]
                        #     )
                        # ),
                        BubbleContainer(
                            # image
                            hero=ImageComponent(
                                url=dict['coco-tea_image'],
                                size='full',
                                aspect_ratio='20:13',
                                aspect_mode='cover'
                            ),
                            # body
                            body=BoxComponent(
                                layout='vertical',
                                spacing='sm',
                                contents=[
                                    # branch
                                    TextComponent(
                                        text=dict['coco-tea_branch'], 
                                        size='xl', 
                                        weight='bold', 
                                        color='#000000'
                                    ),
                                    # telphone
                                    BoxComponent(
                                        layout='horizontal',
                                        contents=[
                                            TextComponent(
                                                text='電話: ', 
                                                size='lg', 
                                                weight='bold', 
                                                color='#000000'
                                            ),
                                            TextComponent(
                                                text=dict['coco-tea_branch_phone'], 
                                                size='lg', 
                                                weight='bold', 
                                                color='#000000'
                                            )
                                        ]
                                    ),
                                    # note
                                    TextComponent(
                                        text=dict['coco-tea_branch_note'], 
                                        size='xxs', 
                                        margin="md", 
                                        color='#FF0000'
                                    )
                                ]
                            ),
                            footer=BoxComponent(
                                layout='vertical',
                                spacing='sm',
                                contents=[
                                    # recipe
                                    ButtonComponent(
                                        style='secondary',
                                        action=URIAction(
                                            label='菜單', 
                                            uri=dict['coco-tea_recipe']
                                        )
                                    ),
                                    # launch order
                                    ButtonComponent(
                                        style='primary',
                                        action=PostbackAction(
                                            label='揪團', 
                                            data='action=SelectDrinkVender&item=coco-tea'
                                        )
                                    )
                                ]
                            )
                        ),
                        BubbleContainer(
                            # image
                            hero=ImageComponent(
                                url=dict['chingshin_image'],
                                size='full',
                                aspect_ratio='20:13',
                                aspect_mode='cover'
                            ),
                            # body
                            body=BoxComponent(
                                layout='vertical',
                                spacing='sm',
                                contents=[
                                    # branch
                                    TextComponent(
                                        text=dict['chingshin_branch'], 
                                        size='xl', 
                                        weight='bold', 
                                        color='#000000'
                                    ),
                                    # telphone
                                    BoxComponent(
                                        layout='horizontal',
                                        contents=[
                                            TextComponent(
                                                text='電話: ', 
                                                size='lg', 
                                                weight='bold', 
                                                color='#000000'
                                            ),
                                            TextComponent(
                                                text=dict['chingshin_branch_phone'], 
                                                size='lg', 
                                                weight='bold', 
                                                color='#000000'
                                            )
                                        ]
                                    ),
                                    # note
                                    TextComponent(
                                        text=dict['chingshin_branch_note'], 
                                        size='xxs', 
                                        margin="md", 
                                        color='#FF0000'
                                    )
                                ]
                            ),
                            footer=BoxComponent(
                                layout='vertical',
                                spacing='sm',
                                contents=[
                                    # recipe
                                    ButtonComponent(
                                        style='secondary',
                                        action=URIAction(
                                            label='菜單', 
                                            uri=dict['chingshin_recipe']
                                        )
                                    ),
                                    # launch order
                                    ButtonComponent(
                                        style='primary',
                                        action=PostbackAction(
                                            label='揪團', 
                                            data='action=SelectDrinkVender&item=chingshin'
                                        )
                                    )
                                ]
                            )
                        )
                    ]
                )
                   
        )

        line_bot_api.reply_message(event.reply_token, SelectDrinkVender)

    elif msg == '誰在開團':
        ExpireDatetime = datetime.datetime.utcnow() - datetime.timedelta(minutes=ORDER_EXPIRED_TIME)
        ResultSet = OrderList.query.\
            filter(OrderList.CreateDate > ExpireDatetime).\
            all()

        if ResultSet is None:
            line_bot_api.reply_message(
                event.reply_token, 
                TextSendMessage(text='目前尚無發起中的訂單。'))
        else:
            orderlist_string = '[團號]\t[發起人]\t[飲料]'
            for result in ResultSet:
                ResultSet1 = UserData.query.\
                    filter(UserData.UserID==result.Creator).\
                    first()
                orderlist_string = orderlist_string + \
                    '\n{0}\t{1}\t{2}'.format(result.Id, ResultSet1.DisplayName, result.DrinkVender)

            line_bot_api.reply_message(
                event.reply_token, 
                TextSendMessage(text=orderlist_string))

            line_bot_api.push_message(
                event.source.user_id, 
                TextSendMessage(text="你要查看哪個揪團目前的統計情況呢?\n請輸入 團號X"))

            line_bot_api.push_message(
                event.source.user_id, 
                TextSendMessage(text="Ex: 團號7"))
        
    # check drinks order
    elif not match is None:

        # Check if the order_id is correct or not.
        ExpireDatetime = datetime.datetime.utcnow() - datetime.timedelta(minutes=ORDER_EXPIRED_TIME)
        ResultSet1 = OrderList.query.\
                filter(OrderList.Id==match.group(1)).\
                filter(OrderList.CreateDate > ExpireDatetime).\
                first()

        # # Check if there is repeated orderer in the same order.
        # ResultSet2 = OrderDetail.query.\
        #         filter(OrderDetail.Order_Index==match.group(1)).\
        #         filter(OrderDetail.Orderer==event.source.user_id).\
        #         first()

        if ResultSet1 is None:
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text='團號 {0} 有誤，可能是錯誤輸入或者是該團號之揪團已過期。'.format(match.group(1))
                    )
            )
        # elif not ResultSet1 is None and ResultSet2 is None:
        else:
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

                ResultSet = OrderList.query.\
                    filter(OrderList.Id==match.group(1)).\
                    first()

                ResultSet = UserData.query.\
                    filter(UserData.UserID==ResultSet.Creator).\
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

    # look for order detail
    elif not match1 is None:
        if match1.group(1) == '團號':

            # Check if the order_id is correct or not.
            ExpireDatetime = datetime.datetime.utcnow() - datetime.timedelta(minutes=ORDER_EXPIRED_TIME)
            ResultSet1 = OrderList.query.\
                    filter(OrderList.Id==match1.group(2)).\
                    filter(OrderList.CreateDate > ExpireDatetime).\
                    first()

            ResultSet2 = OrderDetail.query.\
                filter(OrderDetail.Order_Index==match1.group(2)).\
                all()

            if ResultSet1 is None:
                line_bot_api.reply_message(
                    event.reply_token, 
                    TextSendMessage(text='團號 {0} 有誤，可能是錯誤輸入或者是該團號之揪團已過期。'.format(match1.group(2))
                    )
                )
            elif not ResultSet1 is None or len(ResultSet2) is 0:
                line_bot_api.reply_message(
                    event.reply_token, 
                    TextSendMessage(text='目前仍沒有人跟團，被邊緣中...'))
            else:
                orderdetail_string = ''
                for result in ResultSet2:
                    ResultSet1 = UserData.query.\
                        filter(UserData.UserID==result.Orderer).\
                        first()
                    orderdetail_string = orderdetail_string + '{0}, {1}, {2}, {3}, {4}\n'.\
                        format(ResultSet1.DisplayName, result.Drink_Size, result.Drink_Item, \
                            result.Drink_Ice, result.Drink_Sugar)

                line_bot_api.reply_message(
                    event.reply_token, 
                    TextSendMessage(text=orderdetail_string.rstrip()))
        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=msg))

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
        ExpireDatetime = datetime.datetime.utcnow() - datetime.timedelta(minutes=ORDER_EXPIRED_TIME)
        ResultSet = OrderList.query.\
            filter(OrderList.Creator==profile.user_id).\
            filter(OrderList.CreateDate > ExpireDatetime).\
            first()

        if not ResultSet is None:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="你曾在過去兩小時以內揪團過了，請查看揪團狀況。"))
        else:

            # query userID of all my friends from database
            ResultSet = UserData.query.all()

            # creat a list of userID before broadcast drink order message
            userIDs = []
            for _userid in ResultSet:
                userIDs.append(_userid.UserID)


            drinkVender = '{0}_name'.format(match.group(4))
            recipeURL = '{0}_recipe'.format(match.group(4))
            drinkVenderImage = '{0}_image'.format(match.group(4))
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
                    thumbnail_image_url=dict[drinkVenderImage],
                    text='請選擇動作或者是忽視這則訊息',
                    actions=[
                        URIAction(
                            label='菜單',
                            uri='{0}'.format(dict[recipeURL])
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
        ExpireDatetime = datetime.datetime.utcnow() - datetime.timedelta(minutes=ORDER_EXPIRED_TIME)
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
                TextSendMessage(text='請按照下面的字串格式進行點單：\n' +
                                     '團號/尺寸/品名/甜度/冰塊'
                )
            )
            line_bot_api.push_message(
                event.source.user_id, 
                TextSendMessage(text='Ex: 1/大/珍珠奶茶/半糖/去冰'))
            line_bot_api.push_message(
                event.source.user_id, 
                TextSendMessage(text='你所選擇的揪團團號是: {0}'.format(match.group(4))))


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
