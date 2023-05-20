import rsa
from cryptography.fernet import Fernet
import os

####STEP 1 - Reciever
def generate_keys():    
    return rsa.newkeys(1024, poolsize=2)


def main():
    user1_pub, user1_priv = generate_keys()
    message = 'hello Bob!'.encode('utf8')
    crypted_message = rsa.encrypt(message, user1_pub)
    print(crypted_message)

####STEP 2 - Reciever




if __name__ == '__main__':
    main()

# with open('private.pem', mode='rb') as privatefile:
#    data = privatefile.read()
# private_key = rsa.PrivateKey.load_pkcs1(data)
