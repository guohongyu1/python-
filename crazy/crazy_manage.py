import sys,os,django
if __name__=="__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crazy.settings')
    django.setup()
    from backend import main
    interactive_obj=main.ArgvHandler(sys.argv)
    interactive_obj.call()
