from django.conf.urls import patterns, url
from extras import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^jobs/$', views.jobs, name='jobs'),
	url(r'^production/(?P<production_name_url>\w+)/role/(?P<role_name_url>\w+)$', views.role, name='role'),
    url(r'^actors/$', views.actors, name='actors'),
	url(r'^about/$', views.about, name='about'),
    url(r'profile/$', views.profile, name='profile'),
	url(r'^add_production/$', views.add_production, name='add production'),
	url(r'^production/(?P<production_name_url>\w+)/add_role/$', views.add_role, name='add_role'),
	url(r'^production/(?P<production_name_url>\w+)/$', views.production, name='production'),
  	url(r'^actor/(?P<actor_name_url>\w+)/$', views.actor, name='actor'),
	url(r'^actor_register/$', views.actorRegister, name='actorRegister'),
	url(r'^director_register/$', views.directorRegister, name='directorRegister'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^search/$', views.search, name='search'),
    url(r'^send/$', views.message, name='send'),)
