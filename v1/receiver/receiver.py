import rsa
from cryptography.fernet import Fernet

####STEP 1
def generate_keys():
    return rsa.newkeys(1024, poolsize=2)


def main():
    receiver_pub, receiver_priv = generate_keys()
    with open('public.pem', mode='wb') as publicfile:
        publicfile.write(receiver_pub.save_pkcs1("PEM"))
    input("Save shared key encrypted file as key.[extension]. Then hit enter: ") #send public.pem


    with open('enc_shared_key.txt', mode='rb') as enc_shared_key:
        shared_key = rsa.decrypt(enc_shared_key, receiver_priv)

    with open('protectedsecret.txt', mode='rb') as prot_secret:
        encrypted_secret = rsa.decrypt(prot_secret, receiver_priv)

    decrypter = Fernet(shared_key)
    secret = decrypter.decrypt(encrypted_secret)
    
    with open('secret.txt', 'wb') as file:
        file.write(secret)

    
    



if __name__ == '__main__':
    main()

# with open('private.pem', mode='rb') as privatefile:
#    data = privatefile.read()
# private_key = rsa.PrivateKey.load_pkcs1(data)
