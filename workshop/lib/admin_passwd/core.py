#!/usr/bin/env python3

from base64 import b64encode
from base64 import b64decode
import random
from Crypto.Cipher import AES
from hashlib import sha256


DIGITS = "0123456789"
ALPHABETS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS_AND_ALPHABETS = DIGITS + ALPHABETS


class AESCipher(object):
    def __init__(self, key, block_size=32):
        self.block_size = block_size
        if len(key) >= block_size:
            self.key = key[:block_size]
        else:
            self.key = self.pad(key)

    def generate_salt(self, digit_num):
        if type(digit_num) != int:
            raise TypeError("digit num must be init")
        randomly_chosens = random.sample(
                                    DIGITS_AND_ALPHABETS,
                                    digit_num
                                        )
        bin_rnd_salt = "".join(randomly_chosens).encode()
        return bin_rnd_salt

    def encrypt(self, raw):
        encode_cipher, salt = self._make_encode_cipher_and_salt()
        raw_16 = self.pad(raw)
        encrypted_raw = salt + encode_cipher.encrypt(raw_16.encode())
        encoded_b64 = b64encode(encrypted_raw)
        return encoded_b64

    def _make_encode_cipher_and_salt(self):
        salt = self.generate_salt(AES.block_size)
        salted = ''.encode()
        dx = ''.encode()
        # two times.
        while len(salted) < 48:
            hash_input = dx + self.key.encode() + salt
            dx = sha256(hash_input).digest()
            salted = salted + dx
        key = salted[0:32]
        initialize_vecs = salted[32:48]
        cipher = AES.new(key, AES.MODE_CBC, initialize_vecs)
        return cipher, salt

    def decrypt(self, enc):
        b64_enc = b64decode(enc)
        b64_enc_base = b64_enc[AES.block_size:]
        cipher = self._make_decoder_cipher_ins(enc)
        raw = cipher.decrypt(b64_enc_base).decode()
        raw = self.unpad(raw)
        return raw

    def _make_decoder_cipher_ins(self, enc):
        enc = b64decode(enc)
        salt = enc[0:AES.block_size]
        data00 = self.key.encode() + salt
        hash_dict = {}
        hash_dict[0] = sha256(data00).digest()
        result = hash_dict[0]
        for i in range(1, 3):
            hash_dict[i] = sha256(hash_dict[i - 1] + data00).digest()
            result += hash_dict[i]
        key = result[:32]
        iv = result[32:48]
        decode_cipher = AES.new(key, AES.MODE_CBC, iv)
        return decode_cipher

    def unpad(self, st):
        pad_st = st[-1]
        pad_num = ord(pad_st)
        unpaded_st = st[:-pad_num]
        return unpaded_st

    def pad(self, st):
        uoccupied_spnum = (self.block_size - len(st)) % self.block_size
        amend = chr(uoccupied_spnum) * uoccupied_spnum
        new_wd = st + amend
        return new_wd
