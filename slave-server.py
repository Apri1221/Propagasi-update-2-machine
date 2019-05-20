# Apriyanto J.P.L Tobing 165150200111184
import socket
import threading
import time
# from fungsi import send_term, recv_term
from fungsi import upload, download

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# defenisikan host, port
host = "0.0.0.0"
port = 8889
sock.bind((host, port))
sock.listen(10)

BUFSIZE = 4096  # harus dinamis

print('listening ...')

while True:
    conn, addr = sock.accept()
    # print('client connected ... ', addr)
    
    lokasi_download = "slave-folder"

    # kedepannya, coba ambil list tiap file
    # kemudian nama file yang ada disini dikirimkan ke method download
    jumlah = conn.recv(1024)
    jumlah = int(jumlah.decode("ascii"))
    count = 0
    while count < jumlah:
        download(conn, lokasi_download)
        count += 1

    conn.close()

    print()
    print('----- bersedia menerima file kembali -----')
    print ("Start : %s" % time.ctime())
