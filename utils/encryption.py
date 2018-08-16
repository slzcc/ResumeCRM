import hashlib
from django import conf

def md5(arg):
    Hash = hashlib.md5(conf.settings.SECRET_KEY.encode("utf-8"))
    Hash.update(arg.encode("utf-8"))
    return Hash.hexdigest()