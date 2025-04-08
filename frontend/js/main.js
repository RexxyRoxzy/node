// Initialize Particles.js
document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('particles-js');
    
    // Only create particles in canvases that exist
    if (canvas) {
        const particleOptions = {
            particleColor: document.body.classList.contains('dark') ? '#ffffff' : '#000000',
            particleRadius: 2,
            speed: 0.5,
            connectParticles: false,
            maxParticles: 100
        };
        
        canvas.particlesInstance = new ParticlesJS(canvas, particleOptions);
        
        // Enable particle connections on mouse hover
        canvas.addEventListener('mousemove', function() {
            canvas.particlesInstance.connectParticles = true;
        });
        
        // Disable particle connections when mouse stops
        let timeout;
        canvas.addEventListener('mousemove', function() {
            clearTimeout(timeout);
            timeout = setTimeout(function() {
                canvas.particlesInstance.connectParticles = false;
            }, 3000);
        });
    }
    
    // Theme toggle
    const themeButtons = document.querySelectorAll('.theme-btn');
    themeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const theme = this.getAttribute('data-theme');
            setTheme(theme);
        });
    });
    
    // Language toggle
    const langButtons = document.querySelectorAll('.lang-btn');
    langButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const lang = this.getAttribute('data-lang');
            setLanguage(lang);
        });
    });
    
    // FAQ Accordion (if present)
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        if (question) {
            question.addEventListener('click', () => {
                const isActive = item.classList.contains('active');
                
                // Close all FAQs
                faqItems.forEach(faq => {
                    faq.classList.remove('active');
                });
                
                // If the clicked one wasn't active, make it active
                if (!isActive) {
                    item.classList.add('active');
                }
            });
        }
    });
    
    // Countdown Timer (if present)
    const countdownEl = document.getElementById('countdown');
    
    if (countdownEl) {
        // Start with 48 hours (48 * 60 * 60 * 1000 ms)
        let timeLeft = 48 * 60 * 60;
        
        // Get saved countdown from localStorage if it exists
        const savedTime = localStorage.getItem('specialOfferCountdown');
        const startTime = localStorage.getItem('countdownStartTime');
        
        if (savedTime && startTime) {
            // Calculate elapsed time since the countdown started
            const elapsedSeconds = Math.floor((Date.now() - parseInt(startTime)) / 1000);
            timeLeft = parseInt(savedTime) - elapsedSeconds;
            
            // Reset if the countdown is finished or negative
            if (timeLeft <= 0) {
                timeLeft = 48 * 60 * 60;
                localStorage.setItem('countdownStartTime', Date.now().toString());
            }
        } else {
            // Initialize countdown if not saved
            localStorage.setItem('specialOfferCountdown', timeLeft.toString());
            localStorage.setItem('countdownStartTime', Date.now().toString());
        }
        
        // Update countdown every second
        function updateCountdown() {
            const hours = Math.floor(timeLeft / 3600);
            const minutes = Math.floor((timeLeft % 3600) / 60);
            const seconds = timeLeft % 60;
            
            countdownEl.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            
            if (timeLeft <= 0) {
                timeLeft = 48 * 60 * 60;
                localStorage.setItem('countdownStartTime', Date.now().toString());
            } else {
                timeLeft--;
                localStorage.setItem('specialOfferCountdown', timeLeft.toString());
            }
        }
        
        // Initialize and start countdown
        updateCountdown();
        setInterval(updateCountdown, 1000);
    }
    
    // Initialize auth state
    updateAuthUI();
    
    // Logout functionality
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }
    
    // Buy button
    const buyButton = document.getElementById('buy-button');
    if (buyButton) {
        buyButton.addEventListener('click', function(e) {
            e.preventDefault();
            createCheckoutSession();
        });
    }
    
    // Discount link
    const discountLink = document.getElementById('discount-link');
    if (discountLink) {
        discountLink.addEventListener('click', function(e) {
            e.preventDefault();
            createCheckoutSession('Uflvb62d');
        });
    }
    
    // Set initial theme and language from localStorage
    initThemeAndLanguage();
});

