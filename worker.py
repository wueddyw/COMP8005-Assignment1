import sys
import socket
from passlib.hash import sha256_crypt, sha512_crypt, md5_crypt, bcrypt
import json, struct, argparse, platform, time

CHARSET = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789"
    "!@#$%^&*()-_=+[]{};:,.<>/?"
    )

def usage():
    print("Usage: python controller.py <Host> <Port>")
    sys.exit(0)

def parse_args():
    if(len(sys.argv) != 3):
        usage()
    host = sys.argv[1]
    port = sys.argv[2]
    return host, int(port)

def crack_md5(target_hash: str, length: int = 3, charset: str = CHARSET):
    handler = determine_cracking_algorithm(target_hash)
    for c1 in CHARSET:
        for c2 in CHARSET:
            for c3 in CHARSET:
                candidate = c1 + c2 + c3
                if handler.verify(candidate, target_hash):
                    return candidate   # FOUND
    return None  # NOT FOUND

def determine_cracking_algorithm(full_hash: str):
    """
    Returns the correct passlib hash handler based on the UNIX shadow hash prefix.
    Raises ValueError for unsupported/invalid hashes.
    """

    if not full_hash or full_hash.strip() == "":
        raise ValueError("Empty hash field (no password set)")

    # locked/disabled accounts in shadow often start with '!' or '*'
    if full_hash[0] in ("!", "*"):
        raise ValueError("Account locked/disabled (hash starts with ! or *)")

    # Most modern formats start with "$"
    if not full_hash.startswith("$"):
        raise ValueError(f"Unrecognized hash format: {full_hash[:20]}")

    # Extract the id between the first two '$'
    # Example: "$1$salt$hash" -> parts = ["", "1", "salt", "hash"]
    parts = full_hash.split("$")
    if len(parts) < 3:
        raise ValueError("Malformed hash (not enough $ fields)")

    alg_id = parts[1]

    # Map algorithm identifiers
    if alg_id == "y":
        return yescrypt
    elif alg_id in ("2a", "2b", "2y"):
        return bcrypt
    elif alg_id == "5":
        return sha256_crypt
    elif alg_id == "6":
        return sha512_crypt
    elif alg_id == "1":
        return md5_crypt

    raise ValueError(f"Unsupported algorithm id: {alg_id}")


def main():
    host,port = parse_args()
    print(f"Host: {host} Port: {port}")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host,port))

    client.sendall("I am ready".encode())
    message= None
    data = client.recv(1024)
    if data:
        message = data.decode().strip()
        print(f"Received: {message}")

    # Generate a UNIX-style MD5 hash
    hash_val = bcrypt.hash("abb")

    print("Hash:", hash_val)

    # Verify correct password

    
    handler = determine_cracking_algorithm(message)
    # if handler is md5_crypt:
    #     result = crack_md5(message)
    #     print(result)

    print("Cracked Password:", crack_md5("$5$rounds=535000$HMC5nXbJKNZcLdYW$1W2jbzFsUT68kUWjzMSvG30UHSCuwvxj8KRsfmBfDi1"))

    # # Verify wrong password
    # print("Verify xyz:", md5_crypt.verify("xyz", hash_val))
    

if __name__=="__main__":
    main()

