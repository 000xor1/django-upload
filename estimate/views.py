from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


import os
import time
import hashlib
import uuid


# Create your views here.

def _createDir(dir_name):
    try:
        if not os.path.exists(dir_name):
            os.makedirs(os.path.join(dir_name))
            os.makedirs(os.path.join(dir_name)+"/"+"video")
            os.makedirs(os.path.join(dir_name)+"/"+"frames")
            os.makedirs(os.path.join(dir_name)+"/"+"blur_frames")
            os.makedirs(os.path.join(dir_name)+"/"+"lp_frames")
            os.makedirs(os.path.join(dir_name)+"/"+"vehicle_frames")
            os.makedirs(os.path.join(dir_name)+"/"+"results")

    except OSError:
        print("Error: creating directory. ", dir_name)


def _handle_uploaded_file(dir_name, file_name, video_file):
    with open(dir_name+'/video/'+file_name, 'wb+') as destination:
        for chunk in video_file.chunks():
            destination.write(chunk)


def _hash():

    now_time = time.time()
    uniqe_id = (str(now_time) + str(uuid.uuid4())).encode('utf-8')

    sha = hashlib.new('sha256')
    sha.update(uniqe_id)

    hash_name = sha.hexdigest()

    return hash_name


@csrf_exempt
def upload(request):
    if request.method == 'POST' and request.FILES['video']:
        video_file = request.FILES['video']

        dir_name = _hash()
        file_name = _hash()

        while True:
            try:
                _createDir(dir_name)
                break
            except:
                print("디렉토리 생성 실패")

        _handle_uploaded_file(dir_name, file_name, video_file)

        return JsonResponse({'status': 'success', 'result': {'report': dir_name}})

    else:
        return JsonResponse({'status': 'fail', 'msg': "업로드 된 파일이 없습니다."})


def report(request, id):

    dir_name = id

    try:
        file_name = os.listdir(dir_name+"/video")[0]
    except:
        file_name = "Not found file"

    return render(request, 'estimate/report.html', {'dir_name': dir_name, 'file_name': file_name})


def index(request):
    msg = 'My Message'
    return render(request, 'estimate/index.html', {'message': msg})
