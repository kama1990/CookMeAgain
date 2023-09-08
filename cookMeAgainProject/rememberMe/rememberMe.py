from django.conf import settings
from cookMe.models import Recipe

class RememberMe:
    def __init__(self, request):
        # initiate the space where will be remembered recipes
        self.session = request.session # storing the current session
        rememberMe = self.session.get(settings.CART_SESSION_ID) # we need to get remebered from current session
        if not rememberMe:
            # we need to save empty remebered in session
            rememberMe = self.session[settings.CART_SESSION_ID] = {}
        self.rememberMe = rememberMe

    def add(self, post, quantity=1):
        # we want to add recipe to remebered
        post_id = str(post.id)
        if post_id not in self.rememberMe:
            self.rememberMe[post_id] = {'quantity':0}
            # if override_quantity:
            #     self.rememberMe[post_id]['quantity'] = quantity
            # else:
            #     self.rememberMe[post_id]['quantity'] += quantity
            self.save()

    def save(self):
        # mark the session as modified
        self.session.modified = True

    def remove(self, post):
        post_id = str(post.id)
        if post_id in self.rememberMe:
            del self.rememberMe[post_id]
            self.save()

    def __iter__(self):
        # iteration through the remebered elements and downloading recipes from the database
        post_ids = self.rememberMe.keys()
        # fetch recipe objects and add to remebered
        posts = Recipe.objects.filter(id__in=post_ids)
        rememberMe = self.rememberMe.copy()
        for post in posts:
            rememberMe[str(post.id)]['post'] = post
        for item in rememberMe.values():
            yield item

    def clear(self):
        # remove all recipes in remebered
        del self.session[settings.CART_SESSION_ID]
        self.save()