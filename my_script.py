# import sys
# import time
# k = 0
# try:
#    for line in iter(sys.stdin.readline, b''):
#       k = k + 1
#       print line
# except KeyboardInterrupt:
#    sys.stdout.flush()
#    pass

#!/usr/bin/python

import sys

while 1:
        line = sys.stdin.readline()
        if line == '':
                break
        try:
            print pretty_string(line)
        except:
                pass
# print k

# import sys
# import time
# k = 0
# try:
#     buff = ''
#     while True:
#         buff += sys.stdin.read(1)
#         if buff.endswith('\n'):
#             print buff[:-1]
#             buff = ''
#             k = k + 1
# except KeyboardInterrupt:
#    sys.stdout.flush()
#    pass
# print k