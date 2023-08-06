import ssl
import socket
from tools import verify, fromFile

DEFAULT_PORT = 4446
LOCAL = 'localhost'
EOF = 'EOF'
SOCKET_BUFFER_SIZE = 1024

ANALYZER_MODE = 1000
VERIFIER_MODE = 1001
REQUEST_MODE = 1010
RESPOND_MODE = 1100

class Connector:
    def sendFile(self, sslSocket, filename):
        offset = 0
        try:
            with open(filename, 'rb') as key:
                while True:
                    sent = sslSocket.sendfile(key, offset)
                    if sent == 0:
                        sslSocket.send(str.encode(EOF))
                        break
                    offset += sent
        except FileNotFoundError as fne:
            sslSocket.send(str.encode(EOF))

    def receiveFile(self, sslSocket, filename):
        with open(filename, 'wb') as key:
            while True:
                data = sslSocket.recv(SOCKET_BUFFER_SIZE)
                if data == str.encode(EOF):
                    break
                key.write(data)

    def setupTLSServer(self):
        serverContext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        serverContext.set_ecdh_curve('prime256v1')
        serverContext.verify_mode = ssl.CERT_REQUIRED
        serverContext.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384')
        serverContext.options |= ssl.OP_NO_COMPRESSION
        serverContext.options |= ssl.OP_SINGLE_ECDH_USE
        serverContext.options |= ssl.OP_CIPHER_SERVER_PREFERENCE
        serverContext.load_cert_chain(certfile='connection/client.pem', keyfile='connection/client.key')
        serverContext.load_verify_locations(cafile='connection/ca.pem')
        return serverContext

    def createTLSClient(self):
        clientContext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        clientContext.verify_mode = ssl.CERT_REQUIRED
        clientContext.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384')
        clientContext.options |= ssl.OP_NO_COMPRESSION
        clientContext.load_cert_chain(certfile='connection/server.pem', keyfile='connection/server.key')
        clientContext.load_verify_locations(cafile='connection/ca.pem')
        return clientContext

    def createServerHandler(self, flag, HOST=LOCAL, PORT=DEFAULT_PORT, maxClients=1):
        serverSocket = self.createTCPSocket()
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSocket.bind((HOST, PORT))
        serverSocket.listen(maxClients)
        conn, addr = serverSocket.accept()
        sslContext = self.setupTLSServer()
        sslSocket = sslContext.wrap_socket(conn, server_side=True)
        serverHandler = ServerHandler(sslSocket, flag)
        serverHandler.handle(self)

    def createClientHandler(self, flag, host=LOCAL, port=DEFAULT_PORT):
        clientSocket = self.createTCPSocket()
        clientSocket.connect((host, port))
        sslContext = self.createTLSClient()
        sslSocket = sslContext.wrap_socket(clientSocket, server_side=False)
        clientHandler = ClientHandler(sslSocket, flag)
        clientHandler.handle(self)

    def createTCPSocket(self):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return clientSocket

    pass


class ClientHandler:
    """ This handler handles all ANALYZER_MODE, VERIFIER_MODE, and REQUEST_MODE queries """

    def __init__(self, sslSocket, flag):
        self.sslSocket = sslSocket
        self.flag = flag

    def handle(self, connector):
        if self.flag == ANALYZER_MODE:
            connector.sendFile(self.sslSocket, 'enclog.txt')
            connector.sendFile(self.sslSocket, 'publickey.pkl')
            connector.sendFile(self.sslSocket, 'randoms.pkl')

        elif self.flag == VERIFIER_MODE:
            connector.sendFile(self.sslSocket, 'hashlog.txt')
            connector.sendFile(self.sslSocket, 'keys.pkl')
            connector.sendFile(self.sslSocket, 'negatives.pkl')
            connector.sendFile(self.sslSocket, 'threshold.pkl')

        elif self.flag == REQUEST_MODE:
            connector.sendFile(self.sslSocket, 'sums.pkl')
            connector.receiveFile(self.sslSocket, 'possibledecrypted.pkl')

    def close(self):
        self.sslSocket.close()


class ServerHandler:
    """ This handler handles all ANALYZER_MODE, VERIFIER_MODE and RESPOND_MODE queries """

    def __init__(self, sslSocket, flag):
        self.sslSocket = sslSocket
        self.flag = flag

    def handle(self, connector):
        if self.flag == ANALYZER_MODE:
            connector.receiveFile(self.sslSocket, 'analyzerlog.txt')
            connector.receiveFile(self.sslSocket, 'analyzerkey.pkl')
            connector.receiveFile(self.sslSocket, 'analyzerrandoms.pkl')
        elif self.flag == VERIFIER_MODE:
            connector.receiveFile(self.sslSocket, 'verifierlog.txt')
            connector.receiveFile(self.sslSocket, 'verifierkeys.pkl')
            connector.receiveFile(self.sslSocket, 'verifiernegatives.pkl')
            connector.receiveFile(self.sslSocket, 'verifierthreshold.pkl')
        elif self.flag == RESPOND_MODE:
            connector.receiveFile(self.sslSocket, 'verifiersums.pkl')
            threshold = fromFile('verifierthreshold.pkl')
            verify('verifierkeys.pkl', 'verifiersums.pkl', 'verifierlog.txt', 'verifiernegatives.pkl', threshold)
            connector.sendFile(self.sslSocket, 'response.pkl')

    def close(self):
        self.sslSocket.close()
