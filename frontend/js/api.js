// API Configuration
const API_URL = 'https://your-backend-api-url.com'; // Replace with your actual backend API URL

// API Functions
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
                password,
                theme: localStorage.getItem('theme') || 'light',
                language: localStorage.getItem('language') || 'en'
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Registration failed');
        }
        
        // Save token and user data
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        return data;
    } catch (error) {
        console.error('Register error:', error);
        throw error;
    }
}

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
        
        if (!response.ok) {
            throw new Error(data.message || 'Login failed');
        }
        
        // Save token and user data
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        // Update UI theme and language from user preferences
        if (data.user.theme) {
            setTheme(data.user.theme);
        }
        
        if (data.user.language) {
            setLanguage(data.user.language);
        }
        
        return data;
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}

async function getUserInfo() {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('Not authenticated');
        }
        
        const response = await fetch(`${API_URL}/api/user`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            if (response.status === 401) {
                // Token expired or invalid
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                updateAuthUI();
            }
            throw new Error(data.message || 'Failed to get user info');
        }
        
        // Update stored user data
        localStorage.setItem('user', JSON.stringify(data.user));
        
        return data.user;
    } catch (error) {
        console.error('Get user info error:', error);
        throw error;
    }
}

async function updateUserSettings(settings) {
    try {
        const token = localStorage.getItem('token');
        if (!token) {
            // Not logged in, just update local settings
            return false;
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
        
        if (!response.ok) {
            if (response.status === 401) {
                // Token expired or invalid
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                updateAuthUI();
            }
            throw new Error(data.message || 'Failed to update settings');
        }
        
        // Update stored user data
        localStorage.setItem('user', JSON.stringify(data.user));
        
        return true;
    } catch (error) {
        console.error('Update settings error:', error);
        return false;
    }
}

async function createCheckoutSession(voucher = null) {
    try {
        // Check if user is logged in
        if (!isLoggedIn()) {
            // Redirect to login page
            window.location.href = 'login.html?redirect=checkout';
            return;
        }
        
        const token = localStorage.getItem('token');
        
        const response = await fetch(`${API_URL}/api/create-checkout-session`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                voucher: voucher,
                success_url: `${window.location.origin}/checkout-success.html`,
                cancel_url: `${window.location.origin}/checkout-cancel.html`,
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Failed to create checkout session');
        }
        
        // Redirect to Stripe checkout
        window.location.href = data.url;
    } catch (error) {
        console.error('Checkout error:', error);
        showFlashMessage('Error creating checkout session: ' + error.message, 'error');
    }
}

// Handle form submissions
document.addEventListener('DOMContentLoaded', function() {
    // Login form
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            try {
                await login(username, password);
                
                // Check for redirect parameter
                const urlParams = new URLSearchParams(window.location.search);
                const redirect = urlParams.get('redirect');
                
                if (redirect === 'checkout') {
                    // Redirect to checkout
                    createCheckoutSession();
                } else {
                    // Redirect to home page
                    window.location.href = 'index.html';
                }
            } catch (error) {
                showFlashMessage(error.message, 'error');
            }
        });
    }
    
    // Registration form
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const password2 = document.getElementById('password2').value;
            
            if (password !== password2) {
                showFlashMessage('Passwords do not match', 'error');
                return;
            }
            
            try {
                await register(username, email, password);
                showFlashMessage('Registration successful! You are now logged in.', 'success');
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 2000);
            } catch (error) {
                showFlashMessage(error.message, 'error');
            }
        });
    }
    
    // Settings form
    const settingsForm = document.getElementById('settings-form');
    if (settingsForm) {
        settingsForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const theme = document.getElementById('theme').value;
            const language = document.getElementById('language').value;
            
            try {
                await updateUserSettings({ theme, language });
                setTheme(theme);
                setLanguage(language);
                showFlashMessage('Settings updated successfully', 'success');
            } catch (error) {
                showFlashMessage(error.message, 'error');
            }
        });
    }
});