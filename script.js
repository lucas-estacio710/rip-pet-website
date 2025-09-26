/**
 * =====================================================
 * PREMIUM RESPONSIVE LAYOUT - JAVASCRIPT MODULAR
 * =====================================================
 * 
 * Funcionalidades:
 * - Navegação responsiva com menu mobile
 * - Smooth scrolling com offset de header
 * - Intersection Observer para animações
 * - Form validation e UX enhancements
 * - Performance optimizations
 * - Accessibility features
 * 
 * =====================================================
 */

// ===== CONFIGURAÇÕES GLOBAIS =====
const CONFIG = {
    breakpoints: {
        sm: 640,
        md: 768,
        lg: 1024,
        xl: 1280,
        '2xl': 1536
    },
    animations: {
        duration: 300,
        easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
    },
    scroll: {
        headerOffset: 80,
        smoothDuration: 800
    }
};

// ===== UTILITÁRIOS =====
const utils = {
    // Debounce function para performance
    debounce(func, wait, immediate) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                timeout = null;
                if (!immediate) func.apply(this, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(this, args);
        };
    },

    // Throttle function para scroll events
    throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },

    // Get current viewport width
    getViewportWidth() {
        return Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
    },

    // Check if mobile
    isMobile() {
        return this.getViewportWidth() < CONFIG.breakpoints.md;
    },

    // Get element height
    getElementHeight(element) {
        return element ? element.getBoundingClientRect().height : 0;
    }
};

// ===== CLASSE PARA NAVEGAÇÃO RESPONSIVA =====
class ResponsiveNavigation {
    constructor() {
        this.header = document.querySelector('.header');
        this.menuToggle = document.getElementById('menu-toggle');
        this.navbarMenu = document.getElementById('navbar-menu');
        this.navLinks = document.querySelectorAll('.navbar-nav a');
        this.isMenuOpen = false;
        this.lastScrollY = window.scrollY;

        this.init();
    }

    init() {
        if (!this.header || !this.menuToggle || !this.navbarMenu) {
            console.warn('Elementos de navegação não encontrados');
            return;
        }

        this.bindEvents();
        this.setupSmoothScrolling();
        this.handleInitialScroll();
    }

    bindEvents() {
        // Mobile menu toggle
        this.menuToggle.addEventListener('click', () => this.toggleMobileMenu());

        // Close menu on link click
        this.navLinks.forEach(link => {
            link.addEventListener('click', () => this.closeMobileMenu());
        });

        // Close menu on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isMenuOpen) {
                this.closeMobileMenu();
            }
        });

        // Scroll effects
        window.addEventListener('scroll', utils.throttle(() => this.handleScroll(), 16));

        // Resize handler
        window.addEventListener('resize', utils.debounce(() => this.handleResize(), 150));

        // Close mobile menu on outside click
        document.addEventListener('click', (e) => {
            if (this.isMenuOpen && !this.header.contains(e.target)) {
                this.closeMobileMenu();
            }
        });
    }

    toggleMobileMenu() {
        this.isMenuOpen = !this.isMenuOpen;

        // Toggle classes
        this.menuToggle.classList.toggle('active', this.isMenuOpen);
        this.navbarMenu.classList.toggle('active', this.isMenuOpen);

        // Update ARIA attributes
        this.menuToggle.setAttribute('aria-expanded', this.isMenuOpen);

        // Prevent body scroll
        document.body.style.overflow = this.isMenuOpen ? 'hidden' : '';

        // Focus management
        if (this.isMenuOpen) {
            // Focus first menu item after animation
            setTimeout(() => {
                const firstLink = this.navbarMenu.querySelector('a');
                if (firstLink) firstLink.focus();
            }, CONFIG.animations.duration);
        } else {
            this.menuToggle.focus();
        }

        // Announce to screen readers
        this.announceMenuState();
    }

    closeMobileMenu() {
        if (!this.isMenuOpen) return;

        this.isMenuOpen = false;
        this.menuToggle.classList.remove('active');
        this.navbarMenu.classList.remove('active');
        this.menuToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
    }

    announceMenuState() {
        // Create or update screen reader announcement
        let announcement = document.getElementById('menu-announcement');
        if (!announcement) {
            announcement = document.createElement('div');
            announcement.id = 'menu-announcement';
            announcement.setAttribute('aria-live', 'polite');
            announcement.setAttribute('aria-atomic', 'true');
            announcement.style.position = 'absolute';
            announcement.style.left = '-10000px';
            announcement.style.width = '1px';
            announcement.style.height = '1px';
            announcement.style.overflow = 'hidden';
            document.body.appendChild(announcement);
        }

        announcement.textContent = this.isMenuOpen ? 'Menu aberto' : 'Menu fechado';
    }

    handleScroll() {
        const currentScrollY = window.scrollY;

        // Add/remove scrolled class
        this.header.classList.toggle('scrolled', currentScrollY > 50);

        // Hide/show header on scroll (optional)
        if (Math.abs(currentScrollY - this.lastScrollY) > 5) {
            if (currentScrollY > this.lastScrollY && currentScrollY > 100) {
                this.header.style.transform = 'translateY(-100%)';
            } else {
                this.header.style.transform = 'translateY(0)';
            }
            this.lastScrollY = currentScrollY;
        }
    }

    handleResize() {
        // Close mobile menu on resize to desktop
        if (!utils.isMobile() && this.isMenuOpen) {
            this.closeMobileMenu();
        }
    }

    handleInitialScroll() {
        // Handle initial scroll position (e.g., page refresh at scrolled position)
        if (window.scrollY > 50) {
            this.header.classList.add('scrolled');
        }
    }

    setupSmoothScrolling() {
        // Enhanced smooth scrolling with header offset
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();

                const targetId = anchor.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);

                if (targetElement) {
                    const headerHeight = utils.getElementHeight(this.header);
                    const targetPosition = targetElement.getBoundingClientRect().top + 
                                         window.pageYOffset - 
                                         headerHeight - 20;

                    // Close mobile menu if open
                    this.closeMobileMenu();

                    // Smooth scroll
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });

                    // Focus target for accessibility
                    setTimeout(() => {
                        targetElement.focus({ preventScroll: true });
                    }, CONFIG.scroll.smoothDuration);
                }
            });
        });
    }
}

