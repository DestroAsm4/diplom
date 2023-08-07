from collections import namedtuple
from typing import Any

from django.db import IntegrityError

from goals.models import BoardParticipant, Goal, GoalCategory, Status, Priority
from goals.serializers import GoalCategorySerializer, GoalSerializer

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.schemas import Message

from django.conf import settings

tg_client = TgClient(settings.BOT_TOKEN)

GoalData = namedtuple('GoalData', ['title', 'due_date', 'priority', 'status'])
CategoryData = namedtuple('CategoryData', ['cat_id', 'title'])


def get_user_goals(tg_user: TgUser, msg: Message) -> str:

    user_id = tg_user.user.id

    priority = dict(Priority.choices)
    status = dict(Status.choices)

    goals = (
        Goal.objects.select_related('user')
        .filter(category__board__participants__user_id=user_id, category__is_deleted=False)
        .exclude(status=Status.archived)
        .all()
    )



    if not goals.exists():
        return "You don't have any goals."

    serializer = GoalSerializer(goals, many=True)

    data = []
    for item in serializer.data:
        filtered_dict = GoalData(
            title=item['title'],
            due_date=item['due_date'][:10] if item['due_date'] else '',
            priority=priority[item['priority']],
            status=status[item['status']],
        )
        data.append(filtered_dict)

    # data = []
    # for item in serializer.data:
    #     goal = item['title']
    #     print(goal)
    #     # due_date=item['due_date'][:10] if item['due_date'] else '',
    #     # priority=priority[item['priority']],
    #     # status=status[item['status']],
    #     # )
    #     data.append(goal)
    #     tg_client.send_message(chat_id=msg.chat.id, text=goal)




    message = []
    for index, item in enumerate(data, start=1):
        goal = (
            f'{index}) {item.title}, status: {item.status}, priority: {item.priority}, '
            f"{'due_date: ' + item.due_date if item.due_date else ''}"
        )

        message.append(goal)

    response = '\n'.join(message)

    tg_client.send_message(chat_id=msg.chat.id, text=response)
    return response

def show_categories(user_id: int, chat_id: int, users_data: dict[int, dict[str | int, ...]], msg: Message) -> dict:

    user_data = {
            'categories': {},
            'user_id': user_id,
            'category_id': None,
            'title': None
        }

    categories = (
        GoalCategory.objects.select_related('user')
        .filter(
            board__participants__user_id=user_id,
            board__participants__role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        )
        .exclude(is_deleted=True)
    )

    if not categories.exists():
        tg_client.send_message(chat_id=msg.chat.id, text="You don't have any categories to create a goal. Please create a category first.")

    serializer = GoalCategorySerializer(categories, many=True)

    data = []
    for item in serializer.data:
        category = CategoryData(cat_id=item['id'], title=item['title'])
        data.append(category)

    # Save 'index' to choose a user and link the category id to its index
    user_data['categories'] = {index: item.cat_id for index, item in enumerate(data, start=1)}

    message = [f'{index}) {item.title}' for index, item in enumerate(data, start=1)]

    response = '\n'.join(message)
    tg_client.send_message(chat_id=msg.chat.id,
                           text='Choose category for goal:\n' + response)


    return user_data

def choose_category(user_data, **kwargs) -> dict:

    chat_id: int = kwargs.get('chat_id')
    message: str = kwargs.get('message')
    user_data: dict = user_data


    text: str = ''

    # print(chat_id, type(message), users_data)

    if message.isdigit():
        value = int(message)
        category_id = user_data['categories'][value]



        category_id = value
        if category_id is not None:

            user_data['category_id'] = category_id
            text = f'You chose category {value}. Please, send the title for the goal.'
        else:
            text = f'Invalid category index. Please choose a valid category.'
    else:
        text = f'You sent not valid category index.'
    tg_client.send_message(chat_id=chat_id, text=text)
    return user_data

def create_goal(**kwargs) -> str:

    user_id: int = kwargs.get('user_id')
    chat_id: int = kwargs.get('chat_id')
    message: str = kwargs.get('message')
    category_id = kwargs.get('category_id')
    text_response = ''
    try:
        Goal.objects.create(title=message, user_id=user_id, category_id=category_id)
          # Clean user cache
        text_response = f'Goal "{message}" added!'
        tg_client.send_message(chat_id=chat_id, text=text_response)
    except IntegrityError:
        text_response = 'Something went wrong. Goal not created.'
        tg_client.send_message(chat_id=chat_id, text=text_response)
    except Exception as e:
        text_response = f'Error: {str(e)}'
        tg_client.send_message(chat_id=chat_id, text=text_response)
