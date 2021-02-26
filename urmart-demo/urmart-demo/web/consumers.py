import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'] # get room_name via scorp['url_route']['kwargs']
        print("self.room_name:", self.room_name)
        self.room_group_name = 'chat_%s'%self.room_name # group name only allow letters, digits, hyphens and period
        print("self.room_group_name:", self.room_group_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)( # add channel_name to room_gorup_name
            self.room_group_name, 
            self.channel_name 
        )
        print(f"add {self.channel_name} to group {self.room_group_name}.")
        # add specific.987e7bacf20d406b82a2a1397a7a9f51!442cd384aeae4d47a2f72b71ce24eae6 to group chat_lobby.

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)( # remove channel_name from room_group_name
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from Websocket
    def receive(self, text_data):
        print("consumer received a message")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # # for now, it does not broadcast
        # self.send(text_data=json.dumps({
        #     'message': message,
        # }))
        async_to_sync(self.channel_layer.group_send)( # group send with type required
            self.room_group_name,
            {
                'type': 'chat_message', 
                'message': message
            }
        )
    # Receive message from room_group_name
    def chat_message(self, event):
        print("consumer chat message box listen event is ON.")
        message = event['message'] # via event to receive message from channel layer
        self.send(text_data=json.dumps({
            'message': message,
        }))
    
    def send_from_view(self, msg):
        async_to_sync(self.channel_layer.group_send)( # group send with type required
            self.room_group_name,
            {
                'type': 'chat_message', 
                'message': msg
            }
        )

class UrmartConsumer(WebsocketConsumer):
    
    def connect(self):
        self.group_name = "urmart_group"
        async_to_sync(self.channel_layer.group_add)( # add channel_name to room_gorup_name
            self.group_name, 
            self.channel_name 
        )
        print(f"add {self.channel_name} to group {self.group_name}.")
        self.accept()
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)( # remove channel_name from room_group_name
            self.group_name,
            self.channel_name
        )
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.channel_layer.group_send)( # group send with type required
            self.group_name,
            {
                'type': 'urmart_message',  # specify function name for a call
                'message': message
            }
        )
    def urmart_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message,
        }))
    