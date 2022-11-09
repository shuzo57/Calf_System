import socket

server_ip : str = "192.168.1.67"
server_port : int = 4200

for i in range(30):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))
    sock.close()


"""
サーバーのソケットが接続待機状態にあるので
Ctrl + C を行っても
サーバーを強制終了させることができない
そこで、サーバーに繋ぐためだけのプログラムを作成した。
"""
