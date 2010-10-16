===========================
"Ultimate" Arduino Doorbell
===========================

Doorbell that uses a cheap wireless doorbell, attached to an Arduino to drive a servo to ring a "real" brass bell.

Pictures of the construction:

    http://www.flickr.com/photos/lilspikey/sets/72157624576532196/

Eventual plan will involve listening to Arduino's serial port to fire off additional actions on the local network and/or internet.

Using netgrowl and PicoRendezvous from:

 * http://the.taoofmac.com/space/projects/netgrowl
 * http://the.taoofmac.com/space/projects/PicoRendezvous

Also using http://github.com/kfdm/gntp for Growl for Windows notification

Installation
============

If you want to run the Python part of this on a chumby, you should attach something that sends the string 'DING DONG' down the serial port (USB) of the chumby.

On your computer (within doorbell directory):

 * virtualenv --no-site-packages .
 * source bin/activate
 * pip install -r dependencies.txt
 * ./build.sh
 
Then copy the contents of dist/ onto a USB stick (along with python in python2.6-chumby/) and plug it into your chumby.  Python for the chumby is available here:

http://wiki.chumby.com/mediawiki/index.php/Python

Of course this should all work on a "real" computer too.

