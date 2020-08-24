DATE=`date '+%Y-%m-%d %H:%M:%S'`
echo "Canary Monitoring service started at ${DATE}" | systemd-cat -p info

while :
do
 	sudo /usr/bin/python3 /opt/customlogger/detectiveROB.py
	sleep 300;
done
