# filename=$1
grunt --config Gruntfile.js --force
#mv ./dash.all.js onlinecd_pens_video.dash.all.mpc.new.js
#echo Lums_123 | sudo -S cp onlinecd_pens_video.dash.all.mpc.new.js /var/www/html/yz_dashplayers/
#cp onlinecd_pens_video.dash.all.mpc.new.js pens_video.dash.all.robustmpc.js
#echo Lums_123 | sudo -S cp pens_video.dash.all.robustmpc.js /var/www/html/yz_dashplayers/
mv ./dash.all.js dash.allAlgo.js
echo Lums_123 | sudo -S cp dash.allAlgo.js /var/www/html/yz_dashplayers/
echo
#cp ./dash.all.js ../video_server/
# cp ./dash.all.js ./compiled_code/$1_dash.all.js
