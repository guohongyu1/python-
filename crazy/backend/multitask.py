import json
from web import models
import subprocess
from django import  conf
class MultiTaskManger(object):
    def __init__(self,request):
        self.request=request
        self.run_task()
    def parse_task(self):
        self.task_date=json.loads(self.request.POST.get('task_arguments'))
        task_type=self.task_date.get('task_type')
        if hasattr(self,task_type):
            func=getattr(self,task_type)
            func()
        else:
            print('cannot find task',task_type)
    def run_task(self):
        self.parse_task()
    def cmd(self):
        task_obj=models.Task.objects.create(task_type=0,content=self.task_date.get('cmd_text'),user=self.request.user)
        print(task_obj)
        select_host_id=set(self.task_date.get('select_host_id'))
        task_log_obj=[]
        for id in select_host_id:
            task_log_obj.append(models.TaskLogDetail(task=task_obj,result='init...',host_to_remoteuser_id=id))
        models.TaskLogDetail.objects.bulk_create(task_log_obj)
        task_script="python %s/backend/task_runner.py %s"%(conf.settings.BASE_DIR,task_obj.id)
        subprocess.Popen(task_script,shell=True)
        print('running batch commanads')
        self.task_obj=task_obj
    def file_transfer(self):
        task_obj = models.Task.objects.create(task_type=1, content=json.dumps(self.task_date),
                                              user=self.request.user)
        print(task_obj)
        select_host_id = set(self.task_date.get('select_host_id'))
        task_log_obj = []
        for id in select_host_id:
            task_log_obj.append(models.TaskLogDetail(task=task_obj, result='init...', host_to_remoteuser_id=id))
        models.TaskLogDetail.objects.bulk_create(task_log_obj)
        task_script = "python %s/backend/task_runner.py %s" % (conf.settings.BASE_DIR, task_obj.id)
        subprocess.Popen(task_script, shell=True)
        print('running batch commanads')
        self.task_obj = task_obj