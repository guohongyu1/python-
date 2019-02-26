class ArgvHandler(object):
    def __init__(self,sys_args):
        self.sys_args=sys_args
    def help_mag(self,error_msg=''):
        msgs = """
            %s
              run 启动交互程序

              """%error_msg
        exit(msgs)
    def call(self):
        if len(self.sys_args)==1:
            self.help_mag()
        if hasattr(self,self.sys_args[1]):
            func=getattr(self,self.sys_args[1])
            func()
        else:
            self.help_mag("没有:%s"%self.sys_args[1])

    def run(self):
        from backend.ssh_interactive import SshHandler
        obj=SshHandler(self)
        obj.interactive()