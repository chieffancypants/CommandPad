from subprocess import Popen, PIPE, STDOUT
p = Popen(['gcalctool'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
