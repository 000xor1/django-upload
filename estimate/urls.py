from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload, name='upload'),
    path('report/<id>', views.report, name='report'),
    path('api/report/<id>', views.get_report, name='report'),
    path('api/image/<dir_id>/<sub_dir_id>/<file_id>',
         views.load_image, name='load_image'),
]
