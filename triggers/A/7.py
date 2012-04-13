from subprocess import Popen, PIPE, STDOUT
p = Popen(['xte', "keydown Control_L", "keydown Alt_L", "key l", "keyup Alt_L", "keyup Control_L"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
#p = Popen(['env'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
#out = p.communicate()[0]
#print(out)
