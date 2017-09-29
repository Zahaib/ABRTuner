from mod_python import apache
import logging
import datetime



logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(message)s', filename='/tmp/myscript.log', filemode='a+')
log = logging.getLogger('myscript')


def handler(req):
    #ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    ts = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    d = ts + " " + str(req.read()) + "\n"

    outfile = open("/home/zahaib/stats.txt", "a+")
    outfile.write("%s" % d)
    outfile.close()

    #log.info(req.read())

    #req.content_type = "text/plain"
    #req.write("Hello World!")

    return apache.OK

