from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'blog.views.home'),
    url(r'^add-item', 'blog.views.add_item'),
    url(r'^delete-item/(?P<id>\d+)$', 'blog.views.delete_item'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'blog/login.html'}),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^register$', 'blog.views.register'),
    url(r'^confirmation$', 'blog.views.validation'),
    url(r'^manage$', 'blog.views.manage'),
    url(r'^watch$', 'blog.views.watch'),
    url(r'^follow$', 'blog.views.follow'),
    url(r'^get-list$', 'blog.views.get_bloggers'),
    url(r'^photo/(?P<id>\d+)$', 'blog.views.get_photo', name='photo'),

)
