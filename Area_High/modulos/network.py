
from HOST_PORT import HOSTPORT

try:
    # import logging
    import socket
    import threading
    import socketserver
    # import sys
except Exception as ex:
    raise Exception(f"ERROR:\n{ex}")

client_sid = 1000000000
client_max_device = 10000

satellite_sid = 2000000000
satellite_max_device = 10000

class CustomTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        try:
            # self.request is the TCP socket connected to the client
            
            self.data = self.request.recv(1024).strip()
            
            print("{} wrote:".format(self.client_address[1]))
            print(self.data)
            low_db = 2
            data_byte = lower_snr(self.data,low_db)
            print(data_byte)
            # Send forward the same data, with lower snr
            # if(self.client_address[1] == HOSTPORT['Satellite']):
            #     print("Forward Lower")
            #     forward_socket(HOSTPORT['Area_High_OUT'],HOSTPORT['Area_Low'],data_byte)
            #     forward_socket(HOSTPORT['Area_High_OUT'],HOSTPORT['Attacker'],data_byte)
            # else:
            #     forward_socket(HOSTPORT['Area_High_OUT'],HOSTPORT['Satellite'],data_byte)

            if satellite_sid < satellite_sid < satellite_sid + satellite_max_device:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect(("localhost", 8014))
                    sock.sendall(data_byte)

            

        except Exception as ex:
            print(f"ERROR:\n{ex}")


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        try:
            data = str(self.request.recv(1024), 'ascii')
            cur_thread = threading.current_thread()
            response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
            self.request.sendall(response)
        except Exception as ex:
            print(f"ERROR:\n{ex}")


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def client(ip, port, message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))
            sock.sendall(bytes(message, 'ascii'))
            response = str(sock.recv(1024), 'ascii')
            print("Received: {}".format(response))
    except Exception as ex:
            print(f"ERROR:\n{ex}")



class MyTcpHandler(socketserver.BaseRequestHandler):
    # BaseRequestHandler is specifically used to process communication-related information
    def handle(self):
        try:
            # Here must define a handle method, and the method name must be handle, sockerserver will automatically call the handle method
            print(self.request)  # The self.request here is equivalent to the conn object we saw before (conn,client_addr=server.accept())
            while True:
                try:
                    recv_cliend_cmd = self.request.recv(1024) # Receive instructions from the client
                    if not recv_cliend_cmd:
                        break
                        # Next, we will process the instructions sent by the client
                    obj = subprocess.Popen(recv_cliend_cmd.decode('utf-8'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout = obj.stdout.read()
                    stderr = obj.stderr.read()
                    # Let's create the header (write it at will), here we really use the total_size in the dictionary
                    # header_dic={
                    #         'total_size':len(stdout)+len(stderr),
                    #         'filename':'xxx.mp4',
                    #         'md5sum':'8f6fbf8347faa4924a76856701edb0f3'
                    # }
                    # header_json = json.dumps(header_dic)
                    print(stderr)
                    # header_bytes = header_json.encode('utf-8')
                    # self.request.send(struct.pack('i', len(header_bytes)))  # This sent a fixed number of bytes in the past 4, so the client can receive four bytes for the first time
                    # self.request.send(header_bytes)
                    # self.request.send(stdout)
                    # self.request.send(stderr)
                    self.request.sendall(self.data.upper())

                except ConnectionResetError:
                    break
            self.request.close()
        except Exception as ex:
            print(f"ERROR:\n{ex}")


class MyTCPHandler(socketserver.StreamRequestHandler):

    def handle(self):
        try:
            # self.rfile is a file-like object created by the handler;
            # we can now use e.g. readline() instead of raw recv() calls
            self.data = self.rfile.readline().strip()
            print("{} wrote:".format(self.client_address[0]))
            print(self.data)
            # Likewise, self.wfile is a file-like object used to write back
            # to the client
            self.wfile.write(self.data.upper())
        except Exception as ex:
            print(f"ERROR:\n{ex}")





def lower_snr(data,lower_db,which_byte = 0):
        #byte_data = bytes(data, 'utf-8')
        byte_data = list(data)
        byte_data[which_byte] = byte_data[which_byte] - lower_db
        return bytes(byte_data)


def forward_socket(src_port, dst_port,data):
    HOST = "localhost"
    # Create a socket (SOCK_STREAM means a TCP socket)
    try :
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to server and send data
        sock.bind((HOST,src_port))
        sock.connect((HOST, dst_port))
        sock.sendall(data)
        print(f"Sent FROM:  {src_port} ==> TO:  {dst_port}")
    except:
        print(f"Failed FROM:  {src_port} ==> TO:  {dst_port}")