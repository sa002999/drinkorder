from linebot.models import *


class Messages():
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
	    'yifang_recipe': 'http://www.yifangtea.com.tw/upload/menu/1903130958040000001.jpg',
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
	    '85cafe_branch': '中壢龍岡店',
	    '85cafe_branch_phone': '03-436-2300',
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

	# ready to launch order message
	SelectDrinkVender = FlexSendMessage(
		alt_text='SelectDrinkVender',
		contents=[
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
			                    TextComponent(text=dict['50blue_branch'], size='xl', weight='bold', color='#000000'),
			                    # telphone
			                    BoxComponent(
			                        layout='horizontal',
			                        contents=[
			                        	TextComponent(text='電話: ', size='lg', weight='bold', color='#000000'),
			                        	TextComponent(text=dict['50blue_branch_phone'], size='lg', weight='bold', color='#000000')
			                        ]
			                    ),
			                    # note
			                    TextComponent(text=dict['50blue_branch_note'], size='xxs', margin="md", color='#FF0000')
			                ]
			            ),
			            footer=BoxComponent(
			                layout='vertical',
			                spacing='sm',
			                contents=[
			                    # recipe
			                    ButtonComponent(
			                        style='secondary',
			                        action=URIAction(label='菜單', uri=dict['50blue_recipe'])
			                    ),
			                    # launch order
		                    	ButtonComponent(
			                        style='primary',
			                        action=PostbackAction(label='揪團', data='action=SelectDrinkVender&item=50blue')
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
			                    TextComponent(text=dict['yifang_branch'], size='xl', weight='bold', color='#000000'),
			                    # telphone
			                    BoxComponent(
			                        layout='horizontal',
			                        contents=[
			                        	TextComponent(text='電話: ', size='lg', weight='bold', color='#000000'),
			                        	TextComponent(text=dict['yifang_branch_phone'], size='lg', weight='bold', color='#000000')
			                        ]
			                    ),
			                    # note
			                    TextComponent(text=dict['yifang_branch_note'], size='xxs', margin="md", color='#FF0000')
			                ]
			            ),
			            footer=BoxComponent(
			                layout='vertical',
			                spacing='sm',
			                contents=[
			                    # recipe
			                    ButtonComponent(
			                        style='secondary',
			                        action=URIAction(label='菜單', uri=dict['yifang_recipe'])
			                    ),
			                    # launch order
		                    	ButtonComponent(
			                        style='primary',
			                        action=PostbackAction(label='揪團', data='action=SelectDrinkVender&item=yifang')
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
			                    TextComponent(text=dict['tp-tea_branch'], size='xl', weight='bold', color='#000000'),
			                    # telphone
			                    BoxComponent(
			                        layout='horizontal',
			                        contents=[
			                        	TextComponent(text='電話: ', size='lg', weight='bold', color='#000000'),
			                        	TextComponent(text=dict['tp-tea_branch_phone'], size='lg', weight='bold', color='#000000')
			                        ]
			                    ),
			                    # note
			                    TextComponent(text=dict['tp-tea_branch_note'], size='xxs', margin="md", color='#FF0000')
			                ]
			            ),
			            footer=BoxComponent(
			                layout='vertical',
			                spacing='sm',
			                contents=[
			                    # recipe
			                    ButtonComponent(
			                        style='secondary',
			                        action=URIAction(label='菜單', uri=dict['tp-tea_recipe'])
			                    ),
			                    # launch order
		                    	ButtonComponent(
			                        style='primary',
			                        action=PostbackAction(label='揪團', data='action=SelectDrinkVender&item=tp-tea')
			                    )
			                ]
			            )
			        ),
			        BubbleContainer(
						# image
			            hero=ImageComponent(
			                url=dict['85cafe_image'],
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
			                    TextComponent(text=dict['85cafe_branch'], size='xl', weight='bold', color='#000000'),
			                    # telphone
			                    BoxComponent(
			                        layout='horizontal',
			                        contents=[
			                        	TextComponent(text='電話: ', size='lg', weight='bold', color='#000000'),
			                        	TextComponent(text=dict['85cafe_branch_phone'], size='lg', weight='bold', color='#000000')
			                        ]
			                    ),
			                    # note
			                    TextComponent(text=dict['85cafe_branch_note'], size='xxs', margin="md", color='#FF0000')
			                ]
			            ),
			            footer=BoxComponent(
			                layout='vertical',
			                spacing='sm',
			                contents=[
			                    # recipe
			                    ButtonComponent(
			                        style='secondary',
			                        action=URIAction(label='菜單', uri=dict['85cafe_recipe'])
			                    ),
			                    # launch order
		                    	ButtonComponent(
			                        style='primary',
			                        action=PostbackAction(label='揪團', data='action=SelectDrinkVender&item=85cafe')
			                    )
			                ]
			            )
			        ),
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
			                    TextComponent(text=dict['coco-tea_branch'], size='xl', weight='bold', color='#000000'),
			                    # telphone
			                    BoxComponent(
			                        layout='horizontal',
			                        contents=[
			                        	TextComponent(text='電話: ', size='lg', weight='bold', color='#000000'),
			                        	TextComponent(text=dict['coco-tea_branch_phone'], size='lg', weight='bold', color='#000000')
			                        ]
			                    ),
			                    # note
			                    TextComponent(text=dict['coco-tea_branch_note'], size='xxs', margin="md", color='#FF0000')
			                ]
			            ),
			            footer=BoxComponent(
			                layout='vertical',
			                spacing='sm',
			                contents=[
			                    # recipe
			                    ButtonComponent(
			                        style='secondary',
			                        action=URIAction(label='菜單', uri=dict['coco-tea_recipe'])
			                    ),
			                    # launch order
		                    	ButtonComponent(
			                        style='primary',
			                        action=PostbackAction(label='揪團', data='action=SelectDrinkVender&item=coco-tea')
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
			                    TextComponent(text=dict['chingshin_branch'], size='xl', weight='bold', color='#000000'),
			                    # telphone
			                    BoxComponent(
			                        layout='horizontal',
			                        contents=[
			                        	TextComponent(text='電話: ', size='lg', weight='bold', color='#000000'),
			                        	TextComponent(text=dict['chingshin_branch_phone'], size='lg', weight='bold', color='#000000')
			                        ]
			                    ),
			                    # note
			                    TextComponent(text=dict['chingshin_branch_note'], size='xxs', margin="md", color='#FF0000')
			                ]
			            ),
			            footer=BoxComponent(
			                layout='vertical',
			                spacing='sm',
			                contents=[
			                    # recipe
			                    ButtonComponent(
			                        style='secondary',
			                        action=URIAction(label='菜單', uri=dict['chingshin_recipe'])
			                    ),
			                    # launch order
		                    	ButtonComponent(
			                        style='primary',
			                        action=PostbackAction(label='揪團', data='action=SelectDrinkVender&item=chingshin')
			                    )
			                ]
			            )
			        )
				]
			)
		]
	)
