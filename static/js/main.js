// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize particles background
    if (document.getElementById('particles-js')) {
        initParticles('particles-js', {
            maxParticles: 100,
            particleRadius: 1.5,
            particleColor: '#000000',
            speed: 0.3,
            connectParticles: true,
            connectDistance: 140,
            connectLineWidth: 0.5,
            connectLineColor: '#000000'
        });
    }

    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuToggle && navLinks) {
        mobileMenuToggle.addEventListener('click', function() {
            navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
        });
    }

    // FAQ accordion functionality
    const faqItems = document.querySelectorAll('.faq-item');
    
    if (faqItems.length > 0) {
        faqItems.forEach(item => {
            const question = item.querySelector('.faq-question');
            
            question.addEventListener('click', () => {
                // Toggle active class on the clicked item
                item.classList.toggle('active');
                
                // Close other open FAQ items
                faqItems.forEach(otherItem => {
                    if (otherItem !== item && otherItem.classList.contains('active')) {
                        otherItem.classList.remove('active');
                    }
                });
            });
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add hover effect to constellation for mouse position
    const particlesContainer = document.getElementById('particles-js');
    
    if (particlesContainer) {
        particlesContainer.addEventListener('mousemove', function(e) {
            // Create a custom event that the particles.js can listen to
            const event = new CustomEvent('particle-hover', {
                detail: {
                    x: e.clientX,
                    y: e.clientY
                }
            });
            
            particlesContainer.dispatchEvent(event);
        });
    }

    // Add animation to elements when they come into view
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.feature-card, .pricing-card, .hero-content, .showcase-content, .step');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 100) {
                element.classList.add('animate-in');
            }
        });
    };

    // Run once on page load
    animateOnScroll();
    
    // Run on scroll
    window.addEventListener('scroll', animateOnScroll);
});

// Add animation class to CSS
document.head.insertAdjacentHTML('beforeend', `
<style>
.animate-in {
    animation: fadeInUp 0.6s ease forwards;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.feature-card, .pricing-card, .hero-content, .showcase-content, .step {
    opacity: 0;
}
</style>
`);
