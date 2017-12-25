# filename=$1
grunt --config Gruntfile.js --force
cp build/temp/dash.all.min.js ./bola_dash.js
#mv ./bola_dash.js dash.allAlgo.js
echo Lums_123 | sudo -S cp bola_dash.js /var/www/html/yz_dashplayers/
echo



#cp ./dash.all.js ../video_server/
# cp ./dash.all.js ./compiled_code/$1_dash.all.js
