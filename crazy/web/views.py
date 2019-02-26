from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from backend.multitask import  MultiTaskManger
from web import models
# Create your views here.
def dashboard(request):
    return render(request,'index.html')
def acc_login(request):
    error_msg=''
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('/')
        else:
            error_msg='Wrong username password'
    return render(request,'login.html',{'error_msg':error_msg})
def web_ssh(request):
    return render(request,'web_ssh.html')
@login_required
def host_mgr(request):
    return render(request,'host_mgr.html')
@login_required
def file_transfer(request):
    return render(request,'file_transfer.html')
@login_required
@csrf_exempt
def batch_task_mgr(request):
    task_arguments=json.loads(request.POST.get('task_arguments'))
    task_obj=MultiTaskManger(request)
    response={'task_id':task_obj.task_obj.id,
              'select_hosts':list(task_obj.task_obj.tasklogdetail_set.all().values('id',
                                                                         'host_to_remoteuser__host__name',
                                                                         'host_to_remoteuser__host__id_addr',
                                                                         'host_to_remoteuser__removeuser__username'
                                                                         ))
              }
    return HttpResponse(json.dumps(response))
def get_task_result(request):
    task_id=request.GET.get('task_id')
    sub_tasklog_objs=models.TaskLogDetail.objects.filter(id=task_id)
    log_data=list(sub_tasklog_objs.values("id","result","task_status"))
    return HttpResponse(json.dumps(log_data))











