import os,sys
import paramiko

t = paramiko.Transport(('192.168.1.104',22))
t.connect(username='',password='')
sftp = paramiko.SFTPClient.from_transport(t)
sftp.put('d:/c.txt','/root/downloads/c.txt')
# sftp.get('/root/a.txt/123','d:/a.txt')
t.close()