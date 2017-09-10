from rest_framework.permissions import BasePermission
from django.utils import timezone

class IsOwner(BasePermission):
	message = "You must be the owner of this object"

	def has_object_permission(self, request, view, obj):
		if request.user.is_superuser or request.user.is_staff or (obj.author == request.user):
			return True
		else:
			return False

class IsDraft(BasePermission):
	message = "You dont own this, and/or it isn't ready yet"

	def has_object_permission(self, request, view, obj):
		if (obj.draft) or (obj.publish > timezone.now().date() ):
			if not(request.user.is_superuser or request.user.is_staff or (obj.author == request.user)):
				return False
		return True