// Helper Functions
function setTheme(theme) {
    document.body.className = theme;
    localStorage.setItem('theme', theme);
    
    // Update active state on buttons
    document.querySelectorAll('.theme-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`.theme-btn[data-theme="${theme}"]`).classList.add('active');
    
    // Update particle color
    const canvas = document.getElementById('particles-js');
    if (canvas && canvas.particlesInstance) {
        const particleColor = theme === 'dark' ? '#ffffff' : '#000000';
        canvas.particlesInstance.particlesArray.forEach(particle => {
            particle.color = particleColor;
        });
    }
    
    // If user is logged in, save preference to server
    if (isLoggedIn()) {
        updateUserSettings({ theme: theme });
    }
}

function setLanguage(lang) {
    localStorage.setItem('language', lang);
    
    // Update active state on buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`.lang-btn[data-lang="${lang}"]`).classList.add('active');
    
    // Update UI text based on language
    updateUILanguage(lang);
    
    // If user is logged in, save preference to server
    if (isLoggedIn()) {
        updateUserSettings({ language: lang });
    }
}

function updateUILanguage(lang) {
    const translations = {
        'welcome-text': {
            'en': 'Welcome to DiscoBots.fr',
            'fr': 'Bienvenue sur DiscoBots.fr'
        },
        'intro-text': {
            'en': 'Discover a powerful and easy-to-use Discord bot that will enhance your server with amazing features.',
            'fr': 'Découvrez un bot Discord puissant et facile à utiliser qui améliorera votre serveur avec des fonctionnalités étonnantes.'
        },
        'add-discord-text': {
            'en': 'Add to Discord',
            'fr': 'Ajouter à Discord'
        },
        'features-title': {
            'en': 'Features',
            'fr': 'Fonctionnalités'
        },
        'moderation-title': {
            'en': 'Moderation',
            'fr': 'Modération'
        },
        'moderation-text': {
            'en': 'Keep your server clean and secure with advanced moderation tools.',
            'fr': 'Gardez votre serveur propre et sécurisé avec des outils de modération avancés.'
        },
        'music-title': {
            'en': 'Music',
            'fr': 'Musique'
        },
        'music-text': {
            'en': 'Play high-quality music from various platforms.',
            'fr': 'Jouez de la musique de haute qualité depuis diverses plateformes.'
        },
        'customization-title': {
            'en': 'Customization',
            'fr': 'Personnalisation'
        },
        'customization-text': {
            'en': 'Tailor the bot to your server with extensive customization options.',
            'fr': 'Adaptez le bot à votre serveur avec des options de personnalisation étendues.'
        },
        'economy-title': {
            'en': 'Economy',
            'fr': 'Économie'
        },
        'economy-text': {
            'en': 'Create an engaging economy system for your community.',
            'fr': 'Créez un système économique engageant pour votre communauté.'
        },
        'pricing-title': {
            'en': 'Pricing',
            'fr': 'Tarification'
        },
        'promo-text': {
            'en': '🔥 Special Offer: Use code <span class="coupon-code">DISCO30</span> for 30% off! 🔥',
            'fr': '🔥 Offre Spéciale: Utilisez le code <span class="coupon-code">DISCO30</span> pour obtenir 30% de réduction! 🔥'
        },
        'standard-title': {
            'en': 'Standard',
            'fr': 'Standard'
        },
        'features-access': {
            'en': 'Full access to all features',
            'fr': 'Accès complet aux fonctionnalités'
        },
        'priority-support': {
            'en': 'Priority support',
            'fr': 'Support prioritaire'
        },
        'servers-limit': {
            'en': 'Up to 10 servers',
            'fr': 'Jusqu\'à 10 serveurs'
        },
        'buy-button': {
            'en': 'Buy Now',
            'fr': 'Acheter maintenant'
        },
        'discount-link': {
            'en': 'Use discount code',
            'fr': 'Utiliser le code promotion'
        },
        'custom-title': {
            'en': 'Custom',
            'fr': 'Personnalisé'
        },
        'contact-us-text': {
            'en': 'Contact Us',
            'fr': 'Contactez-nous'
        },
        'custom-features': {
            'en': 'Custom features',
            'fr': 'Fonctionnalités personnalisées'
        },
        'dedicated-support': {
            'en': '24/7 Dedicated support',
            'fr': 'Support dédié 24/7'
        },
        'unlimited-servers': {
            'en': 'Unlimited servers',
            'fr': 'Serveurs illimités'
        },
        'contact-button': {
            'en': 'Contact Us',
            'fr': 'Contactez-nous'
        },
        'footer-home': {
            'en': 'Home',
            'fr': 'Accueil'
        },
        'footer-terms': {
            'en': 'Terms',
            'fr': 'Conditions'
        },
        'footer-pricing': {
            'en': 'Pricing',
            'fr': 'Tarification'
        },
        'footer-faq': {
            'en': 'FAQ',
            'fr': 'FAQ'
        },
        'footer-contact-us': {
            'en': 'Contact Us',
            'fr': 'Contactez-nous'
        },
        'copyright-text': {
            'en': '&copy; 2024 DiscoBots.fr. All rights reserved.',
            'fr': '&copy; 2024 DiscoBots.fr. Tous droits réservés.'
        }
    };
    
    // Update text for all elements with translations
    for (const [id, text] of Object.entries(translations)) {
        const element = document.getElementById(id);
        if (element && text[lang]) {
            element.innerHTML = text[lang];
        }
    }
}

function initThemeAndLanguage() {
    // Set theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    
    // Set language
    const savedLanguage = localStorage.getItem('language') || 'en';
    setLanguage(savedLanguage);
}

function showFlashMessage(message, type = 'info') {
    const flashContainer = document.getElementById('flash-messages');
    if (flashContainer) {
        const messageElement = document.createElement('div');
        messageElement.className = `flash-message ${type}`;
        messageElement.textContent = message;
        flashContainer.appendChild(messageElement);
        
        // Remove message after 5 seconds
        setTimeout(() => {
            messageElement.remove();
        }, 5000);
    }
}

function updateAuthUI() {
    const isAuthenticated = isLoggedIn();
    
    // Update navigation links
    document.getElementById('login-link').style.display = isAuthenticated ? 'none' : 'inline-block';
    document.getElementById('register-link').style.display = isAuthenticated ? 'none' : 'inline-block';
    document.getElementById('settings-link').style.display = isAuthenticated ? 'inline-block' : 'none';
    document.getElementById('logout-link').style.display = isAuthenticated ? 'inline-block' : 'none';
    
    // Update user greeting
    const userGreeting = document.getElementById('user-greeting');
    if (userGreeting) {
        if (isAuthenticated) {
            const user = JSON.parse(localStorage.getItem('user'));
            document.getElementById('username').textContent = user.username;
            userGreeting.style.display = 'block';
        } else {
            userGreeting.style.display = 'none';
        }
    }
}

// Helper to check login state
function isLoggedIn() {
    return !!localStorage.getItem('token');
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    updateAuthUI();
    showFlashMessage('You have been logged out successfully.');
}