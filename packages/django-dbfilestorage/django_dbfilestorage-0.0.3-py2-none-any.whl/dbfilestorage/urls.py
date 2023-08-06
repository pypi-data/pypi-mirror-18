from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^(?P<name>.*)$', views.show_file, name="dbstorage_file"),
)
