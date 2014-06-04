#very simple gui with yad

touch "guiactivated"
choice=$(yad --width=400 --height=250 --button=gtk-close:1 --title="Radio Reddit" --list --column="Radio List" "Main" "Indie" "Random" "Rock" "Metal" "Quit")
ret=$?
echo "$ret"

if [ $ret -eq 1 ]; then
exit 0
fi

choice=$(echo $choice | awk 'BEGIN {FS="|" } { print $1 }')
if [ "$choice" == "Main" ]; then
  python radioreddit-cli.py main
fi
if [ "$choice" == "Indie" ]; then
  python radioreddit-cli.py indie
fi
if [ "$choice" == "Random" ]; then
  python radioreddit-cli.py random
fi
if [ "$choice" == "Rock" ]; then
  python radioreddit-cli.py rock
fi
if [ "$choice" == "Metal" ]; then
  python radioreddit-cli.py metal
fi

if [ "$choice" == "Quit" ]; then
  exit 0
fi

#extremely basic at this stage. Will improve on this shortly. 
#need Pandora detection
#need reddit radio picture
#need yad window when playing the song
#need to destroy the guiactivated file when exiting in the python script
#need to add yadcommand for detection
#blahblah in other words wil release during the weekend probably. 
