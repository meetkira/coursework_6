from django.http import Http404
from rest_framework.permissions import BasePermission

from ads.models import Ad, Comment
from users.models import User


class UpdateAdPermission(BasePermission):
    message = "You can't update or delete not yours ads"

    def has_permission(self, request, view):
        try:
            ad = Ad.objects.get(id=view.kwargs["pk"])
        except Ad.DoesNotExist:
            raise Http404

        if ad.author_id == request.user.id:
            return True

        if request.user.role == User.ADMIN:
            return True

        return False


class UpdateCommentPermission(BasePermission):
    message = "You can't update or delete not yours comments"

    def has_permission(self, request, view):
        try:
            comment = Comment.objects.get(id=view.kwargs["pk"])
        except Comment.DoesNotExist:
            raise Http404

        if comment.author_id == request.user.id:
            return True

        if request.user.is_admin:
            return True

        return False
