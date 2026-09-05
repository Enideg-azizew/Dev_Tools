#!/usr/bin/env python3
"""
Unified encryption and decryption utilities.
"""
import os
import base64
import hashlib
from pathlib import Path
from typing import Union, Optional
from itertools import cycle

class CryptoUtils:
    """Encryption and decryption utilities."""
    
    SALT_SIZE = 32
    ITERATIONS = 100000
    KEY_LENGTH = 32
    
    @staticmethod
    def derive_key(password: str, salt: bytes) -> bytes:
        """Derive a strong key using PBKDF2."""
        if isinstance(password, str):
            password = password.encode('utf-8')
        return hashlib.pbkdf2_hmac(
            'sha256',
            password,
            salt,
            CryptoUtils.ITERATIONS,
            CryptoUtils.KEY_LENGTH
        )
    
    @staticmethod
    def xor_cipher(data: bytes, key: bytes) -> bytes:
        """XOR cipher using cycle on bytes."""
        return bytes(b ^ k for b, k in zip(data, cycle(key)))
    
    @classmethod
    def encrypt_b64(cls, message: str, key: str) -> str:
        """Encrypt a string to base64."""
        key_bytes = hashlib.sha256(key.encode()).digest()
        xor_data = cls.xor_cipher(message.encode(), key_bytes)
        return base64.b64encode(xor_data).decode()
    
    @classmethod
    def decrypt_b64(cls, ciphertext: str, key: str) -> str:
        """Decrypt a base64 string."""
        try:
            key_bytes = hashlib.sha256(key.encode()).digest()
            xor_data = base64.b64decode(ciphertext)
            return cls.xor_cipher(xor_data, key_bytes).decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")
    
    @classmethod
    def encrypt_file(cls, input_path: Union[str, Path], password: str, 
                     output_path: Optional[Union[str, Path]] = None) -> Path:
        """Encrypt a file with password."""
        input_path = Path(input_path)
        if output_path is None:
            output_path = input_path.with_suffix(input_path.suffix + '.enc')
        else:
            output_path = Path(output_path)
        
        salt = os.urandom(cls.SALT_SIZE)
        key = cls.derive_key(password, salt)
        
        with open(input_path, 'rb') as f:
            plaintext = f.read()
        
        ciphertext = cls.xor_cipher(plaintext, key)
        
        with open(output_path, 'wb') as f:
            f.write(salt + ciphertext)
        
        return output_path
    
    @classmethod
    def decrypt_file(cls, input_path: Union[str, Path], password: str,
                     output_path: Optional[Union[str, Path]] = None) -> Path:
        """Decrypt a file with password."""
        input_path = Path(input_path)
        if output_path is None:
            # Remove .enc extension if present
            if input_path.suffix == '.enc':
                output_path = input_path.with_suffix('')
            else:
                output_path = input_path.with_suffix(input_path.suffix + '.decrypted')
        else:
            output_path = Path(output_path)
        
        with open(input_path, 'rb') as f:
            salt = f.read(cls.SALT_SIZE)
            ciphertext = f.read()
        
        key = cls.derive_key(password, salt)
        plaintext = cls.xor_cipher(ciphertext, key)
        
        with open(output_path, 'wb') as f:
            f.write(plaintext)
        
        return output_path