// ===== CLASSE PARA ANIMAÇÕES E INTERSECTION OBSERVER =====
class AnimationController {
    constructor() {
        this.observerOptions = {
            threshold: [0.1, 0.25, 0.5],
            rootMargin: '0px 0px -50px 0px'
        };

        this.init();
    }

    init() {
        if ('IntersectionObserver' in window) {
            this.setupIntersectionObserver();
        } else {
            // Fallback for older browsers
            this.fallbackAnimations();
        }
    }

    setupIntersectionObserver() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateElement(entry.target, entry.intersectionRatio);
                    
                    // Unobserve after animation for performance
                    if (entry.intersectionRatio > 0.25) {
                        observer.unobserve(entry.target);
                    }
                }
            });
        }, this.observerOptions);

        // Observe animatable elements
        const animatableElements = document.querySelectorAll(
            '.card, .content-block, .portfolio-item, .service-card, .process-step'
        );

        animatableElements.forEach(el => {
            el.classList.add('animate-on-scroll');
            observer.observe(el);
        });
    }

    animateElement(element, ratio) {
        // Add animation class based on intersection ratio
        if (ratio > 0.1) {
            element.classList.add('animate-fade-in');
        }
        if (ratio > 0.25) {
            element.classList.add('animate-slide-up');
        }
        if (ratio > 0.5) {
            element.classList.add('animate-complete');
        }
    }

    fallbackAnimations() {
        // Simple fallback for browsers without IntersectionObserver
        const elements = document.querySelectorAll('.card, .content-block, .portfolio-item');
        elements.forEach((el, index) => {
            setTimeout(() => {
                el.classList.add('animate-fade-in');
            }, index * 100);
        });
    }
}

// ===== CLASSE PARA VALIDAÇÃO DE FORMULÁRIOS =====
class FormValidator {
    constructor() {
        this.forms = document.querySelectorAll('form[role="form"]');
        this.init();
    }

    init() {
        this.forms.forEach(form => this.setupFormValidation(form));
    }

