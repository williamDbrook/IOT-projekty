from picozero import LED
from time import sleep

yellow = LED(13)
yellow.on()
sleep(2)
yellow.off()

"jupí svítí"