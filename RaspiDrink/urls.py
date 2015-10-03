from django.conf.urls import patterns, include, url
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'webgui.views.homepage'),
    url(r'^create_cocktail/$', 'webgui.views.create_cocktail'),
    url(r'^delete_cocktail/(\d+)/$', 'webgui.views.delete_cocktail'),
    url(r'^admin_homepage/$', 'webgui.views.admin_homepage'),
    url(r'^login/$', 'webgui.views.login_page'),
    url(r'^logout/$', 'webgui.views.logout_view'),
    url(r'^delete_bottle/(\d+)/$', 'webgui.views.delete_bottle'),
    url(r'^create_bottle/$', 'webgui.views.create_bottle'),
    url(r'^update_bottle/(\d+)/$', 'webgui.views.update_bottle'),
    url(r'^run_cocktail/(\d+)/$', 'webgui.views.run_cocktail'),
    url(r'^run_random/$', 'webgui.views.run_random'),
    url(r'^run_coffin/$', 'webgui.views.run_coffin'),
    url(r'^desactivate_bottle/(\d+)/$', 'webgui.views.desactivate_bottle'),
    url(r'^activate_bottle/(\d+)/$', 'webgui.views.activate_bottle'),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),

)