    setupFormValidation(form) {
        const inputs = form.querySelectorAll('input, textarea, select');
        const submitButton = form.querySelector('button[type="submit"]');

        // Real-time validation
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', utils.debounce(() => {
                this.clearFieldError(input);
                if (input.value.trim()) this.validateField(input);
            }, 300));
        });

        // Form submission
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFormSubmit(form, submitButton);
        });
    }

    validateField(field) {
        const value = field.value.trim();
        const fieldName = field.getAttribute('name');
        let isValid = true;
        let errorMessage = '';

        // Clear previous errors
        this.clearFieldError(field);

        // Required field validation
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'Este campo é obrigatório.';
        }

        // Email validation
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                errorMessage = 'Por favor, insira um email válido.';
            }
        }

        // Phone validation (Brazilian format)
        if (field.type === 'tel' && value) {
            const phoneRegex = /^(?:\+55\s?)?(?:\(\d{2}\)\s?|\d{2}\s?)?\d{4,5}[-.\s]?\d{4}$/;
            if (!phoneRegex.test(value)) {
                isValid = false;
                errorMessage = 'Por favor, insira um telefone válido.';
            }
        }

        // Minimum length validation
        const minLength = field.getAttribute('minlength');
        if (minLength && value.length < parseInt(minLength)) {
            isValid = false;
            errorMessage = `Este campo deve ter pelo menos ${minLength} caracteres.`;
        }

        if (!isValid) {
            this.showFieldError(field, errorMessage);
        } else {
            this.showFieldSuccess(field);
        }

        return isValid;
    }

    showFieldError(field, message) {
        field.classList.add('error');
        field.setAttribute('aria-invalid', 'true');

        const errorElement = this.getOrCreateErrorElement(field);
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }

    showFieldSuccess(field) {
        field.classList.remove('error');
        field.classList.add('success');
        field.setAttribute('aria-invalid', 'false');

        const errorElement = this.getOrCreateErrorElement(field);
        errorElement.style.display = 'none';
    }

    clearFieldError(field) {
        field.classList.remove('error', 'success');
        field.removeAttribute('aria-invalid');

        const errorElement = this.getOrCreateErrorElement(field);
        errorElement.style.display = 'none';
    }

    getOrCreateErrorElement(field) {
        const fieldId = field.getAttribute('id');
        let errorElement = document.getElementById(`${fieldId}-error`);

        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.id = `${fieldId}-error`;
            errorElement.className = 'field-error';
            errorElement.setAttribute('role', 'alert');
            errorElement.setAttribute('aria-live', 'polite');

            // Insert after field
            field.parentNode.insertBefore(errorElement, field.nextSibling);
        }

        return errorElement;
    }

    async handleFormSubmit(form, submitButton) {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        // Validate all fields
        const inputs = form.querySelectorAll('input, textarea, select');
        let isFormValid = true;

        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isFormValid = false;
            }
        });

        if (!isFormValid) {
            // Focus first error field
            const firstError = form.querySelector('.error');
            if (firstError) {
                firstError.focus();
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
            return;
        }

        // Show loading state
        this.setSubmitLoading(submitButton, true);

        try {
            // Simulate API call
            await this.submitForm(data);
            
            // Success feedback
            this.showSuccessMessage(form);
            form.reset();

        } catch (error) {
            // Error feedback
            this.showErrorMessage(form, error.message);
        } finally {
            this.setSubmitLoading(submitButton, false);
        }
    }

    async submitForm(data) {
        // Simulate API call delay
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                // Simulate success (replace with actual API call)
                console.log('Form data:', data);
                resolve({ success: true });
            }, 2000);
        });
    }

    setSubmitLoading(button, isLoading) {
        if (isLoading) {
            button.disabled = true;
            button.classList.add('loading');
            button.setAttribute('aria-busy', 'true');
        } else {
            button.disabled = false;
            button.classList.remove('loading');
            button.setAttribute('aria-busy', 'false');
        }
    }

    showSuccessMessage(form) {
        const message = document.createElement('div');
        message.className = 'form-success';
        message.setAttribute('role', 'alert');
        message.innerHTML = `
            <p>✅ <strong>Mensagem enviada com sucesso!</strong></p>
            <p>Responderemos em até 24 horas úteis.</p>
        `;

        form.insertBefore(message, form.firstChild);
        message.scrollIntoView({ behavior: 'smooth', block: 'center' });

        setTimeout(() => message.remove(), 8000);
    }

    showErrorMessage(form, errorText) {
        const message = document.createElement('div');
        message.className = 'form-error';
        message.setAttribute('role', 'alert');
        message.innerHTML = `
            <p>❌ <strong>Erro ao enviar mensagem:</strong></p>
            <p>${errorText}</p>
        `;

        form.insertBefore(message, form.firstChild);
        message.scrollIntoView({ behavior: 'smooth', block: 'center' });

        setTimeout(() => message.remove(), 8000);
    }
}

// ===== CLASSE PARA ACESSIBILIDADE =====
class AccessibilityEnhancer {
    constructor() {
        this.init();
    }

    init() {
        this.setupKeyboardNavigation();
        this.setupFocusManagement();
        this.setupScreenReaderSupport();
        this.setupMotionPreferences();
    }

    setupKeyboardNavigation() {
        // Keyboard navigation for interactive elements
        document.addEventListener('keydown', (e) => {
            // Skip links navigation
            if (e.key === 'Tab' && e.shiftKey) {
                this.handleSkipLinks(e);
            }

            // Modal close on ESC
            if (e.key === 'Escape') {
                this.closeModals();
            }
        });

        // Add skip link if not exists
        this.addSkipLink();
    }

