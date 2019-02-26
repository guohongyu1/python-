import os,django,sys,paramiko
from concurrent.futures import ThreadPoolExecutor
from django import conf
import json
def ssh_cmd(sub_host_to_user_obj):
    host_to_user=sub_host_to_user_obj.host_to_remoteuser
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host_to_user.host.id_addr, host_to_user.host.port, host_to_user.removeuser.username, host_to_user.removeuser.password,timeout=5)
        stdin, stdout, stderr = ssh.exec_command(sub_host_to_user_obj.task.content)
        stdout_res=stdout.read()
        stderr_res=stderr.read()
        sub_host_to_user_obj.result=stdout_res.decode('utf-8')+stderr_res.decode('utf-8')
        if stderr_res:
            sub_host_to_user_obj.task_status=3
        else:
            sub_host_to_user_obj.task_status =2
    except  Exception as e:
        sub_host_to_user_obj.result=e
        sub_host_to_user_obj.task_status = 2
    sub_host_to_user_obj.save()
    ssh.close()
def file_transfer(sub_host_to_user_obj,task_data):
    import os, sys
    import paramiko
    host_to_user = sub_host_to_user_obj.host_to_remoteuser
    try:
        t = paramiko.Transport((host_to_user.host.id_addr, host_to_user.host.port))
        t.connect(username=host_to_user.removeuser.username, password=host_to_user.removeuser.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        if task_data['file_transfer_type']=="get":
            local_file_path=conf.settings.DOWNLOAD_DIR
            if not os.path.isdir("%s%s"%(local_file_path,sub_host_to_user_obj.task.id)):
                os.mkdir("%s%s"%(local_file_path,sub_host_to_user_obj.task.id))
            filename="%s.%s"%(sub_host_to_user_obj.host_to_remoteuser.host.id_addr,task_data['remote_file_path'].split('/')[-1])
            sftp.get(task_data['remote_file_path'], "%s/%s/%s"%(local_file_path,sub_host_to_user_obj.task.id,filename))
            result="下载成功"
        else:
            sftp.put(task_data['local_file_path'],task_data['remote_file_path'])
            result='上传成功'
        sub_host_to_user_obj.task_status=2
        t.close()
    except Exception as e:
        sub_host_to_user_obj.task_status = 3
        result=e
    sub_host_to_user_obj.result = result
    sub_host_to_user_obj.save()
if __name__=="__main__":
    bath_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(bath_dir)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crazy.settings')
    django.setup()
    if len(sys.argv)==1:
        exit('task is not provided')
    task_id=sys.argv[1]
    from web import models
    task_obj=models.Task.objects.get(id=task_id)
    pool = ThreadPoolExecutor(10)
    if task_obj.task_type == 0:
        for sub_host_to_user_obj in task_obj.tasklogdetail_set.all():
            pool.submit(ssh_cmd,sub_host_to_user_obj)
    else:
        task_data=json.loads(task_obj.content)
        for sub_host_to_user_obj in task_obj.tasklogdetail_set.all():
            pool.submit(file_transfer,sub_host_to_user_obj,task_data)
    pool.shutdown(wait=True)
