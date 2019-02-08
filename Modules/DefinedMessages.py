from linebot.models import *

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

# print (DefinedMessages.DrinkVenders.template.columns[0].text)