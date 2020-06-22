from pymongo import MongoClient
from pubnub import Pubnub
import logging
import	datetime


def _callback(message):
    logging.info(message)

def _error(message):
	logging.info(message)

def sub_callback(message, channel):
	# print(channel)
	if "CV_Data" in message.keys():
		logging.basicConfig(filename='hydrobase_cv.log',level=logging.INFO)
		logging.info(message)
		db.cv_data.insert_one(message)
	elif 'sender' in message.keys():
		message_array  = []
		utc_datetime = datetime.datetime.utcnow()
		message['year'] = utc_datetime.year
		message['month'] = utc_datetime.month
		message['day'] = utc_datetime.day
		message['hour'] = utc_datetime.hour
		message['min'] = utc_datetime.minute
		message['sec'] = utc_datetime.second
		if 'EC' in message.keys():
			message['TDS'] = message['EC'].split(",")[1]
			message['PS'] = message['EC'].split(",")[2]
			message['EC'] = message['EC'].split(",")[0]

		device_id = message['sender']['device_id']
		message['device_id'] = device_id
		message.pop('sender', None)
		related_grows = db.grows.find({'device_id' : device_id})
		date_now = datetime.datetime(year=message['year'], month=message['month'], day=message['day'], \
			hour=message['hour'], minute=message['min'], second=message['sec'])
		for grow in related_grows:
			message_temp = message.copy()
			message_temp['grow_name'] = grow['grow_name']
			message_array.append(message_temp)
			data_points = db.data.find({'grow_name' : grow['grow_name']}).sort('_id', -1).limit(1)
			for data_point in data_points:
				date_last = datetime.datetime(year=data_point['year'], month=data_point['month'], day=data_point['day'], \
					hour=data_point['hour'], minute=data_point['min'], second=data_point['sec'])
				time_diff = date_now - date_last
		
		# insert in display
		logging.basicConfig(filename='hydrobase_display.log',level=logging.INFO)
		logging.info(message_array)
		db.display.insert_many(message_array)

		# insert in data db if last entry was more than 4 hpurs back
		if int(time_diff.seconds) >= 14400:
			logging.basicConfig(filename='hydrobase_data.log',level=logging.INFO)
			logging.info(message_array)
			db.data.insert_many(message_array)
		

if __name__ == '__main__':

	client = MongoClient('mongodb+srv://admin:admin@cluster0-4w9h4.gcp.mongodb.net/hydrosmart?retryWrites=true&w=majority')
	db = client['analytics-hydrosmart']

	#initialize the pubnub instance
	pubnub = Pubnub(publish_key='pub-c-662a8ff6-793e-497d-9793-1e870410e1c2', \
		subscribe_key='sub-c-825013ca-afef-11ea-af7b-9a67fd50bac3', secret_key='sec-c-NTc2ZjI4OGEtZjFlNy00Yzc3LWEwYTgtMWMzMjgwZWYwNDcy', \
		auth_key='auth-me-not')

	# Grant read, write and manage permissions to the pubnub instance that we initialized
	pubnub.grant(channel_group='hydrosmart', auth_key='auth-me-not',\
	 read=True, write=True, manage=True, ttl=0, callback=_callback, error=_error)

	# Subscribe to the channel group 'hydrobase' that contains the channels for all users to get the data 
	# coming in from different devices and put that into the DB
	pubnub.subscribe_group(channel_groups='hydrosmart', \
		callback=sub_callback, error=_error)