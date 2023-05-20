import rsa
import rsa.randnum
import pyAesCrypt
import random
import string

def generate_keys():
    return rsa.newkeys(1024, poolsize=2)


def main():
    receiver_pub, receiver_priv = generate_keys()
    shared_key = str(''.join(random.choices(string.ascii_letters + string.digits, k=50)))
    pyAesCrypt.encryptFile("secret.txt", "protectedsecret.txt.aes", shared_key)
    encrypted_shared_key = rsa.encrypt(bytes(shared_key, 'utf-8'), receiver_pub)
    print(type(encrypted_shared_key))
    shared_key_2 = rsa.decrypt(encrypted_shared_key, receiver_priv).decode('utf-8')
    pyAesCrypt.decryptFile("protectedsecret.txt.aes", "secret1.txt", shared_key_2)





if __name__ == "__main__":
    main()