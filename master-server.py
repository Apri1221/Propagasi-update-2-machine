# Apriyanto J.P.L Tobing 165150200111184
import socket
import os
import time
# from fungsi import send_term, recv_term
from fungsi import upload, download


while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # defenisikan host, port
    host = "127.0.0.1"
    port = 8889

    sock.connect((host, port))

    # kedepannya, coba ambil list tiap file
    # kemudian nama file yang ada disini dikirimkan ke method upload
    # file_upload = 'blah/testfile.pdf'
    
    path = "master-folder"
    directory = os.listdir(path)
    jumlah = str(len(directory))
    print(jumlah, " file")

    sock.send(jumlah.encode("ascii"))
    for files in directory:
        print(files)
        filename = os.path.join(path,files)
        upload(sock, filename, files)

        # kasih jeda waktu sebelum menulis file berikutnya
        time.sleep(10)
        print()

    # kasih jeda waktu sebelum masuk ke sinkronkan lagi
    time.sleep(10)
    print()
    print("----- mulai sinkronkan file kembali -----")
    print ("Start : %s" % time.ctime())
    print()

    sock.close()