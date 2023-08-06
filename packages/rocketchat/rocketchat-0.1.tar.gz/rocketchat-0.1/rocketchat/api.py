from rocketchat.calls.message_send import SendMessage
from rocketchat.calls.message_get import GetMessages

from rocketchat.calls.room_get import GetPublicRooms
from rocketchat.calls.room_join import JoinRoom
from rocketchat.calls.room_leave import LeaveRoom

from rocketchat.calls.chanel_create import CreateChannel

from rocketchat.calls.user_create import CreateUser
from rocketchat.calls.user_update import UpdateUser

class RocketChatAPI(object):
    settings = None

    def __init__(self, settings=None, *args, **kwargs):
        if settings:
            self.settings = settings
        else:
            raise NotImplementedError('You must pass in settings for RocketChat')

    def send_message(self, message, room_id, **kwargs):
        """
        Send a message to a given room
        """
        return SendMessage(settings=self.settings, **kwargs).call(
            message=message,
            room_id=room_id,
            **kwargs
        )

    def get_public_rooms(self, **kwargs):
        """
        Get a listing of all public rooms with their names and IDs
        """
        return GetPublicRooms(settings=self.settings, **kwargs).call(**kwargs)

    def create_channel(self, name, **kwargs):
        """
        Create public channel with name :param name
        """

        return CreateChannel(settings=self.settings, **kwargs).call(
            name=name,
            **kwargs
        )

    def get_messages(self, room_id, **kwargs):
        """
        Get a listing of all public rooms with their names and IDs
        """
        return GetMessages(settings=self.settings, **kwargs).call(
            room_id = room_id,
            **kwargs
        )

    def join_room(self, room_id, **kwargs):
        """
        Join room with ID
        """
        return JoinRoom(settings=self.settings, **kwargs).call(
            room_id = room_id,
            **kwargs
        )

    def leave_room(self, room_id, **kwargs):
        """
        Leave room with ID
        """
        return LeaveRoom(settings=self.settings, **kwargs).call(
            room_id=room_id,
            **kwargs
        )

    def create_user(self, **kwargs):
        """
        Create User
        """
        return CreateUser(settings=self.settings, **kwargs).call(**kwargs)

    def update_user(self, **kwargs):
        """
        Update User with ID
        """
        return UpdateUser(settings=self.settings, **kwargs).call(**kwargs)



