from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from goals.models import GoalCategory, Goal, GoalComment, Status, Board, BoardParticipant
from core.models import User
from core.serializers import UserSerializer



#------------categories---------------


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_field = ('id', 'created', 'updated', 'user')
        fields = '__all__'


class GoalCategorySerializer(GoalCategoryCreateSerializer):
    user = UserSerializer(read_only=True)

    def validate_board(self, board: Board) -> Board:
        if board.is_deleted:
            raise ValidationError('Board do not exists')
        if not BoardParticipant.objects.filter(
            board_id=board.id,
            user_id=self.context['request'].user,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists():

            raise PermissionDenied

        return board

#---------------Goal----------------------------

class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError('not allowed in deleted category')

        if value.user != self.context['request'].user:
            raise serializers.ValidationError('not owner of the category')

        return value



class GoalSerializer(GoalCreateSerializer):
    user = UserSerializer(read_only=True)

    def validate_category(self, category: GoalCategory) -> GoalCategory:
        if category.is_deleted:
            raise ValidationError('Category do not exists')
        if not BoardParticipant.objects.filter(
            board_id=category.board_id,
            user_id=self.context['request'].user,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists():
            raise PermissionDenied

        return category

#---------------------comments---------------------
class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')

    def validate_goal(self, goal: Goal) -> Goal:
        if goal.status == Status.archived:
            raise ValidationError('Goal do not exists')
        if not BoardParticipant.objects.filter(
                board_id=goal.category.board_id,
                user_id=self.context['request'].user,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists():
            raise PermissionDenied

        return goal

class GoalCommentSerializer(GoalCommentCreateSerializer):
    user = UserSerializer(read_only=True)
    goal = GoalSerializer(read_only=True)


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ('id', 'created', 'updated')
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        board =  Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board

#---------------------------Board----------------------

class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.Role
    )
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'board')


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated')

    def update(self, instance, validated_data):
        owner = validated_data.pop('user')
        new_participants = validated_data.pop('participants')
        new_by_id = {part['user'].id: part for part in new_participants}

        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user.id not in new_by_id:
                    old_participant.delete()
                else:
                    if old_participant.role != new_by_id[old_participant.user_id]['role']:
                        old_participant.role = new_by_id[old_participant.user_id]['role']
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(board=instance, user=new_part['user'], role=new_part['role'])

            instance.title = validated_data['title']
            instance.save()

        return instance


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields ='__all__'
