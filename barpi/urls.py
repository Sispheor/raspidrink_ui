from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'barpi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'webgui.views.homepage'),
    url(r'^create_cocktail/$', 'webgui.views.create_cocktail'),
    url(r'^delete_cocktail/(\d+)/$', 'webgui.views.delete_cocktail'),


)
