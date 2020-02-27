# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.core.cache import cache

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        if cache.has_key(self.room_name):
            room_data = cache.get(self.room_name)
            room_data['numClient'] -= 1
            if room_data['numClient'] == 0:
                cache.delete(self.room_name)
            else:
                cache.set(self.room_name, room_data)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        message = text_data_json['message']
        re_action = None
        re_message = None
        room_data = None
        if cache.has_key(self.room_name):
            room_data = cache.get(self.room_name)
        else:
            room_data = {'numClient':0}
            cache.set(self.room_name, room_data)
        print(room_data)
        # Send message to room group
        if action == 'message':
            #print('消息')
            re_action = 'message'
            re_message = message
        elif action == 'create or join':
            #print('创建/加入')
            if room_data['numClient'] == 0:
                re_action = 'created'
                message = {'room':self.room_name, 'socketID':'wangfang'}
                room_data['numClient'] += 1
                cache.set(self.room_name, room_data)
            elif room_data['numClient'] == 1:
                re_action = 'joined'
                message = {'room':self.room_name, 'socketID':'fangyuan'}
                room_data['numClient'] +=1
                cache.set(self.room_name, room_data)
            else:
                re_action = 'full'
                message = 'full'
        elif action == 'ipaddr':
            print('ipaddr')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'action': re_action,
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        action = event['action']
        message = event['message']
        print(message)
        #print(event)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'action': action,
            'message': message
        }))