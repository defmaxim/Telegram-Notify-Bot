#нужные модули
import telebot
from telebot import types
import time
import psycopg2
bot = telebot.TeleBot('5214967905:AAGjM1jR_j4uCQMb_fOoMGmFFj1yyLhQt0w')
DB_URI="postgres://rdpthcxbvnlydf:542b009ab6a9863f835f02efa62d7d93d280438f5f488c90c1a86f70c87e8d6d@ec2-52-48-159-67.eu-west-1.compute.amazonaws.com:5432/d62hams8jsvq4a"
#работа с базой данных PostgreSQL
conn=psycopg2.connection(DB_URI,sslmode="require")
cursor=conn.cursor()
def db_table_val(us_id, text):
	cursor.execute('INSERT INTO users (us_id, text) VALUES (?, ?)',
				   (us_id, text))
	conn.commit()


def db_table_val1(text):
	cursor.execute('INSERT INTO users (text) VALUES(?)', (text,))
	conn.commit()

def sql_carry(us_id,text):
	check = cursor.execute('SELECT * FROM users WHERE us_id=?', (us_id,))
	if check.fetchone() is None:
		db_table_val(us_id, text)
	else:
		delete = """DELETE from users where us_id = ?"""
		cursor.execute(delete, (us_id,))
		conn.commit()
		db_table_val(us_id, text)
#supporst arr
msup=['/min','/day','/hour','/help','/start','/n','/notify']
sup=[1]
sup1=[]
sup2=['1','2','3','4']
sup3=[2,3,4]
sup4=[5,6,7,8,9,0]


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
	bot.send_message(message.chat.id, 'Вас приветствует NotifyBot(бот-напоминание)\n'
										   'Бот предназначен для создания напоминаний.\n'
										   'Чтобы начать введите /notify или /n')
@bot.message_handler(commands=['n', 'notify'])
def request_0(message):
	bot.send_message(message.from_user.id, 'О чем напомнить?')
	bot.register_next_step_handler(message,request)
def request(message):
	req_ = message.text
	text = req_
	us_id = message.from_user.id
	sql_carry(us_id,text)

	if True:
		ed_iden = 'Выберите единицу времени:'
		keyboard = types.InlineKeyboardMarkup()
		key_hour = types.InlineKeyboardButton(text='Минуты', callback_data='min')
		key_min = types.InlineKeyboardButton(text='Часы', callback_data='hour')
		key_day = types.InlineKeyboardButton(text='Дни', callback_data='days')
		keyboard.add(key_min, key_hour, key_day)
		bot.send_message(message.chat.id, text=ed_iden, reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: True)
def choose_1(call):
	if call.data=='min':
		bot.send_message(call.message.chat.id,'Введите целое количество минут.')
		bot.register_next_step_handler(call.message, mins)
	elif call.data=='hour':
		bot.send_message(call.message.chat.id,'Введите целое количество часов.')
		bot.register_next_step_handler(call.message, hour)
	elif call.data == 'days':
		bot.send_message(call.message.chat.id, 'Введите целое количество дней.')
		bot.register_next_step_handler(call.message, day)
def mins(call):
	us_id=call.from_user.id
	for value in cursor.execute('SELECT * FROM users WHERE us_id=?', (us_id,)):
		reqq=value[1]
	text = call.text
	if text=='1':
		end='минуту'
	elif int(text) in sup3:
		end='минуты'
	elif int(text)>4 and int(text)<20 or int(text)//10>1 and int(text)%10 in sup4:
		end='минут'
	else:
		end='минуты'
	kolvo=int(text)
	bot.send_message(call.chat.id, 'Я напомню вам о '+str(reqq)+' через '+str(kolvo)+' '+str(end)+'!')
	time.sleep(kolvo*60)
	bot.send_message(call.chat.id,text=reqq)
def hour(call):
	us_id=call.from_user.id
	for value in cursor.execute('SELECT * FROM users WHERE us_id=?', (us_id,)):
		reqq=value[1]
	text = call.text
	if text == '1':
		end = 'час'
	elif int(text) in sup3:
		end = 'часа'
	elif int(text) > 4 and int(text) < 20 or int(text) // 10 > 1 and int(text) % 10 in sup4:
		end = 'часов'
	else:
		end = 'часов'
	kolvo = int(text)
	bot.send_message(call.chat.id, 'Я напомню вам о ' + str(reqq) + ' через ' + str(kolvo) + ' ' + str(end) + '!')
	time.sleep(kolvo * 60 * 60)
	bot.send_message(call.chat.id, text=reqq)
def day(call):
	us_id=call.from_user.id
	for value in cursor.execute('SELECT * FROM users WHERE us_id=?', (us_id,)):
		reqq=value[1]
	text = call.text
	if text == '1':
		end = 'день'
	elif int(text) in sup3:
		end = 'дня'
	elif int(text) > 4 and int(text) < 20 or int(text) // 10 > 1 and int(text) % 10 in sup4:
		end = 'дней'
	else:
		end = 'дней'
	kolvo = int(text)
	bot.send_message(call.chat.id,'Я напомню вам о ' + str(reqq) + ' через ' + str(kolvo) + ' ' + str(end) + '!')
	time.sleep(kolvo * 24 * 60 * 60)
	bot.send_message(call.chat.id, text=reqq)
bot.infinity_polling()
