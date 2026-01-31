import sys
import socket

def usage():
    print("Usage: python controller.py <shadow_file> <username>")
    sys.exit(0)

def parse_args():
    if(len(sys.argv) != 3):
        usage()
    sf = sys.argv[1]
    un = sys.argv[2]
    return sf, un

def get_user_hash(shadow_file, username:str):
    shadow_content = []
    with open(shadow_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # split only on the first ":" in case weird stuff appears later
            user, rest = line.split(":", 1)

            if user == username:
                # rest is the hash field (may include trailing stuff)
                return rest.strip()

    raise ValueError(f"Username '{username}' not found in {shadow_path}")


def main():
    shadow_file, username = parse_args()
    print(f"Shadow file: {shadow_file} Username: {username}" )

    shadow_file_content = get_user_hash(shadow_file, username)
    print(shadow_file_content)
    

    host = "0.0.0.0"
    port = 6767
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host,port))
    server.listen(1)
    print(f"Listening on {host}:{port}")

    conn, addr = server.accept()
    print(f"Connection from {addr}")
    

    data = conn.recv(1024)
    if data:
        message = data.decode().strip()
        print(f"Received: {message}")

    conn.sendall(shadow_file_content.encode())


if __name__=="__main__":
    main()
