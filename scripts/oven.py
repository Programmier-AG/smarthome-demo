import RPi.GPIO as g
def run(attr):
    g.setmode(g.BCM)
    if(attr == "on"):
        g.setup(3, 1)
    elif(attr == "off"):
        g.setup(3, 0)
