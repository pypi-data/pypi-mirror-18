#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
基于官方版本修改为同时支持 python2、python3 并整理入一个文件内。
部分参考自 https://github.com/chenjianjx/wechat-encrypt-python3
"""

import xml.etree.cElementTree as ET
import base64
import string
import random
import hashlib
import time
import struct
import socket
import sys

PY2 = False
if sys.version_info[0] == 2:
    PY2 = True

try:
    from Crypto.Cipher import AES
except ImportError:
    print ('please install Crypto at first: $ pip install pycrypto')


Crypt_OK = 0
Crypt_ValidateSignature_Error = -40001
Crypt_ParseXml_Error = -40002
Crypt_ComputeSignature_Error = -40003
Crypt_IllegalAesKey = -40004
Crypt_ValidateAppid_Error = -40005
Crypt_EncryptAES_Error = -40006
Crypt_DecryptAES_Error = -40007
Crypt_IllegalBuffer = -40008
Crypt_EncodeBase64_Error = -40009
Crypt_DecodeBase64_Error = -40010
Crypt_GenReturnXml_Error = -40011


def getSHA1(token, timestamp, nonce, encrypt):
    """用SHA1算法生成安全签名
    @param token:  票据
    @param timestamp: 时间戳
    @param encrypt: 密文
    @param nonce: 随机字符串
    @return: 安全签名
    """
    try:
        sortlist = [token, timestamp, nonce, encrypt]
        sortlist.sort()
        sha = hashlib.sha1()
        sha.update("".join(sortlist).encode('utf-8'))
        return Crypt_OK, sha.hexdigest()
    except Exception:
        return Crypt_ComputeSignature_Error, None


class XMLParse:
    """提供提取消息格式中的密文及生成回复消息格式的接口"""

    # xml消息模板
    AES_TEXT_RESPONSE_TEMPLATE = """<xml>
