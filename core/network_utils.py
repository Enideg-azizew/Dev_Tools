#!/usr/bin/env python3
"""
Network utilities for remote control and communication.
"""
import socket
import requests
import json
from typing import Optional, Dict, Any
from urllib.parse import urlparse

class NetworkUtils:
    """Network and remote communication utilities."""
    
    @staticmethod
    def get_local_ip() -> str:
        """Get the local IP address."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"
    
    @staticmethod
    def check_port(port: int, host: str = "0.0.0.0") -> bool:
        """Check if a port is available."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            sock.close()
            return result != 0
        except Exception:
            return False
    
    @staticmethod
    def get_public_ip() -> Optional[str]:
        """Get the public IP address."""
        try:
            response = requests.get("https://api.ipify.org?format=json", timeout=5)
            return response.json().get('ip')
        except Exception:
            try:
                response = requests.get("https://httpbin.org/ip", timeout=5)
                return response.json().get('origin')
            except Exception:
                return None
    
    @staticmethod
    def is_url_reachable(url: str, timeout: int = 5) -> bool:
        """Check if a URL is reachable."""
        try:
            response = requests.head(url, timeout=timeout)
            return response.status_code < 500
        except Exception:
            return False
    
    @staticmethod
    def get_qr_code_data(url: str) -> str:
        """Generate QR code data as base64."""
        try:
            import qrcode
            from PIL import Image
            import io
            import base64
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode()
        except ImportError:
            return ""
