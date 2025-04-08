// Main JavaScript file for DiscoBots.fr

// Global variables
const LANGUAGES = {
    en: {
        // Navigation
        'footer-home': 'Home',
        'footer-terms': 'Terms',
        'footer-pricing': 'Pricing',
        'footer-faq': 'FAQ',
        'footer-contact-us': 'Contact Us',
        'copyright-text': '© 2024 DiscoBots.fr. All rights reserved.',
        
        // Homepage
        'hero-title': 'Enhance Your Discord Server',
        'hero-description': 'DiscoBots.fr provides powerful, customizable Discord bots to improve moderation, engagement, and fun on your server.',
        'get-started-button': 'Get Started',
        'learn-more-button': 'Learn More',
        'special-offer-badge': 'Limited Offer!',
        'special-offer-title': '30% Off First Month',
        'special-offer-description': 'Use voucher code <strong>Uflvb62d</strong> during checkout to claim your discount!',
        'offer-ends-text': 'Offer ends in:',
        'hours-label': 'hours',
        'minutes-label': 'minutes',
        'seconds-label': 'seconds',
        'features-title': 'Key Features',
        'moderation-title': 'Moderation',
        'moderation-description': 'Powerful moderation tools to keep your server safe and clean.',
        'music-title': 'Music',
        'music-description': 'High-quality music playback from various sources.',
        'welcome-title': 'Welcome',
        'welcome-description': 'Customize welcome messages and auto-roles for new members.',
        'games-title': 'Games',
        'games-description': 'Fun games to boost engagement in your community.',
        'stats-title': 'Statistics',
        'stats-description': 'Track server activity and member engagement.',
        'customization-title': 'Customization',
        'customization-description': 'Tailor the bot to fit your server\'s unique needs.',
        'pricing-title': 'Pricing Plans',
        'standard-plan-title': 'Standard Plan',
        'price-amount': '$5.99',
        'price-period': '/ month',
        'standard-feature-1': '✅ Moderation commands',
        'standard-feature-2': '✅ Custom welcome messages',
        'standard-feature-3': '✅ Auto-roles',
        'standard-feature-4': '✅ Music commands',
        'standard-feature-5': '✅ 24/7 Support',
        'standard-cta-button': 'Subscribe Now',
        'custom-plan-title': 'Custom Plan',
        'custom-price': 'Contact Us',
        'custom-feature-1': '✅ All Standard features',
        'custom-feature-2': '✅ Custom commands',
        'custom-feature-3': '✅ Advanced automations',
        'custom-feature-4': '✅ Custom development',
        'custom-feature-5': '✅ Priority support',
        'custom-cta-button': 'Contact Us',
        'how-to-title': 'How to Use',
        'step1-title': 'Subscribe',
        'step1-description': 'Choose a plan and complete the payment process.',
        'step2-title': 'Invite Bot',
        'step2-description': 'Add the bot to your Discord server with one click.',
        'step3-title': 'Configure',
        'step3-description': 'Customize settings to match your server\'s needs.',
        'step4-title': 'Enjoy',
        'step4-description': 'Start using the commands and features!',
        'faq-title': 'Frequently Asked Questions',
        'faq1-question': 'What is DiscoBots.fr?',
        'faq1-answer': 'DiscoBots.fr provides customizable Discord bots that help server owners moderate their communities, enhance user engagement, and add fun features to their servers.',
        'faq2-question': 'How do I add the bot to my server?',
        'faq2-answer': 'After subscribing, you\'ll receive an invite link. Click on it, select your server, and authorize the bot with the required permissions.',
        'faq3-question': 'Can I cancel my subscription?',
        'faq3-answer': 'Yes, you can cancel your subscription at any time from your account settings. Your subscription will remain active until the end of the current billing period.',
        'faq4-question': 'Do you offer discounts?',
        'faq4-answer': 'Yes, we periodically offer special discounts. Currently, we have a 30% discount for the first month with the voucher code Uflvb62d.',
        'faq5-question': 'How can I get support?',
        'faq5-answer': 'You can join our Discord server for immediate support, or contact us via email at discobots.com@gmail.com.',
        'cta-title': 'Ready to enhance your Discord server?',
        'cta-description': 'Join thousands of server owners who trust DiscoBots.fr',
        'cta-pricing-button': 'View Pricing',
        'cta-discord-button': 'Join Discord',
        
        // Auth pages
        'login-title': 'Login',
        'register-title': 'Register',
        'username-label': 'Username',
        'email-label': 'Email',
        'password-label': 'Password',
        'password2-label': 'Repeat Password',
        'remember-me-label': 'Remember Me',
        'login-button': 'Sign In',
        'register-button': 'Create Account',
        'no-account-text': 'No account yet?',
        'register-link-text': 'Register',
        'already-account-text': 'Already registered?',
        'login-link-text': 'Login',
        
        // Settings page
        'settings-title': 'Settings',
        'theme-label': 'Theme',
        'theme-light': 'White',
        'theme-dark': 'Black',
        'language-label': 'Language',
        'language-en': 'English',
        'language-fr': 'Français',
        'save-settings-button': 'Save Settings',
        'subscription-title': 'Subscription',
        'subscription-status-text': 'You don\'t have an active subscription.',
        'subscribe-button': 'Subscribe Now',
        
        // Discord page
        'discord-title': 'Discord Server',
        'discord-description': 'Join our Discord server to get support, chat with our community, and stay updated on the latest DiscoBots features and news.',
        'join-discord-button': 'Join Discord Server',
        'discord-features-title': 'Server Features',
        'support-channel-title': '24/7 Support Channels',
        'support-channel-desc': 'Get help from our team and community members at any time.',
        'bot-commands-title': 'Bot Commands Testing',
        'bot-commands-desc': 'Test our bot commands and see all features in action.',
        'events-title': 'Events & Giveaways',
        'events-desc': 'Participate in regular events and win awesome prizes.',
        'community-title': 'Growing Community',
        'community-desc': 'Connect with like-minded Discord users and bot enthusiasts.',
        
        // Terms page
        'terms-title': 'Terms of Service & Privacy Policy',
        'terms-subtitle': 'Terms of Service',
        'terms-effective-date': 'Effective Date: April 1, 2024',
        'terms-acceptance': '1. Acceptance of Terms',
        'terms-acceptance-text': 'By accessing or using DiscoBots.fr services, you agree to be bound by these Terms of Service. If you do not agree to these terms, please do not use our services.',
        'terms-services': '2. Description of Services',
        'terms-services-text': 'DiscoBots.fr provides Discord bot services that enhance your Discord server experience. Our services include but are not limited to moderation tools, entertainment features, and server management utilities.',
        'terms-account': '3. User Accounts',
        'terms-account-text': 'To access certain features of our service, you must create an account. You are responsible for maintaining the confidentiality of your account information and for all activities that occur under your account.',
        'terms-payment': '4. Payment Terms',
        'terms-payment-text': 'Some features of our service require payment. By purchasing these features, you agree to pay the fees indicated. All payments are processed through secure third-party payment processors. Refunds are issued at our discretion.',
        'terms-conduct': '5. User Conduct',
        'terms-conduct-text': 'You agree not to use our services for any unlawful purpose or in violation of Discord\'s Terms of Service. We reserve the right to terminate accounts that violate these terms.',
        'terms-modifications': '6. Modifications to Service',
        'terms-modifications-text': 'We reserve the right to modify or discontinue our services at any time without notice. We will not be liable if all or any part of the service is unavailable.',
        'terms-termination': '7. Termination',
        'terms-termination-text': 'We may terminate your access to our services for violations of these terms. You may terminate your account at any time.',
        'privacy-subtitle': 'Privacy Policy',
        'privacy-collection': '1. Information Collection',
        'privacy-collection-text': 'We collect information that you provide directly to us, such as when you create an account, purchase services, or contact us for support. This information may include your name, email address, Discord user ID, and payment information.',
        'privacy-usage': '2. Information Usage',
        'privacy-usage-text': 'We use the information we collect to provide, maintain, and improve our services, to process transactions, to communicate with you, and to protect our users and service.',
        'privacy-sharing': '3. Information Sharing',
        'privacy-sharing-text': 'We do not sell or rent your personal information to third parties. We may share information with third-party service providers that perform services on our behalf, such as payment processing and data analysis.',
        'privacy-security': '4. Data Security',
        'privacy-security-text': 'We take reasonable measures to protect your personal information from unauthorized access, use, or disclosure. However, no method of transmission over the Internet is 100% secure.',
        'privacy-rights': '5. Your Rights',
        'privacy-rights-text': 'You have the right to access, correct, or delete your personal information. You may also object to or restrict certain processing of your information. To exercise these rights, please contact us at discobots.com@gmail.com.',
        'privacy-changes': '6. Changes to this Policy',
        'privacy-changes-text': 'We may update this Privacy Policy from time to time. We will notify you of any changes by posting the new policy on this page.',
        'privacy-contact': '7. Contact Us',
        'privacy-contact-text': 'If you have any questions about our Terms of Service or Privacy Policy, please contact us at discobots.com@gmail.com.',
        
        // Checkout page
        'checkout-title': 'Checkout',
        'plan-summary-title': 'Standard Plan',
        'plan-price-text': '$5.99 / month',
        'plan-feature-1': '✅ Moderation commands',
        'plan-feature-2': '✅ Custom welcome messages',
        'plan-feature-3': '✅ Auto-roles',
        'plan-feature-4': '✅ Music commands',
        'plan-feature-5': '✅ 24/7 Support',
        'voucher-title': 'Have a voucher?',
        'subtotal-label': 'Subtotal:',
        'discount-label': 'Discount:',
        'total-label': 'Total:',
        'checkout-button': 'Proceed to Payment',
        
        // Success/Cancel pages
        'success-title': 'Payment Successful!',
        'success-message': 'Thank you for your purchase. Your subscription to DiscoBots.fr is now active.',
        'next-steps-title': 'Next Steps',
        'next-step-1': 'Join our Discord server for support',
        'next-step-2': 'Invite the bot to your server using the link below',
        'next-step-3': 'Set up your bot with the customization options',
        'invite-bot-button': 'Invite Bot to Server',
        'back-home-button': 'Back to Home',
        'cancel-title': 'Payment Cancelled',
        'cancel-message': 'Your payment was cancelled. No charges were made to your account.',
        'try-again-title': 'Would you like to try again?',
        'try-again-button': 'Try Again',
        'help-message': 'If you\'re having trouble with the payment process or have any questions, please join our Discord server for assistance or contact us at discobots.com@gmail.com.'
    },
    fr: {
        // Navigation
        'footer-home': 'Accueil',
        'footer-terms': 'Conditions',
        'footer-pricing': 'Tarifs',
        'footer-faq': 'FAQ',
        'footer-contact-us': 'Contactez-nous',
        'copyright-text': '© 2024 DiscoBots.fr. Tous droits réservés.',
        
        // Homepage
        'hero-title': 'Améliorez Votre Serveur Discord',
        'hero-description': 'DiscoBots.fr fournit des bots Discord puissants et personnalisables pour améliorer la modération, l\'engagement et le plaisir sur votre serveur.',
        'get-started-button': 'Commencer',
        'learn-more-button': 'En savoir plus',
        'special-offer-badge': 'Offre Limitée!',
        'special-offer-title': '30% de Réduction le Premier Mois',
        'special-offer-description': 'Utilisez le code <strong>Uflvb62d</strong> lors du paiement pour réclamer votre réduction!',
        'offer-ends-text': 'L\'offre se termine dans:',
        'hours-label': 'heures',
        'minutes-label': 'minutes',
        'seconds-label': 'secondes',
        'features-title': 'Fonctionnalités Clés',
        'moderation-title': 'Modération',
        'moderation-description': 'Outils de modération puissants pour garder votre serveur sûr et propre.',
        'music-title': 'Musique',
        'music-description': 'Lecture de musique de haute qualité à partir de diverses sources.',
        'welcome-title': 'Bienvenue',
        'welcome-description': 'Personnalisez les messages de bienvenue et les rôles automatiques pour les nouveaux membres.',
        'games-title': 'Jeux',
        'games-description': 'Jeux amusants pour augmenter l\'engagement dans votre communauté.',
        'stats-title': 'Statistiques',
        'stats-description': 'Suivez l\'activité du serveur et l\'engagement des membres.',
        'customization-title': 'Personnalisation',
        'customization-description': 'Adaptez le bot aux besoins uniques de votre serveur.',
        'pricing-title': 'Plans Tarifaires',
        'standard-plan-title': 'Plan Standard',
        'price-amount': '5,99€',
        'price-period': '/ mois',
        'standard-feature-1': '✅ Commandes de modération',
        'standard-feature-2': '✅ Messages de bienvenue personnalisés',
        'standard-feature-3': '✅ Rôles automatiques',
        'standard-feature-4': '✅ Commandes musicales',
        'standard-feature-5': '✅ Support 24/7',
        'standard-cta-button': 'S\'abonner maintenant',
        'custom-plan-title': 'Plan Personnalisé',
        'custom-price': 'Contactez-nous',
        'custom-feature-1': '✅ Toutes les fonctionnalités Standard',
        'custom-feature-2': '✅ Commandes personnalisées',
        'custom-feature-3': '✅ Automatisations avancées',
        'custom-feature-4': '✅ Développement personnalisé',
        'custom-feature-5': '✅ Support prioritaire',
        'custom-cta-button': 'Contactez-nous',
        'how-to-title': 'Comment Utiliser',
        'step1-title': 'S\'abonner',
        'step1-description': 'Choisissez un plan et complétez le processus de paiement.',
        'step2-title': 'Inviter le Bot',
        'step2-description': 'Ajoutez le bot à votre serveur Discord en un clic.',
        'step3-title': 'Configurer',
        'step3-description': 'Personnalisez les paramètres selon les besoins de votre serveur.',
        'step4-title': 'Profiter',
        'step4-description': 'Commencez à utiliser les commandes et les fonctionnalités!',
        'faq-title': 'Questions Fréquemment Posées',
        'faq1-question': 'Qu\'est-ce que DiscoBots.fr?',
        'faq1-answer': 'DiscoBots.fr fournit des bots Discord personnalisables qui aident les propriétaires de serveurs à modérer leurs communautés, à améliorer l\'engagement des utilisateurs et à ajouter des fonctionnalités amusantes à leurs serveurs.',
        'faq2-question': 'Comment ajouter le bot à mon serveur?',
        'faq2-answer': 'Après vous être abonné, vous recevrez un lien d\'invitation. Cliquez dessus, sélectionnez votre serveur et autorisez le bot avec les permissions requises.',
        'faq3-question': 'Puis-je annuler mon abonnement?',
        'faq3-answer': 'Oui, vous pouvez annuler votre abonnement à tout moment dans les paramètres de votre compte. Votre abonnement restera actif jusqu\'à la fin de la période de facturation en cours.',
        'faq4-question': 'Offrez-vous des réductions?',
        'faq4-answer': 'Oui, nous proposons périodiquement des réductions spéciales. Actuellement, nous avons une réduction de 30% pour le premier mois avec le code Uflvb62d.',
        'faq5-question': 'Comment obtenir de l\'aide?',
        'faq5-answer': 'Vous pouvez rejoindre notre serveur Discord pour une assistance immédiate ou nous contacter par email à discobots.com@gmail.com.',
        'cta-title': 'Prêt à améliorer votre serveur Discord?',
        'cta-description': 'Rejoignez des milliers de propriétaires de serveurs qui font confiance à DiscoBots.fr',
        'cta-pricing-button': 'Voir les tarifs',
        'cta-discord-button': 'Rejoindre Discord',
        
        // Auth pages
        'login-title': 'Connexion',
        'register-title': 'Inscription',
        'username-label': 'Nom d\'utilisateur',
        'email-label': 'Email',
        'password-label': 'Mot de passe',
        'password2-label': 'Répéter le mot de passe',
        'remember-me-label': 'Se souvenir de moi',
        'login-button': 'Se connecter',
        'register-button': 'Créer un compte',
        'no-account-text': 'Pas encore de compte?',
        'register-link-text': 'S\'inscrire',
        'already-account-text': 'Déjà inscrit?',
        'login-link-text': 'Connexion',
        
        // Settings page
        'settings-title': 'Paramètres',
        'theme-label': 'Thème',
        'theme-light': 'Blanc',
        'theme-dark': 'Noir',
        'language-label': 'Langue',
        'language-en': 'English',
        'language-fr': 'Français',
        'save-settings-button': 'Enregistrer les paramètres',
        'subscription-title': 'Abonnement',
        'subscription-status-text': 'Vous n\'avez pas d\'abonnement actif.',
        'subscribe-button': 'S\'abonner maintenant',
        
        // Discord page
        'discord-title': 'Serveur Discord',
        'discord-description': 'Rejoignez notre serveur Discord pour obtenir de l\'aide, discuter avec notre communauté et rester informé des dernières fonctionnalités et actualités de DiscoBots.',
        'join-discord-button': 'Rejoindre le serveur Discord',
        'discord-features-title': 'Fonctionnalités du serveur',
        'support-channel-title': 'Canaux de support 24/7',
        'support-channel-desc': 'Obtenez de l\'aide de notre équipe et des membres de la communauté à tout moment.',
        'bot-commands-title': 'Test des commandes du bot',
        'bot-commands-desc': 'Testez nos commandes de bot et voyez toutes les fonctionnalités en action.',
        'events-title': 'Événements et cadeaux',
        'events-desc': 'Participez à des événements réguliers et gagnez des prix fantastiques.',
        'community-title': 'Communauté grandissante',
        'community-desc': 'Connectez-vous avec des utilisateurs Discord partageant les mêmes intérêts et des passionnés de bots.',
        
        // Terms page
        'terms-title': 'Conditions d\'utilisation et politique de confidentialité',
        'terms-subtitle': 'Conditions d\'utilisation',
        'terms-effective-date': 'Date d\'effet: 1er avril 2024',
        'terms-acceptance': '1. Acceptation des conditions',
        'terms-acceptance-text': 'En accédant ou en utilisant les services de DiscoBots.fr, vous acceptez d\'être lié par ces conditions d\'utilisation. Si vous n\'acceptez pas ces conditions, veuillez ne pas utiliser nos services.',
        'terms-services': '2. Description des services',
        'terms-services-text': 'DiscoBots.fr fournit des services de bots Discord qui améliorent votre expérience sur le serveur Discord. Nos services comprennent, sans s\'y limiter, des outils de modération, des fonctionnalités de divertissement et des utilitaires de gestion de serveur.',
        'terms-account': '3. Comptes utilisateurs',
        'terms-account-text': 'Pour accéder à certaines fonctionnalités de notre service, vous devez créer un compte. Vous êtes responsable du maintien de la confidentialité des informations de votre compte et de toutes les activités qui se produisent sous votre compte.',
        'terms-payment': '4. Conditions de paiement',
        'terms-payment-text': 'Certaines fonctionnalités de notre service nécessitent un paiement. En achetant ces fonctionnalités, vous acceptez de payer les frais indiqués. Tous les paiements sont traités par des processeurs de paiement tiers sécurisés. Les remboursements sont émis à notre discrétion.',
        'terms-conduct': '5. Conduite de l\'utilisateur',
        'terms-conduct-text': 'Vous acceptez de ne pas utiliser nos services à des fins illégales ou en violation des conditions d\'utilisation de Discord. Nous nous réservons le droit de résilier les comptes qui violent ces conditions.',
        'terms-modifications': '6. Modifications du service',
        'terms-modifications-text': 'Nous nous réservons le droit de modifier ou d\'interrompre nos services à tout moment sans préavis. Nous ne serons pas responsables si tout ou partie du service est indisponible.',
        'terms-termination': '7. Résiliation',
        'terms-termination-text': 'Nous pouvons mettre fin à votre accès à nos services pour violations de ces conditions. Vous pouvez résilier votre compte à tout moment.',
        'privacy-subtitle': 'Politique de confidentialité',
        'privacy-collection': '1. Collecte d\'informations',
        'privacy-collection-text': 'Nous collectons les informations que vous nous fournissez directement, par exemple lorsque vous créez un compte, achetez des services ou nous contactez pour obtenir de l\'aide. Ces informations peuvent inclure votre nom, adresse e-mail, identifiant d\'utilisateur Discord et informations de paiement.',
        'privacy-usage': '2. Utilisation des informations',
        'privacy-usage-text': 'Nous utilisons les informations que nous collectons pour fournir, maintenir et améliorer nos services, pour traiter les transactions, pour communiquer avec vous et pour protéger nos utilisateurs et notre service.',
        'privacy-sharing': '3. Partage d\'informations',
        'privacy-sharing-text': 'Nous ne vendons ni ne louons vos informations personnelles à des tiers. Nous pouvons partager des informations avec des fournisseurs de services tiers qui exécutent des services en notre nom, tels que le traitement des paiements et l\'analyse des données.',
        'privacy-security': '4. Sécurité des données',
        'privacy-security-text': 'Nous prenons des mesures raisonnables pour protéger vos informations personnelles contre l\'accès, l\'utilisation ou la divulgation non autorisés. Cependant, aucune méthode de transmission sur Internet n\'est sécurisée à 100%.',
        'privacy-rights': '5. Vos droits',
        'privacy-rights-text': 'Vous avez le droit d\'accéder, de corriger ou de supprimer vos informations personnelles. Vous pouvez également vous opposer à certains traitements de vos informations ou les restreindre. Pour exercer ces droits, veuillez nous contacter à discobots.com@gmail.com.',
        'privacy-changes': '6. Modifications de cette politique',
        'privacy-changes-text': 'Nous pouvons mettre à jour cette politique de confidentialité de temps à autre. Nous vous informerons de tout changement en publiant la nouvelle politique sur cette page.',
        'privacy-contact': '7. Contactez-nous',
        'privacy-contact-text': 'Si vous avez des questions concernant nos conditions d\'utilisation ou notre politique de confidentialité, veuillez nous contacter à discobots.com@gmail.com.',
        
        // Checkout page
        'checkout-title': 'Paiement',
        'plan-summary-title': 'Plan Standard',
        'plan-price-text': '5,99€ / mois',
        'plan-feature-1': '✅ Commandes de modération',
        'plan-feature-2': '✅ Messages de bienvenue personnalisés',
        'plan-feature-3': '✅ Rôles automatiques',
        'plan-feature-4': '✅ Commandes musicales',
        'plan-feature-5': '✅ Support 24/7',
        'voucher-title': 'Vous avez un code promo?',
        'subtotal-label': 'Sous-total:',
        'discount-label': 'Réduction:',
        'total-label': 'Total:',
        'checkout-button': 'Procéder au paiement',
        
        // Success/Cancel pages
        'success-title': 'Paiement réussi!',
        'success-message': 'Merci pour votre achat. Votre abonnement à DiscoBots.fr est maintenant actif.',
        'next-steps-title': 'Prochaines étapes',
        'next-step-1': 'Rejoignez notre serveur Discord pour obtenir de l\'aide',
        'next-step-2': 'Invitez le bot sur votre serveur en utilisant le lien ci-dessous',
        'next-step-3': 'Configurez votre bot avec les options de personnalisation',
        'invite-bot-button': 'Inviter le bot sur le serveur',
        'back-home-button': 'Retour à l\'accueil',
        'cancel-title': 'Paiement annulé',
        'cancel-message': 'Votre paiement a été annulé. Aucun frais n\'a été prélevé sur votre compte.',
        'try-again-title': 'Voulez-vous réessayer?',
        'try-again-button': 'Réessayer',
        'help-message': 'Si vous rencontrez des difficultés avec le processus de paiement ou si vous avez des questions, veuillez rejoindre notre serveur Discord pour obtenir de l\'aide ou nous contacter à discobots.com@gmail.com.'
    }
};

