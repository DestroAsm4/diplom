from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.bot_logic import get_user_goals, show_categories
from bot.tg.client import TgClient
from bot.tg.schemas import Message
from todolist.settings import BOT_TOKEN


class Command(BaseCommand):

    help = "run bot"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(BOT_TOKEN)
        self.user_data = {}

    def handle(self, *args, **options):
        offset = 0
        self.stdout.write(self.style.SUCCESS('Bot started...'))
        while True:
            res = self.tg_client.get_updates(offset=offset, allow_updates='message')
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)
                print(item.message)

    def handle_message(self, msg: Message):
        tg_user, _ = TgUser.objects.get_or_create(chat_id=msg.chat.id, defaults={'username': msg.chat.username})
        if not tg_user.is_verified:
            tg_user.update_verification_code()
            self.tg_client.send_message(msg.chat.id, f'Confirm your account\n Verification code: {tg_user.verification_code}')
        else:
            self.handle_auth_user(tg_user, msg)

    def handle_auth_user(self, tg_user: TgUser, msg: Message):
        if msg.text.startswith('/'):
            match msg.text:
                case '/goals':
                    get_user_goals(tg_user, msg)
                    # self.tg_client.send_message(chat_id=msg.chat.id, res)
                case '/create':
                    text = show_categories(user_id=tg_user.user.id, chat_id=msg.chat.id, users_data=self.user_data)
                case '/cancel':
                    if self.user_data[msg.chat.id]:
                        del self.user_data[msg.chat.id]
                    text = 'Creation cancelled'
        else:
            text = 'List of commands:\n/goals - Show your goals\n/create - Create a goal\n/cancel - Cancel creation'
            self.tg_client.send_message(chat_id=msg.chat.id, text=text)
