from django.urls import path

from goals.views import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryView, GoalCreateView, GoalListView, GoalView, GoalCommentCreateView, GoalCommentListView, GoalCommentView, BoardListView, BoardView, BoardCreateView

urlpatterns = [
    # Categories
    path('goal_category/create', GoalCategoryCreateView.as_view()),
    path('goal_category/list', GoalCategoryListView.as_view()),
    path('goal_category/<pk>', GoalCategoryView.as_view()),
    # Goals
    path('goal/create', GoalCreateView.as_view()),
    path('goal/list', GoalListView.as_view()),
    path('goal/<pk>', GoalView.as_view()),
    # Comments
    path('goal_comment/create', GoalCommentCreateView.as_view()),
    path('goal_comment/list', GoalCommentListView.as_view()),
    path('goal_comment/<pk>', GoalCommentView.as_view()),
    # Boards
    path('board/create', BoardCreateView.as_view()),
    path('board/list', BoardListView.as_view()),
    path('board/<pk>', BoardView.as_view()),
]