    setupFocusManagement() {
        let usingMouse = false;

        document.addEventListener('mousedown', () => {
            usingMouse = true;
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                usingMouse = false;
            }
        });

        document.addEventListener('focusin', () => {
            document.body.classList.toggle('using-mouse', usingMouse);
            document.body.classList.toggle('using-keyboard', !usingMouse);
        });
    }

    setupScreenReaderSupport() {
        // Announce dynamic content changes
        this.createAriaLiveRegion();

        // Update page title on navigation
        this.updatePageTitle();
    }

    setupMotionPreferences() {
        // Respect user motion preferences
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
        
        if (prefersReducedMotion.matches) {
            document.documentElement.classList.add('reduce-motion');
        }

        prefersReducedMotion.addEventListener('change', () => {
            document.documentElement.classList.toggle('reduce-motion', prefersReducedMotion.matches);
        });
    }

    addSkipLink() {
        if (document.querySelector('.skip-link')) return;

        const skipLink = document.createElement('a');
        skipLink.className = 'skip-link';
        skipLink.href = '#main-content';
        skipLink.textContent = 'Pular para conteúdo principal';

        document.body.insertBefore(skipLink, document.body.firstChild);
    }

    handleSkipLinks(e) {
        const skipLinks = document.querySelectorAll('.skip-link');
        if (skipLinks.length && document.activeElement === document.body) {
            e.preventDefault();
            skipLinks[0].focus();
        }
    }

    closeModals() {
        // Close any open modals or overlays
        const openModals = document.querySelectorAll('.modal.active, .overlay.active');
        openModals.forEach(modal => {
            modal.classList.remove('active');
        });
    }

    createAriaLiveRegion() {
        if (document.querySelector('#aria-live-region')) return;

        const liveRegion = document.createElement('div');
        liveRegion.id = 'aria-live-region';
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.style.position = 'absolute';
        liveRegion.style.left = '-10000px';
        liveRegion.style.width = '1px';
        liveRegion.style.height = '1px';
        liveRegion.style.overflow = 'hidden';

        document.body.appendChild(liveRegion);
    }

    announce(message) {
        const liveRegion = document.querySelector('#aria-live-region');
        if (liveRegion) {
            liveRegion.textContent = message;
        }
    }

    updatePageTitle() {
        // Update title based on current section
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && entry.intersectionRatio > 0.5) {
                    const sectionTitle = entry.target.querySelector('h2');
                    if (sectionTitle) {
                        document.title = `${sectionTitle.textContent} - Premium Layout`;
                    }
                }
            });
        }, { threshold: 0.5 });

        document.querySelectorAll('section[id]').forEach(section => {
            observer.observe(section);
        });
    }
}

// ===== INICIALIZAÇÃO DA APLICAÇÃO =====
class App {
    constructor() {
        this.navigation = null;
        this.animations = null;
        this.formValidator = null;
        this.accessibility = null;

        this.init();
    }

    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initializeComponents());
        } else {
            this.initializeComponents();
        }
    }

    initializeComponents() {
        try {
            // Initialize all components
            this.navigation = new ResponsiveNavigation();
            this.animations = new AnimationController();
            this.formValidator = new FormValidator();
            this.accessibility = new AccessibilityEnhancer();

            // Setup global error handling
            this.setupErrorHandling();

            // Log success
            this.logInitializationSuccess();

        } catch (error) {
            console.error('Erro na inicialização da aplicação:', error);
            this.handleInitializationError(error);
        }
    }

    setupErrorHandling() {
        window.addEventListener('error', (e) => {
            console.error('Erro JavaScript:', e.error);
        });

        window.addEventListener('unhandledrejection', (e) => {
            console.error('Promise rejeitada:', e.reason);
        });
    }

    handleInitializationError(error) {
        // Fallback functionality
        console.warn('Modo de fallback ativado devido a erro na inicialização');
        
        // Basic functionality without advanced features
        this.setupBasicFunctionality();
    }

    setupBasicFunctionality() {
        // Basic smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    }

    logInitializationSuccess() {
        console.log('%c🚀 Premium Responsive Layout inicializado com sucesso!', 
                   'color: #10b981; font-weight: bold; font-size: 16px;');
        console.log('📱 Navegação responsiva: ✓');
        console.log('🎨 Animações: ✓');
        console.log('📝 Validação de formulários: ✓');
        console.log('♿ Acessibilidade: ✓');
        console.log('⚡ Performance otimizada: ✓');
    }
}

// ===== INICIALIZAR APLICAÇÃO =====
const app = new App();