// API.js - For interacting with the DiscoBots.fr API

// API URL - You should replace this with your actual API URL when deploying
// For Netlify, this will be replaced by the environment variable through netlify.toml
const API_URL = window.API_URL || 'http://localhost:5000';

// Try to get API_URL from Netlify environment
document.addEventListener('DOMContentLoaded', function() {
  // This script tag will be injected by Netlify with the API_URL
  // <script>window.API_URL = "https://api.discobots.fr";</script>
  if (!window.API_URL) {
    console.log('API_URL not set, using localhost for development');
  }
});

// Register a new user
async function register(username, email, password) {
    try {
        const response = await fetch(`${API_URL}/api/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username,
                email,
                password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            return { success: true, message: data.message };
        } else {
            return { success: false, message: data.message || 'Registration failed' };
        }
    } catch (error) {
        console.error('Registration error:', error);
        return { success: false, message: 'Network error. Please try again later.' };
    }
}

// Login user
async function login(username, password) {
    try {
        const response = await fetch(`${API_URL}/api/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username,
                password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Store token in localStorage
            localStorage.setItem('token', data.token);
            return { success: true, message: data.message };
        } else {
            return { success: false, message: data.message || 'Login failed' };
        }
    } catch (error) {
        console.error('Login error:', error);
        return { success: false, message: 'Network error. Please try again later.' };
    }
}

// Get current user information
async function getUserInfo() {
    try {
        const token = localStorage.getItem('token');
        
        if (!token) {
            return null;
        }
        
        const response = await fetch(`${API_URL}/api/user`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            return await response.json();
        } else {
            // If unauthorized, clear token
            if (response.status === 401) {
                localStorage.removeItem('token');
            }
            return null;
        }
    } catch (error) {
        console.error('User info error:', error);
        return null;
    }
}

// Update user settings
async function updateUserSettings(settings) {
    try {
        const token = localStorage.getItem('token');
        
        if (!token) {
            return { success: false, message: 'Not logged in' };
        }
        
        const response = await fetch(`${API_URL}/api/settings`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(settings)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            return { success: true, message: data.message };
        } else {
            // If unauthorized, clear token
            if (response.status === 401) {
                localStorage.removeItem('token');
            }
            return { success: false, message: data.message || 'Failed to update settings' };
        }
    } catch (error) {
        console.error('Update settings error:', error);
        return { success: false, message: 'Network error. Please try again later.' };
    }
}

// Create a checkout session
async function createCheckoutSession(voucher = null) {
    try {
        const token = localStorage.getItem('token');
        
        if (!token) {
            return { success: false, message: 'Not logged in' };
        }
        
        const response = await fetch(`${API_URL}/api/create-checkout-session`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ voucher })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            return { success: true, url: data.url };
        } else {
            // If unauthorized, clear token
            if (response.status === 401) {
                localStorage.removeItem('token');
            }
            return { success: false, message: data.message || 'Failed to create checkout session' };
        }
    } catch (error) {
        console.error('Checkout error:', error);
        return { success: false, message: 'Network error. Please try again later.' };
    }
}