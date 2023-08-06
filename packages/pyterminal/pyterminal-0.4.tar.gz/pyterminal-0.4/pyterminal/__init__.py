#Python print text with a delay like terminal :D
#Many thanks to @JackRendor (Telegram Nick)
#Check it on Github :D

import sys, time

def keyboard(argument, tempo):
    var = list(argument)
    n = 0
    for x in var:
        sys.stdout.write(var[n])
        sys.stdout.flush()
        n+=1
        time.sleep(tempo)
    else:
        print
