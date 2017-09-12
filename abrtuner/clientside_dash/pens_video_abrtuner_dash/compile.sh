# filename=$1
grunt --config Gruntfile.js --force
mv ./dash.all.js pens_video.dash.all.mpc.new.pensieve.js
echo Lums_123 | sudo -S cp pens_video.dash.all.mpc.new.pensieve.js /var/www/html/yz_dashplayers/
echo
#cp ./dash.all.js ../video_server/
# cp ./dash.all.js ./compiled_code/$1_dash.all.js
