from subprocess import Popen, PIPE, STDOUT
p = Popen(['xte', "keydown Control_L", "key F4", "keyup Control_L"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)