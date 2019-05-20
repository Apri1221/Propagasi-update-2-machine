import struct
import os
import hashlib


BLOCKSIZE = 65536

def generate_file_md5(filename, blocksize=2**20):
    m = hashlib.md5()
    with open(filename, "rb" ) as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update( buf )
    return str(m.hexdigest())

def upload(conn, filename, files):
    
    # cek ada ga file nya
    if os.path.isfile(filename):

        filesize = os.path.getsize(filename)
        
        
        # cek kode hash dan properties nya
        hash_in = generate_file_md5(filename)
        
        print("kode hash file : " ,hash_in)
        # pengiriman file
        payload = open(filename,'rb').read() 

        size = len(payload)

        message = files + "," + hash_in

        print("sumber : ", filename)
        if filename != '':
            conn.send(message.encode("ascii"))
        
        status = conn.recv(1024).decode("ascii")
        print("balasan => ", status)

        # jika file disana telah berubah, siap lakukan replika
        if("siap replika" in status):
            print("bersiap mengirimkan file sebesar " + str(filesize/1000) + " KB")
        
            header = struct.pack(">I", size) # 2 byte unsigned dan 4 byte unsigned
            
            # tidak di encode
            alldata = header + payload
            
            # kirim data
            conn.sendall(alldata)



def download(conn, lokasi_download):
    
    # bagian pertama adalah filename dan kode hash nya
    message = conn.recv(1024)
    message = message.decode("ascii").split(',')
    
    filename = message[0]
    hash_in = message[1]
    
    print()
    print(filename)
    print("sedang cek file dan kode hash nya ...")

    file_download = lokasi_download + "/" + filename

    exists = os.path.isfile(file_download)
    hash_out = 0
    # cek file apakah ada
    if exists:
        # cek kode hash file
        hash_out = generate_file_md5(file_download)

    print("kode file sekarang : " , hash_out)
    
    # jika kode hash file tidak sama dengan kode hash yang di server
    # lakukan replika
    if (hash_out != hash_in):
        print()
        print("file sekarang berbeda dengan file server")
        # kirimkan status
        conn.send("siap replika".encode("ascii"))

        # terima properties size file
        header = conn.recv(4)
    
        # bagian pertama ( [0] ) adalah ID di encode dengan mekanisme yang sama ( >H )
        size = struct.unpack(">I", header)[0]
    
        # membuat file bytes
        myfile = open(file_download, 'wb')

        # menerima payload dan menulis file
        print('sedang replika file sebesar ', size/1000 , ' KB ke ', file_download)
        
        # data diambil sebanyak size
        data = conn.recv(size)
        # bersiap menulis file
        myfile.write(data)
            
        # penulisan harus ditutup
        myfile.close()

        print('berhasil membuat file')
    
    else :
        print("file tidak berubah")
        # jika kode hash sama dengan yang di server, kirimkan pesan
        conn.send(("file sama").encode("ascii"))