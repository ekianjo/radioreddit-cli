import subprocess, sys, re, os
mode="cli"

#may be better to use the notification icon function from yad instead... need to try it out. 

def songnamewindow(songname):
    global songwindow
    if songwindow:
        songwindow.kill()
    if songwindow.poll()==None:
        songwindow.kill()
    try:
        songwindow = subprocess.Popen(["yad",'''--title="Song Information"''','''--text={0}'''.format(songname)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

if os.path.isfile("guiactivated"):
    mode="gui"

if sys.argv.__len__() > 1:
    stream_name = sys.argv[1]
else:
    stream_name = "main"

stream_name_to_url = {
    "main": "http://173.231.136.91:8000/",
    "random": "http://173.231.136.91:8050/",
    "rock": "http://173.231.136.91:8020/",
    "metal": "http://173.231.136.91:8090/",
    "indie": "http://173.231.136.91:8070/"
}

try:
    player = subprocess.Popen(["mplayer", stream_name_to_url[stream_name]], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
except KeyError:
    print "Usage: %s [station]" % sys.argv[0]
    print "Available stations: %s" % ", ".join(sorted(stream_name_to_url))
    print "Default stream: main"
    sys.exit(1)
except OSError as err:
    if err.errno == 2:
        print "You need to install mplayer to play the streams. (apt-get install mplayer)"
        sys.exit(1)

try:
    while not player.poll():
        player_line = player.stdout.readline()
        if songwindow:
            songwindowline= songwindow.stdout.readline()
        
            if songwindowline.startswith("1"):
                player.kill()
                menu = subprocess.Popen(["radioreddit-gui.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                exit 0
        
        if player_line.startswith("ICY Info: "):
            song_name = re.match("ICY Info: StreamTitle='(.*?)';StreamUrl='';", player_line).group(1)
            print "New song! %s" % song_name
            
            if mode=="gui":
                songnamewindow(song_name)

            #kill previous yad window
            #display song title
            #record songs played in a text file for reference
            #need to catch if yad's returning an exit, so that the player may be killed
            
except KeyboardInterrupt:
    player.kill()
except Exception, e:
    print e
