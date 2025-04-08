// API integration for DiscoBots frontend
const API_URL = '/api';

async function register(username, email, password) {
    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }),
        });
        return await response.json();
    } catch (error) {
        console.error('Registration error:', error);
        return { success: false, message: 'Network error occurred' };
    }
}

async function login(username, password) {
    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });
        const data = await response.json();
        if (data.success) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
        }
        return data;
    } catch (error) {
        console.error('Login error:', error);
        return { success: false, message: 'Network error occurred' };
    }
}

async function getUserInfo() {
    const token = localStorage.getItem('token');
    if (!token) {
        return null;
    }
    
    try {
        const response = await fetch(`${API_URL}/user`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        return await response.json();
    } catch (error) {
        console.error('Get user info error:', error);
        return null;
    }
}

async function updateUserSettings(settings) {
    const token = localStorage.getItem('token');
    if (!token) {
        return { success: false, message: 'Not authenticated' };
    }
    
    try {
        const response = await fetch(`${API_URL}/settings`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(settings),
        });
        return await response.json();
    } catch (error) {
        console.error('Update settings error:', error);
        return { success: false, message: 'Network error occurred' };
    }
}

async function createCheckoutSession(voucher = null) {
    const token = localStorage.getItem('token');
    const headers = {
        'Content-Type': 'application/json'
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        const response = await fetch(`${API_URL}/create-checkout`, {
            method: 'POST',
            headers,
            body: JSON.stringify({ voucher }),
        });
        const data = await response.json();
        if (data.success && data.url) {
            window.location.href = data.url;
        }
        return data;
    } catch (error) {
        console.error('Checkout error:', error);
        return { success: false, message: 'Network error occurred' };
    }
}
