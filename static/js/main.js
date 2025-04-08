document.addEventListener('DOMContentLoaded', function() {
    // Initialize the particle background
    const theme = document.body.classList.contains('dark') ? 'dark' : 'light';
    
    // Configure particles based on the theme
    const particleOptions = {
        maxParticles: 100,
        particleRadius: 1.2,
        particleColor: theme === 'dark' ? '#ffffff' : '#000000',
        speed: 0.3,
        connectParticles: false, // We'll only connect particles on hover
        connectDistance: 120,
        connectLineWidth: 0.5,
        connectLineColor: theme === 'dark' ? '#ffffff' : '#000000'
    };
    
    // Initialize particles with the canvas element
    const canvas = document.getElementById('particles-js');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        // Create particles array
        const particles = [];
        const particleCount = particleOptions.maxParticles;
        
        // Create particles
        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                radius: particleOptions.particleRadius,
                color: particleOptions.particleColor,
                velocity: {
                    x: (Math.random() - 0.5) * particleOptions.speed,
                    y: (Math.random() - 0.5) * particleOptions.speed
                }
            });
        }
        
        // Mouse position for hover effect
        let mouse = {
            x: null,
            y: null,
            radius: 150 // Radius around mouse to connect particles
        };
        
        // Update mouse position on mousemove
        window.addEventListener('mousemove', function(event) {
            mouse.x = event.x;
            mouse.y = event.y;
        });
        
        // Reset mouse position when mouse leaves the window
        window.addEventListener('mouseout', function() {
            mouse.x = null;
            mouse.y = null;
        });
        
        // Resize canvas when window is resized
        window.addEventListener('resize', function() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
        
        // Animation function
        function animate() {
            requestAnimationFrame(animate);
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Update and draw particles
            for (let i = 0; i < particles.length; i++) {
                let p = particles[i];
                
                // Update position
                p.x += p.velocity.x;
                p.y += p.velocity.y;
                
                // Bounce off edges
                if (p.x + p.radius > canvas.width || p.x - p.radius < 0) {
                    p.velocity.x = -p.velocity.x;
                }
                
                if (p.y + p.radius > canvas.height || p.y - p.radius < 0) {
                    p.velocity.y = -p.velocity.y;
                }
                
                // Draw the particle
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.fill();
                
                // Connect particles near mouse
                if (mouse.x !== null && mouse.y !== null) {
                    // Check if particle is near mouse
                    const dx = mouse.x - p.x;
                    const dy = mouse.y - p.y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    
                    if (distance < mouse.radius) {
                        // Connect to nearby particles
                        for (let j = i + 1; j < particles.length; j++) {
                            const p2 = particles[j];
                            const dx2 = p2.x - p.x;
                            const dy2 = p2.y - p.y;
                            const distance2 = Math.sqrt(dx2 * dx2 + dy2 * dy2);
                            
                            if (distance2 < particleOptions.connectDistance) {
                                // Draw line with opacity based on distance
                                const opacity = 1 - (distance2 / particleOptions.connectDistance);
                                ctx.beginPath();
                                ctx.moveTo(p.x, p.y);
                                ctx.lineTo(p2.x, p2.y);
                                ctx.strokeStyle = particleOptions.connectLineColor.replace(')', ', ' + opacity + ')').replace('rgb', 'rgba');
                                ctx.lineWidth = particleOptions.connectLineWidth;
                                ctx.stroke();
                            }
                        }
                    }
                }
            }
        }
        
        // Start animation
        animate();
    }
});