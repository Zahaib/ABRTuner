# filename=$1
grunt --config Gruntfile.js --force
cp ./dash.all.js ./dash.all.mpc.new.hyb.js
echo Lums_123 | sudo -S cp dash.all.mpc.new.hyb.js /var/www/html/yz_dashplayers/
echo

# cp ./dash.all.js ./compiled_code/$1_dash.all.js
