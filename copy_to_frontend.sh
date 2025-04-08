#!/bin/bash

# Create necessary directories
mkdir -p frontend/css frontend/js frontend/img

# Copy CSS files
cp static/css/styles.css frontend/css/

# Copy JS files
cp static/js/particles.js frontend/js/
cp static/js/main.js frontend/js/

# Copy images (if any)
cp -r static/img/* frontend/img/ 2>/dev/null
cp static/favicon.ico frontend/img/ 2>/dev/null

# Create api.js for frontend
cat > frontend/js/api.js << 'EOL'
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
EOL

# Process HTML files from templates and convert them to standalone files
for file in templates/*.html; do
  if [[ $(basename "$file") != "base.html" ]]; then
    # Get filename without extension
    filename=$(basename "$file" .html)
    
    # Handle specific file renaming
    if [[ "$filename" == "checkout_cancel" ]]; then
      output_file="frontend/checkout-cancel.html"
    elif [[ "$filename" == "checkout_success" ]]; then
      output_file="frontend/checkout-success.html"
    else
      output_file="frontend/${filename}.html"
    fi
    
    # Create standalone HTML files (simple copy for now)
    cat "$file" > "$output_file"
  fi
done

# Create a checkout.html file
cat > frontend/checkout.html << 'EOL'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DiscoBots - Checkout</title>
    <link rel="stylesheet" href="/css/styles.css">
    <link rel="icon" type="image/x-icon" href="/img/favicon.ico">
</head>
<body>
    <header>
        <div class="container">
            <nav>
                <div class="logo">
                    <a href="/">
                        <img src="/img/logo.png" alt="DiscoBots Logo" height="40">
                        <span>DiscoBots</span>
                    </a>
                </div>
                <ul class="nav-links">
                    <li><a href="/">Home</a></li>
                    <li><a href="/discord.html">Discord Server</a></li>
                    <li><a href="/terms.html">Terms & Privacy</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main>
        <section class="checkout-section">
            <div class="container">
                <h1>Complete Your Purchase</h1>
                <div class="checkout-options">
                    <div class="checkout-card">
                        <h2>Standard Plan</h2>
                        <p class="price">$5.99</p>
                        <ul class="features">
                            <li>24/7 Bot Uptime</li>
                            <li>Priority Support</li>
                            <li>All Commands Unlocked</li>
                            <li>Custom Prefix</li>
                        </ul>
                        <div class="voucher-container">
                            <input type="text" id="voucher" placeholder="Voucher Code">
                            <p id="voucher-message"></p>
                        </div>
                        <button id="checkout-button" class="btn primary">Proceed to Payment</button>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-logo">
                    <img src="/img/logo.png" alt="DiscoBots Logo" height="30">
                    <span>DiscoBots</span>
                </div>
                <div class="footer-links">
                    <a href="/">Home</a>
                    <a href="/discord.html">Discord Server</a>
                    <a href="/terms.html">Terms & Privacy</a>
                </div>
                <div class="footer-social">
                    <a href="https://discord.gg/XBY893MsgC" target="_blank">Join our Discord</a>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 DiscoBots.fr - All rights reserved</p>
                <p>Contact: discobots.com@gmail.com</p>
            </div>
        </div>
    </footer>

    <script src="/js/api.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const checkoutButton = document.getElementById('checkout-button');
            const voucherInput = document.getElementById('voucher');
            const voucherMessage = document.getElementById('voucher-message');
            
            checkoutButton.addEventListener('click', function() {
                const voucher = voucherInput.value.trim();
                createCheckoutSession(voucher ? voucher : null);
            });
            
            voucherInput.addEventListener('input', function() {
                const voucher = voucherInput.value.trim();
                if (voucher === 'Uflvb62d') {
                    voucherMessage.textContent = '30% discount will be applied!';
                    voucherMessage.style.color = 'green';
                } else if (voucher.length > 0) {
                    voucherMessage.textContent = 'Invalid voucher code';
                    voucherMessage.style.color = 'red';
                } else {
                    voucherMessage.textContent = '';
                }
            });
        });
    </script>
</body>
</html>
EOL

echo "Files have been copied to the frontend directory."