from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
  path(''       , views.index,  name='index'),

  path('sample-page/', views.filesUpload,  name='sample-page'),
  path('map/', views.map,  name='map'),
  path('tables/', views.tables, name='tables'),
  re_path('view/(?P<id>[\w-]+)/$', views.CameraDetailView, name='view'),
  re_path('analyse/(?P<id>[\w-]+)/$', views.VideoDetailView, name='analyse'),
  re_path('suspects/(?P<id>[\w-]+)/$', views.suspectDetails, name='suspects'),
  path('view_suspects/',views.viewsuspectDetails, name='view-suspects'),
  re_path('suspectDetails/(?P<id>[\w-]+)/$', views.oneSuspectData, name='onesuspect'),
  re_path('trackPerson/(?P<id>[\w-]+)/$',views.tracking1, name='trackPerson'),
  re_path('search/(?P<id>[\w-]+)/$',views.SearchVideoView.as_view(), name='search'),
]
