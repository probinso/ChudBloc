import hashlib
import yaml
import bcrypt

def digest_str(data):
    return digest_data(str.encode(data))

def digest_data(data):
    with open("./config.yml") as fd:
        config = yaml.safe_load(fd)

    DIGEST_ALG = config["crypt"]["hash_name"]
    ENCODING = config["crypt"]["encoding"]
    SALT = bytes(config["crypt"]["salt"], ENCODING)
    ITERATIONS = int(config["crypt"]["depth"])

    digest = hashlib.pbkdf2_hmac(
        DIGEST_ALG,
        bytes(data, 'utf-8'),
        SALT,
        ITERATIONS
    )
    del DIGEST_ALG, SALT, ITERATIONS, config
    return digest