// Initialize on document load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize particles background
    initParticles('particles-js', {
        particleColor: '#5865F2',
        particleRadius: 2,
        particleCount: 80,
        connectParticles: true,
        connectDistance: 120,
        speed: 0.5,
        responsive: true
    });
    
    // Initialize theme and language
    initThemeAndLanguage();
    
    // Set up countdown timer if it exists
    const countdownTimer = document.getElementById('countdown-timer');
    if (countdownTimer) {
        // Set countdown to 48 hours from now
        const deadline = new Date();
        deadline.setHours(deadline.getHours() + 48);
        
        function updateCountdown() {
            const now = new Date();
            const diff = deadline - now;
            
            if (diff <= 0) {
                // Countdown finished
                document.getElementById('countdown-hours').textContent = '00';
                document.getElementById('countdown-minutes').textContent = '00';
                document.getElementById('countdown-seconds').textContent = '00';
                return;
            }
            
            const hours = Math.floor(diff / (1000 * 60 * 60));
            const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((diff % (1000 * 60)) / 1000);
            
            document.getElementById('countdown-hours').textContent = hours.toString().padStart(2, '0');
            document.getElementById('countdown-minutes').textContent = minutes.toString().padStart(2, '0');
            document.getElementById('countdown-seconds').textContent = seconds.toString().padStart(2, '0');
            
            setTimeout(updateCountdown, 1000);
        }
        
        updateCountdown();
    }
    
    // FAQ accordion
    const faqQuestions = document.querySelectorAll('.faq-question');
    faqQuestions.forEach(question => {
        question.addEventListener('click', () => {
            const answer = question.nextElementSibling;
            const isOpen = answer.style.display === 'block';
            
            // Close all answers
            document.querySelectorAll('.faq-answer').forEach(a => {
                a.style.display = 'none';
            });
            
            // Toggle current answer
            if (!isOpen) {
                answer.style.display = 'block';
            }
        });
    });
    
    // Update auth UI
    updateAuthUI();
    
    // Handle logout
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', (e) => {
            e.preventDefault();
            logout();
        });
    }
    
    // Handle theme toggle
    const themeButtons = document.querySelectorAll('.theme-btn');
    themeButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            setTheme(btn.getAttribute('data-theme'));
            
            // Update active state
            themeButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });
    
    // Handle language toggle
    const langButtons = document.querySelectorAll('.lang-btn');
    langButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            setLanguage(btn.getAttribute('data-lang'));
            
            // Update active state
            langButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });
    
    // Handle register form submission
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const password2 = document.getElementById('password2').value;
            
            if (password !== password2) {
                showFlashMessage('Passwords do not match', 'error');
                return;
            }
            
            register(username, email, password)
                .then(response => {
                    if (response.success) {
                        showFlashMessage('Registration successful! Redirecting to login...', 'success');
                        setTimeout(() => {
                            window.location.href = 'login.html';
                        }, 2000);
                    } else {
                        showFlashMessage('Registration failed: ' + response.message, 'error');
                    }
                })
                .catch(err => {
                    showFlashMessage('An error occurred: ' + err.message, 'error');
                });
        });
    }
    
    // Handle login form submission
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const rememberMe = document.getElementById('remember-me')?.checked || false;
            
            login(username, password)
                .then(response => {
                    if (response.success) {
                        showFlashMessage('Login successful! Redirecting...', 'success');
                        setTimeout(() => {
                            window.location.href = 'index.html';
                        }, 1000);
                    } else {
                        showFlashMessage('Login failed: ' + response.message, 'error');
                    }
                })
                .catch(err => {
                    showFlashMessage('An error occurred: ' + err.message, 'error');
                });
        });
    }
});

