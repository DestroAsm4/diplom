from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.models import GoalCategory, Goal, Status, GoalComment, Board
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, GoalSerializer, GoalCommentCreateSerializer, GoalCommentSerializer, BoardSerializer, BoardListSerializer, BoardCreateSerializer
from goals.filters import GoalDateFilter, GoalCategoryFilter
from goals.permissions import BoardPermission



#-------------------categories------------
class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalCategoryFilter
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]
    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user
        ).exclude(is_deleted=True)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    '''
            view for updating and deleting
    '''
    serializer_class = GoalCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.status = Status.archived
        instance.save()
        return instance

#---------------------Goal-----------------

class GoalCreateView(CreateAPIView):
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = [IsAuthenticated]


class GoalListView(ListAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    filterset_class = GoalDateFilter
    ordering = ['title']
    ordering_fields = ['title', 'created', 'category', 'priority', 'due_date']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user,
            category__is_deleted=False).exclude(status=Status.archived)


class GoalView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(category__is_deleted=False).exclude(status=Status.archived)

    def perform_destroy(self, instance):
        instance.status = Status.archived
        instance.save()

#---------------------Comments-----------------
class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    serializer_class = GoalCommentCreateSerializer
    permission_classes = [IsAuthenticated]


class GoalCommentListView(ListAPIView):
    serializer_class = GoalCommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = ['goal']
    ordering = ['-created']

    def get_queryset(self):
        return GoalComment.objects.filter(
            goal__category__board__participants__user=self.request.user
        )


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    '''
        view for updating and deleting
    '''
    serializer_class = GoalCommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = GoalComment.objects.select_related('user')

    def get_queryset(self):
        return GoalComment.objects.select_related("user").filter(
            goal__category__board__participants__user=self.request.user
        )

#---------------------Boards-----------------
class BoardCreateView(CreateAPIView):
    model = Board
    serializer_class = BoardCreateSerializer
    permission_classes = [IsAuthenticated]


class BoardView(RetrieveUpdateDestroyAPIView):
    '''
            view for updating and deleting
    '''
    model = Board
    permission_classes = [IsAuthenticated, BoardPermission]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):

        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Status.archived
            )

        return instance


class BoardListView(ListAPIView):
    serializer_class = BoardListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering = ['title']

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user).exclude(is_deleted=True)
