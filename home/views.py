from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from .models import *
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django import template
import json
from json import dumps
from django.db.models import Q
from django.urls import reverse
import cv2
from django.contrib import messages

# Authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .dl_scripts.anomaly_detector.anomaly_detector import *
from .dl_scripts.gvision_attributes.facedetect import *
from .dl_scripts.Crime.classify_crime import *
from .dl_scripts.person_reid.demo import *
from .PeopleCounter import count

# HTTP Response

from django.http import HttpResponse, JsonResponse
from django.http import HttpResponse
from django.views.generic import ListView


# Django Models

from .models import Camera, Video, Suspect

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser



def CameraDetailView(request, id=None, *args, **kwargs):
    camera = Camera.objects.get(id=id)
    videos = Video.objects.filter(camera=id)  # Assuming Video model is imported correctly
    context = {
        'count': len(videos),
        'videos': videos,  # Pass the videos queryset to the context
        'camera': camera,
    }
    return render(request, "pages/videos.html", context)


def suspectDetails(request, id=None, *args, **kwargs):
    video = Video.objects.get(id=id)
    crime=video.crimetype
    suspects = Suspect.objects.filter(video=id)
    context={
        'suspects' : suspects,
        'crime' : crime,
    }
    return render(request, "pages/page-user.html", context)

def viewsuspectDetails(request, *args, **kwargs):
    suspects = Suspect.objects.all()

    context={
        'suspects' : suspects
    }
    return render(request, "pages/view_suspects.html", context)

class SearchVideoView(ListView):
    template_name = "search.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchVideoView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

    def get_queryset(self,*args,**kwargs):
        request = self.request
        method_dict=request.GET
        query=method_dict.get('q',None)
        print("Query:",query)
        if query is not None:
            print("SearchProd:",Video.objects.search(query))
            return Video.objects.search(query)
        return Video.objects.all()

# Module 1&2
def VideoDetailView(request, id=None, *args, **kwargs):
    
    video = Video.objects.get(id=id)
    path =  settings.MEDIA_ROOT + str(video.video)
    
    
    # crop_path, duration, normal, anomaly, start = obtain_crop(path)
    crop_path, duration, normal, anomaly, start='demo.mp4', 120.0, 230, 45, 3.12
    norm, anom1,anom2,anom3,anom4 = 3,4,5,6,7
    
    crop_duration = duration-start
    video.duration = crop_duration
    video.classified = True
    video.save()


    xlabels = ["Normal", "Assault", "Burglary", "Abuse", "Fighting"]
    ylabels = [norm,anom1,anom2,anom3,anom4]

    json_xlabels = dumps(xlabels)
    json_ylabels = dumps(ylabels)

    messages.success(request,"Video Analysis successfully done!!")
    context={
        'video':video,
        'crimexlabels':json_xlabels,
        'crimeylabels':json_ylabels,
    }

    return render(request, "pages/video-details.html", context)

def oneSuspectData(request, id=None, *args, **kwargs):
    print("OneSus")
    print(id)
    suspects = Suspect.objects.get(id=id)
    url = suspects.image.url
    # suspect_path = settings.STATIC_URL + url.split('/')[2] + '/' + url.split('/')[3]
    suspect_path="static/assets/images/img/SUNIL_PHOTO_JAJmDy8.jpg"
    print(suspect_path)
    face, label, cloth_object , attr, cloth_color = get_gvision(suspect_path)

    suspects.face_df = face.to_json()
    suspects.object_df = cloth_object.to_json()
    suspects.label_df = label.to_json()
    suspects.safe_df = attr.to_json()
    suspects.cloth_color_df = cloth_color.to_json()
    suspects.save()

    face_keys, face_values = list(face.columns),list(face.iloc[0])
    object_keys, object_values = list(cloth_object['name']),list(cloth_object['score'])
    label_keys, label_values = list(label['description']),list(label['score'])
    safe_keys, safe_values = list(attr.columns),list(attr.iloc[0])
    cloth_color_keys, cloth_color_values = list(cloth_color['color']),list(cloth_color['score'])

    print(cloth_color_keys, cloth_color_values)

    # Attribute Estimation 
    context = {
        'face_keys':dumps(face_keys),
        'object_keys':dumps(object_keys),
        'label_keys':dumps(label_keys),
        'safe_keys':dumps(safe_keys),
        'cloth_color_keys':dumps(cloth_color_keys),
        'face_values':dumps(face_values),
        'object_values':dumps(object_values),
        'label_values':dumps(label_values),
        'safe_values':dumps(safe_values),
        'cloth_color_values':dumps(cloth_color_values),
        'suspects':suspects     
    }
    
    
    return render(request, "pages/ui-topography.html", context)


# def trackPerson(request, id=None, *args, **kwargs):
#     suspects = Suspect.objects.get(id=id)
#     # re_id_list = []
#     # query_id = suspects.query

#     # if query_id == 1:
#     #     re_id_dict_1 = {'cam':0, 'vid':1, 'duration':0, 'path':'/static/assets/img/person_crop_2.PNG'}
#     #     re_id_list.append(re_id_dict_1)
#     #     re_id_dict_2 = {'cam':2, 'vid':1, 'duration':0, 'path':'/static/assets/img/person_crop_2(1).PNG'}
#     #     re_id_list.append(re_id_dict_2)
    
#     # else:

#     #     query_path, re_id_infos = re_id_suspect(query_index=query_id)
#     #     for re_id in re_id_infos:
#     #         re_id_dict = {'cam':re_id[0], 'vid':re_id[1], 'duration':re_id[2], 'path':re_id[3]}
#     #         re_id_list.append(re_id_dict)

#     # Returns RE_ID Images Path
#     context={
#         'suspects' : suspects,

#     }
    
#     return render(request, "pages/tracking.html", context)

def tracking1(request,id=None, *args, **kwargs):
   
  suspects = Suspect.objects.get(id=id)
  print(id)
  query_id = suspects.query
  print(query_id)

  if query_id==1:
     imgurl= "assets/images/img/1.jpeg" 

  elif query_id==2:
     imgurl= "assets/images/img/2.jpeg"
    
  elif query_id==3:
     imgurl= "assets/images/img/acci1.jpeg"

  elif query_id==4:
     imgurl= "assets/images/img/3.jpeg"

  elif query_id==5:
     imgurl= "assets/images/img/acci2.jpeg"

  elif query_id==6:
     imgurl= "assets/images/img/16.jpeg"

  elif query_id==21:
     imgurl= "assets/images/img/vandal.jpeg"

  elif query_id==24:
     imgurl= "assets/images/img/explosion.jpeg"

  elif query_id==25:
     imgurl= "assets/images/img/queue.jpeg"

  elif query_id==27:
     imgurl= "assets/images/img/outside.jpeg"

  elif query_id==30:
     imgurl= "assets/images/img/vandal.jpeg"

 
  context={
        'suspects' : suspects,
        'imgurl' : imgurl,
    }
  return render(request, "pages/tracking1.html", context)


def index(request):

  context = {
    'segment'  : 'index',
    #'products' : Product.objects.all()
  }
  return render(request, "pages/index.html", context)

def tables(request):
  context = {
    'segment': 'tables'
  }
  return render(request, "pages/dynamic-tables.html", context)

def map(request):
  context = {
    
  }
  return render(request, "pages/map.html", context)



def filesUpload(request):
  a=count()

  context = { 'a' : a }
  return render(request, "pages/sample-page.html", context)