// Theme handling
function setTheme(theme) {
    document.body.className = theme;
    localStorage.setItem('theme', theme);
    
    // Update theme buttons
    const themeButtons = document.querySelectorAll('.theme-btn');
    themeButtons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-theme') === theme) {
            btn.classList.add('active');
        }
    });
}

// Language handling
function setLanguage(lang) {
    localStorage.setItem('language', lang);
    updateUILanguage(lang);
    
    // Update language buttons
    const langButtons = document.querySelectorAll('.lang-btn');
    langButtons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-lang') === lang) {
            btn.classList.add('active');
        }
    });
}

function updateUILanguage(lang) {
    if (!LANGUAGES[lang]) return;
    
    // Update all translatable elements
    Object.keys(LANGUAGES[lang]).forEach(key => {
        const element = document.getElementById(key);
        if (element) {
            // Check if the content needs to be treated as HTML
            if (LANGUAGES[lang][key].includes('<') && LANGUAGES[lang][key].includes('>')) {
                element.innerHTML = LANGUAGES[lang][key];
            } else {
                element.textContent = LANGUAGES[lang][key];
            }
        }
    });
}

function initThemeAndLanguage() {
    // Set theme from local storage or default to light
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    
    // Set language from local storage or default to en
    const savedLanguage = localStorage.getItem('language') || 'en';
    setLanguage(savedLanguage);
}

// Flash messages
function showFlashMessage(message, type = 'info') {
    const flashMessages = document.getElementById('flash-messages');
    if (!flashMessages) return;
    
    const messageElement = document.createElement('div');
    messageElement.className = `flash-message ${type}`;
    messageElement.textContent = message;
    
    flashMessages.appendChild(messageElement);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        messageElement.remove();
    }, 5000);
}

// Auth UI handling
function updateAuthUI() {
    const isLoggedIn = localStorage.getItem('token') !== null;
    
    const loginLinks = document.querySelectorAll('.nav-login');
    const registerLinks = document.querySelectorAll('.nav-register');
    const settingsLinks = document.querySelectorAll('.nav-settings');
    const logoutLinks = document.querySelectorAll('.nav-logout');
    const userGreeting = document.getElementById('user-greeting');
    const usernameDisplay = document.getElementById('username-display');
    
    if (isLoggedIn) {
        // Hide login/register, show settings/logout
        loginLinks.forEach(link => link.classList.add('hidden'));
        registerLinks.forEach(link => link.classList.add('hidden'));
        settingsLinks.forEach(link => link.classList.remove('hidden'));
        logoutLinks.forEach(link => link.classList.remove('hidden'));
        
        // Show user greeting if it exists
        if (userGreeting) {
            userGreeting.classList.remove('hidden');
            
            // Get user info to display username
            if (usernameDisplay) {
                getUserInfo()
                    .then(user => {
                        usernameDisplay.textContent = user.username;
                    })
                    .catch(err => {
                        console.error('Failed to get user info:', err);
                    });
            }
        }
    } else {
        // Show login/register, hide settings/logout
        loginLinks.forEach(link => link.classList.remove('hidden'));
        registerLinks.forEach(link => link.classList.remove('hidden'));
        settingsLinks.forEach(link => link.classList.add('hidden'));
        logoutLinks.forEach(link => link.classList.add('hidden'));
        
        // Hide user greeting
        if (userGreeting) {
            userGreeting.classList.add('hidden');
        }
    }
}

// Check if user is logged in
function isLoggedIn() {
    return localStorage.getItem('token') !== null;
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    updateAuthUI();
    showFlashMessage('You have been logged out successfully', 'success');
    
    // If on a page that requires authentication, redirect to home
    const authRequiredPages = ['settings.html', 'checkout.html', 'checkout-success.html', 'checkout-cancel.html'];
    const currentPage = window.location.pathname.split('/').pop();
    
    if (authRequiredPages.includes(currentPage)) {
        window.location.href = 'index.html';
    }
}