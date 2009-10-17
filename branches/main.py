import socket;

adress, services = socket.bt_discover();
print "Discovered: %s, %s" % (adress, services);
target = (adress, services.values()[0]);

conn = socket.socket(socket.AF_BT, socket.SOCK_STREAM);
conn.connect(target);
to_gps = conn_makefile("r", 0);

while True:
    msg = to_gps.readline();
    if msg.startswith("$GPGGA"):
        gps_data = msg.split(",");
        lat = gps_data[2];
        lon = gps_data[4];
        break;
    
to_gps.close();
conn.close();
print "You now at latitude %s and longtitude %s" % (lat, lon);