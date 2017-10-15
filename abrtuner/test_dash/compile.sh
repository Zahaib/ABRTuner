# filename=$1
grunt --config Gruntfile.js --force
mv ./dash.all.js dash.test.js
echo Lums_123 | sudo -S cp dash.test.js /var/www/html/yz_dashplayers/
echo
#cp ./dash.all.js ../video_server/
# cp ./dash.all.js ./compiled_code/$1_dash.all.js
