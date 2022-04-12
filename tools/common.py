import os
import sys
sys.path.append("..")
sys.path.append(".")


def getPythonDataBase():
    profile = os.getenv('PY_DB_TP')
    if profile:
        return profile
    else:
        return 'dev'


def Base64Encrypt(content):
    import base64
    return base64.b64encode(content.encode()).decode()


def Base64Decrypt(content_base64):
    import base64
    return base64.b64decode(content_base64).decode()


def RSADecrypt(cipher_text):
    # b.py
    import base64
    from Crypto import Random
    from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
    from Crypto.PublicKey import RSA
    rsa_private_key = ''
    with open('private.pem', 'r') as f:
        rsa_private_key = f.read()
    rsakey = RSA.importKey(rsa_private_key)  # 导入私钥
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    text = cipher.decrypt(base64.b64decode(cipher_text), None)
    content = text.decode('utf8')
    print(content)
    return content


def genKey():
    # a.py
    from Crypto import Random
    from Crypto.PublicKey import RSA

    random_generator = Random.new().read
    rsa = RSA.generate(1024, random_generator)

    # 生成私钥
    private_key = rsa.exportKey()
    with open('private.pem', 'w') as f:
        f.write(private_key.decode('utf-8'))

    # 生成公钥
    public_key = rsa.publickey().exportKey()
    with open('public.pem', 'w') as f:
        f.write(public_key.decode('utf-8'))
