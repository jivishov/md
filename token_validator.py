import jwt
import streamlit as st
from datetime import datetime
import os
from typing import Dict, Optional

class JWTValidator:
    """Handles JWT token validation for Streamlit-Flask authentication"""
    
    def __init__(self):
        """Initialize with JWT configuration"""
        self.jwt_secret = os.getenv('JWT_SECRET_KEY')
        if not self.jwt_secret:
            raise ValueError("JWT_SECRET_KEY not found in environment variables")
            
    
    def validate_token(self, token: str) -> Optional[Dict]:
        """
        Validate JWT token and return user info if valid
        
        Args:
            token: JWT token string
            
        Returns:
            dict: User information if token is valid
            None: If token is invalid or expired
        """
        try:
            # Decode and verify the token
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=['HS256']
            )
            
            # Check if token has expired
            exp = datetime.fromtimestamp(payload['exp'])
            if exp < datetime.utcnow():
                return None
                
            return {
                'user_id': payload['user_id'],
                'email': payload['email'],
                'name': payload['name']
            }
            
        except jwt.ExpiredSignatureError:
            st.error("Your session has expired. Please log in again.")
            return None
        except jwt.InvalidTokenError:
            st.error("Invalid authentication token. Please log in again.")
            return None
        except Exception as e:
            st.error(f"Authentication error: {str(e)}")
            return None
    
    def check_token_in_params(self) -> Optional[Dict]:
        """
        Check for token in URL parameters and validate it
        
        Returns:
            dict: User information if valid token found
            None: If no valid token found
        """
        # Check if token exists in params
        try:
            token = st.query_params["token"]
            
            # Validate token
            user_info = self.validate_token(token)
            if user_info:
                # Store user info in session state
                st.session_state['authenticated'] = True
                st.session_state['user'] = user_info
                
                # Clear token from URL
                st.query_params.token = None
                
                return user_info
        except KeyError:
            # Token not found in query params
            return None
        
        return None
    
    def is_authenticated(self) -> bool:
        """
        Check if user is currently authenticated
        
        Returns:
            bool: True if user is authenticated, False otherwise
        """
        return st.session_state.get('authenticated', False)
    
    def get_current_user(self) -> Optional[Dict]:
        """
        Get current authenticated user information
        
        Returns:
            dict: Current user information if authenticated
            None: If not authenticated
        """
        return st.session_state.get('user') if self.is_authenticated() else None
    
    def logout(self):
        """Clear authentication state"""
        if 'authenticated' in st.session_state:
            del st.session_state['authenticated']
        if 'user' in st.session_state:
            del st.session_state['user']
        # Clear token from URL
        st.query_params.token = None
