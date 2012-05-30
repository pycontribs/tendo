import os
if 'PYTHONPATH' in os.environ:
    os.environ['PYTHONPATH']="..:" + os.environ['PYTHONPATH']
else:
    os.environ['PYTHONPATH']=".."
#os.system('set')
#os.chdir("..")
os.system("make html")
