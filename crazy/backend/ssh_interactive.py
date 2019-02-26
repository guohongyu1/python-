from django.contrib.auth import authenticate
from backend import demo
from web import models
class SshHandler(object):
    def __init__(self,argv_handler_instance):
        self.argv_handler_instance=argv_handler_instance
    def auth(self):
        count=0
        while count<3:
            username=input('username:').strip()
            password=input('password:').strip()
            user=authenticate(username=username,password=password)
            if user:
                self.user=user
                return True
            else:
                count+=1

    def interactive(self):
        self.models=models
        if self.auth():
            while True:
                host_group_list=self.user.host_group.all()
                for index,host_group_obj in enumerate(host_group_list):
                    print("%s.\t%s[%s]"%(index,host_group_obj,host_group_obj.host_to_remoteuser.count()))
                print("z.未分组主机[%s]"%self.user.host_to_remoteuser.count())
                choice=input('选择主机组>>')
                if choice.isdigit():
                    choice=int(choice)
                    host_group_obj=host_group_list[choice]
                elif  choice=='z':
                    host_group_obj = self.user
                while True:
                    for index,host_group_user in enumerate(host_group_obj.host_to_remoteuser.all()):
                        print("%s.%s"%(index,host_group_user))
                    choice = input('选择主机>>')
                    if choice.isdigit():
                        choice = int(choice)
                        host_group_user_obj = host_group_obj.host_to_remoteuser.all()[choice]
                        demo.ssh_connect(self,host_group_user_obj)
                        print(host_group_user_obj)
                    elif choice=='b':
                        break




















