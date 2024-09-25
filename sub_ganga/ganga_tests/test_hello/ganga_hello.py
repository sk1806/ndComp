#from Ganga import Job, Executable

# Create a new job
j = Job()

# Define the executable and its arguments
j.application = Executable()
j.application.exe = 'echo'
j.application.args = ['arg1', 'arg2']

j.outputsandbox = ['stdout', 'stderr']

# Define other job properties, such as input data, output location, etc.

# Submit the job
j.submit()

