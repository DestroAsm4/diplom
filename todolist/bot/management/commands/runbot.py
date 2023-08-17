from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.bot_logic import get_user_goals, show_categories
from bot.tg.client import TgClient
from bot.tg.schemas import Message


from bot.tg.bot_logic import choose_category

from django.conf import settings

from bot.tg.bot_logic import create_goal


class Command(BaseCommand):

    help = "run bot"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)
        self.user_data = {}
        self.item = None
        self.offset = 0

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Bot started...'))
        while True:
            res = self.tg_client.get_updates(offset=self.offset, allow_updates='message')
            for item in res.result:
                self.offset = item.update_id + 1
                self.item = item
                self.handle_message(item.message)
                print(item.message)

    def handle_message(self, msg: Message):
        'Verification of the user, or continuation of the dialogue'
        tg_user, _ = TgUser.objects.get_or_create(chat_id=msg.chat.id, defaults={'username': msg.chat.username})
        if not tg_user.is_verified:
            tg_user.update_verification_code()
            self.tg_client.send_message(msg.chat.id, f'Confirm your account\n Verification code: {tg_user.verification_code}')
        else:
            self.handle_auth_user(tg_user, msg)

    def handle_auth_user(self, tg_user: TgUser, msg: Message):
        'bot interaction menu'

        if msg.text.startswith('/'):
            match msg.text:
                case '/goals':
                    get_user_goals(tg_user, msg)
                case '/create':
                    user_data = show_categories(user_id=tg_user.user.id, chat_id=msg.chat.id, users_data=self.user_data,
                                                msg=msg)
                    while True:
                        res = self.tg_client.get_updates(offset=self.offset)
                        for item in res.result:
                            self.offset = item.update_id + 1
                            user_data = choose_category(chat_id=msg.chat.id, message=item.message.text, user_data=user_data)

                        while True:
                            res = self.tg_client.get_updates(offset=self.offset)
                            for item in res.result:
                                self.offset = item.update_id + 1
                                create_goal(user_id=user_data['user_id'], chat_id=msg.chat.id, message=item.message.text, category_id=user_data['category_id'])
                            break
                        break












        else:
            text = 'List of commands:\n/goals - Show your goals\n/create - Create a goal'
            self.tg_client.send_message(chat_id=msg.chat.id, text=text)
