# chat/consumers.py
import json

from channels.auth import login
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketCon