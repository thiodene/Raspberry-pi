# Add the following line at the end to get the Localhost display on the Raspberry Pi at start up

if [ $(tty) == /dev/tty1 ]; then
  matchbox-window-manager -use_cursor no -user_titlebar no &
  xinit /usr/bin/chromium-browser --kiosk --start-maximized --login-screen-size="1920,1080" http://localhost
fi
