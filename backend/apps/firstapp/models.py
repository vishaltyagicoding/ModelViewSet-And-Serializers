from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


"""
🔥 WHEN TO USE EACH METHOD (SUPER IMPORTANT)
Method	Real Use Case
get_queryset()	Restrict data (user-specific, published only)
filter_queryset()	Custom query params
get_serializer_class()	Different serializer for create/update
get_serializer()	Pass extra context
list()	Custom response format
retrieve()	Customize single object response
create()	Full control of POST response
perform_create()	Add user / extra save logic
update()	Customize PUT response
perform_update()	Modify save behavior
destroy()	Customize delete response
perform_destroy()	Soft delete / logging
paginate_queryset()	Custom pagination
"""