<Encrypt><![CDATA[%(msg_encrypt)s]]></Encrypt>
<MsgSignature><![CDATA[%(msg_signaturet)s]]></MsgSignature>
<TimeStamp>%(timestamp)s</TimeStamp>
<Nonce><![CDATA[%(nonce)s]]></Nonce>
</xml>"""

    def extract(self, xmltext):
        """提取出xml数据包中的加密消息
        @param xmltext: 待提取的xml字符串
        @return: 提取出的加密消息字符串
        """
        try:
            xml_tree = ET.fromstring(xmltext)
            encrypt = xml_tree.find("Encrypt")
            touser_name = xml_tree.find("ToUserName")
            return Crypt_OK, encrypt.text, touser_name.text
        except Exception:
            return Crypt_ParseXml_Error, None, None

    def generate(self, encrypt, signature, timestamp, nonce):
        """生成xml消息
        @param encrypt: 加密后的消息密文
        @param signature: 安全签名
        @param timestamp: 时间戳
        @param nonce: 随机字符串
        @return: 生成的xml字符串
        """
        resp_dict = {
            'msg_encrypt': encrypt,
            'msg_signaturet': signature,
            'timestamp': timestamp,
            'nonce': nonce,
        }
        resp_xml = self.AES_TEXT_RESPONSE_TEMPLATE % resp_dict
        return resp_xml


class PKCS7Encoder():
    """提供基于PKCS7算法的加解密接口"""

    block_size = 32

    def encode(self, text):
        """ 对需要加密的明文进行填充补位
        @param text: 需要进行填充补位操作的明文
        @return: 补齐明文字符串
        """
        text_length = len(text)
        # 计算需要填充的位数
        amount_to_pad = self.block_size - (text_length % self.block_size)
        if amount_to_pad == 0:
            amount_to_pad = self.block_size
        # 获得补位所用的字符
        if PY2:
            pad = chr(amount_to_pad)
        else:
            pad = bytearray([amount_to_pad])
        return text + pad * amount_to_pad

    def decode(self, decrypted):
        """删除解密后明文的补位字符
        @param decrypted: 解密后的明文
        @return: 删除补位字符后的明文
        """
        pad = ord(decrypted[-1])
        if pad < 1 or pad > 32:
            pad = 0
        return decrypted[:-pad]


class Prpcrypt(object):
    """提供接收和推送给公众平台消息的加解密接口"""

    def __init__(self, key, appid):
        # self.key = base64.b64decode(key+"=")
        self.key = key
        # 设置加解密模式为AES的CBC模式
        self.mode = AES.MODE_CBC
        self.appid = appid

    def encrypt(self, xml):
        """对明文进行加密
        @param text: 需要加密的明文
        @return: 加密得到的字符串
        """
        # 16位随机字符串添加到明文开头
        xml = xml.encode('utf-8')
        if PY2:
            text = self.get_random_str() +\
                struct.pack("I", socket.htonl(len(xml))) + xml + self.appid
        else:
            text = self.get_random_str().encode('utf-8') +\
                struct.pack("I", socket.htonl(len(xml))) +\
                xml + self.appid.encode('utf-8')
        # 使用自定义的填充方式对明文进行补位填充
        pkcs7 = PKCS7Encoder()
        text = pkcs7.encode(text)
        # 加密
        cryptor = AES.new(self.key, self.mode, self.key[:16])
        try:
            ciphertext = cryptor.encrypt(text)
            # 使用BASE64对加密后的字符串进行编码
            result = base64.b64encode(ciphertext).decode("utf8")
            return Crypt_OK, result
        except Exception:
            return Crypt_EncryptAES_Error, None

    def decrypt(self, text):
        """对解密后的明文进行补位删除
        @param text: 密文
        @return: 删除填充补位后的明文
        """
        try:
            cryptor = AES.new(self.key, self.mode, self.key[:16])
            # 使用BASE64对密文进行解码，然后AES-CBC解密
            plain_text = cryptor.decrypt(base64.b64decode(text))
        except Exception:
            # print e
            return Crypt_DecryptAES_Error, None
        try:
            if PY2:
                pad = ord(plain_text[-1])
            else:
                pad = plain_text[-1]
            # 去掉补位字符串
            # pkcs7 = PKCS7Encoder()
            # plain_text = pkcs7.encode(plain_text)
            # 去除16位随机字符串
            content = plain_text[16:-pad]
            xml_len = socket.ntohl(struct.unpack("I", content[: 4])[0])
            xml_content = content[4: xml_len + 4]
            from_appid = content[xml_len + 4:].decode("utf8")
        except Exception:
            return Crypt_IllegalBuffer, None
        if from_appid != self.appid:
            return Crypt_ValidateAppid_Error, None
        return 0, xml_content

    def get_random_str(self):
        """ 随机生成16位字符串
        @return: 16位字符串
        """
        if PY2:
            rule = string.letters + string.digits
        else:
            rule = string.ascii_letters + string.digits
        return "".join(random.sample(rule, 16))


class WXBizMsgCrypt(object):
    # 构造函数
    # @param sToken: 公众平台上，开发者设置的Token
    # @param sEncodingAESKey: 公众平台上，开发者设置的EncodingAESKey
    # @param sAppId: 企业号的AppId
    def __init__(self, sToken, sEncodingAESKey, sAppId):
        try:
            key = base64.b64decode(sEncodingAESKey + "=")
            assert len(key) == 32
        except:
            AssertionError("[error]: EncodingAESKey unvalid !")

        self.token = sToken
        self.pc = Prpcrypt(key, sAppId)

    def EncryptMsg(self, sReplyMsg, sNonce, timestamp=None):
        # 将公众号回复用户的消息加密打包
        # @param sReplyMsg: 企业号待回复用户的消息，xml格式的字符串
        # @param sTimeStamp: 时间戳，可以自己生成，也可以用URL参数的timestamp,如为None则自动用当前时间
        # @param sNonce: 随机串，可以自己生成，也可以用URL参数的nonce
        # sEncryptMsg: 加密后的可以直接回复用户的密文，
        # 包括msg_signature, timestamp, nonce, encrypt的xml格式的字符串
        # return：成功0，sEncryptMsg,失败返回对应的错误码None
        ret, encrypt = self.pc.encrypt(sReplyMsg)
        if ret != 0:
            return ret, None
        if timestamp is None:
            timestamp = str(int(time.time()))
        # 生成安全签名
        ret, signature = getSHA1(self.token, timestamp, sNonce, encrypt)
        if ret != 0:
            return ret, None
        xmlParse = XMLParse()
        return ret, xmlParse.generate(encrypt, signature, timestamp, sNonce)

    def DecryptMsg(self, sPostData, sMsgSignature, sTimeStamp, sNonce):
        # 检验消息的真实性，并且获取解密后的明文
        # @param sMsgSignature: 签名串，对应URL参数的msg_signature
        # @param sTimeStamp: 时间戳，对应URL参数的timestamp
        # @param sNonce: 随机串，对应URL参数的nonce
        # @param sPostData: 密文，对应POST请求的数据
        # xml_content: 解密后的原文，当return返回0时有效
        # @return: 成功0，失败返回对应的错误码
        # 验证安全签名
        xmlParse = XMLParse()
        ret, encrypt, touser_name = xmlParse.extract(sPostData)
        if ret != 0:
            return ret, None
        ret, signature = getSHA1(self.token, sTimeStamp, sNonce, encrypt)
        if ret != 0:
            return ret, None
        if not signature == sMsgSignature:
            return Crypt_ValidateSignature_Error, None
        ret, xml_content = self.pc.decrypt(encrypt)
        if not PY2:
            xml_content = xml_content.decode('utf-8')
        return ret, xml_content
