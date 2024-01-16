from channels.consumer import AsyncConsumer , SyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

class mysyncconsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("websocket connnected...........",event)
        print("channel layer:" , self.channel_layer)
        print("channel name:" , self.channel_name)
        await self.channel_layer.group_add("programmers",self.channel_name)
        await self.send({
            'type':'websocket.accept'
        })
    async def websocket_receive(self,event):
        print("websocket received.........",event['text'])
        print("type of msg is...",type(event['text']))
        await self.channel_layer.group_send(
            'programmers',{
            'type':'chat.message',
            'message':event['text']
            }
        )

    async def chat_message(self,event):
        print("Event....",event)
        print("type of actual message is : " ,type(event["message"]))
        await self.send({
            'type':'websocket.send',
            'text':event["message"]
        })
    async def websocket_disconnect(self,event):
        print("websocket disconnected.......",event)
        print("channel layer:" , self.channel_layer)
        print("channel name:" , self.channel_name)
        await self.channel_layer.group_discard("programmers",self.channel_name)
        raise StopConsumer()
