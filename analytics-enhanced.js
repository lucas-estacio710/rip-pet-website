/**
 * =====================================================
 * RIP PET - ANALYTICS AVANÇADO GA4
 * =====================================================
 *
 * Sistema de tracking granular para inteligência de negócio
 * - Eventos específicos por unidade e serviço
 * - Funil de conversão completo
 * - Scroll tracking por seções
 * - User journey mapping
 *
 * =====================================================
 */

// Configuração de unidades e mapeamento de telefones
const ANALYTICS_CONFIG = {
    units: {
        '5512997996543': { name: 'vale_paraiba', label: 'Vale do Paraíba' },
        '5511991603041': { name: 'sao_paulo', label: 'São Paulo' },
        '5513998068262': { name: 'santos', label: 'Santos' },
        '5519999161977': { name: 'campinas', label: 'Campinas' },
        '5524998379825': { name: 'resende', label: 'Resende' },
        '553599042223': { name: 'pouso_alegre', label: 'Pouso Alegre' }
    },
    sections: {
        'hero': 'Topo da Página',
        'servicos': 'Seção de Serviços',
        'processo': 'Como Funciona',
        'depoimentos': 'Depoimentos',
        'faq': 'FAQ',
        'footer': 'Rodapé'
    }
};

// Utility: Detectar seção atual baseada na posição do clique
function detectCurrentSection(element) {
    const sections = document.querySelectorAll('section[id]');
    let currentSection = 'unknown';

    sections.forEach(section => {
        const rect = section.getBoundingClientRect();
        if (rect.top <= window.innerHeight / 2 && rect.bottom >= window.innerHeight / 2) {
            currentSection = section.id || 'unknown';
        }
    });

    return currentSection;
}

// Utility: Extrair informações de URL do WhatsApp
function extractWhatsAppInfo(url) {
    const phoneMatch = url.match(/wa\.me\/(\d+)/);
    const phone = phoneMatch ? phoneMatch[1] : 'unknown';
    const unit = ANALYTICS_CONFIG.units[phone] || { name: 'unknown', label: 'Desconhecido' };

    return {
        phone: phone,
        unit_name: unit.name,
        unit_label: unit.label
    };
}

// ===== TRACKING DE WHATSAPP GRANULAR =====
function trackWhatsAppClick(element, context = {}) {
    // Proteção contra chamadas acidentais
    if (!element) {
        return;
    }

    const url = element.href || element.getAttribute('href');
    if (!url || !url.includes('wa.me')) {
        return;
    }

    const info = extractWhatsAppInfo(url);
    const section = context.section || detectCurrentSection(element);

    // Evento GA4 otimizado
    if (typeof gtag !== 'undefined') {
        gtag('event', 'click_whatsapp', {
            event_category: 'conversion',
            event_label: `whatsapp_${info.unit_name}`,
            unit_name: info.unit_name,
            unit_label: info.unit_label,
            destination_phone: info.phone,
            page_section: section,
            button_location: context.location || 'popup',
            value: 10 // Valor estimado do lead
        });
    }

    // Meta Pixel tracking
    if (typeof fbq !== 'undefined') {
        fbq('track', 'Contact', {
            content_name: 'WhatsApp Click',
            content_category: 'Contact'
        });
    }
}

// ===== TRACKING DE TELEFONE GRANULAR =====
function trackPhoneClick(element, context = {}) {
    // Proteção contra chamadas acidentais
    if (!element || !element.href) {
        return;
    }

    const tel = element.href || element.getAttribute('href');

    // Verificar se é realmente um link tel:
    if (!tel.startsWith('tel:')) {
        return;
    }

    const phoneNumber = tel.replace('tel:', '').replace(/\D/g, '');
    const unit = ANALYTICS_CONFIG.units[phoneNumber] || { name: 'unknown', label: 'Desconhecido' };
    const section = context.section || detectCurrentSection(element);

    if (typeof gtag !== 'undefined') {
        gtag('event', 'click_phone', {
            event_category: 'conversion',
            event_label: `phone_${unit.name}`,
            unit_name: unit.name,
            unit_label: unit.label,
            destination_phone: phoneNumber,
            page_section: section,
            value: 15 // Telefone tem valor maior que WhatsApp (mais comprometido)
        });
    }

    // Meta Pixel tracking
    if (typeof fbq !== 'undefined') {
        fbq('track', 'Contact', {
            content_name: 'Phone Click',
            content_category: 'Contact'
        });
    }
}

// ===== SCROLL TRACKING POR SEÇÕES =====
const scrollTracking = {
    percentages: [25, 50, 75, 90],
    tracked: new Set(),
    sectionsTracked: new Set(),

    trackPercentage(percent) {
        const key = `scroll_${percent}`;
        if (!this.tracked.has(key)) {
            this.tracked.add(key);

            if (typeof gtag !== 'undefined') {
                gtag('event', 'scroll_depth', {
                    event_category: 'engagement',
                    event_label: `${percent}_percent`,
                    percent: percent
                });

            }
        }
    },

    trackSection(sectionId) {
        if (!this.sectionsTracked.has(sectionId)) {
            this.sectionsTracked.add(sectionId);

            if (typeof gtag !== 'undefined') {
                gtag('event', 'section_view', {
                    event_category: 'engagement',
                    event_label: `viewed_${sectionId}`,
                    section_name: sectionId
                });

            }
        }
    },

    init() {
        let ticking = false;

        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    // Tracking de porcentagem
                    const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;

                    this.percentages.forEach(percent => {
                        if (scrollPercent >= percent) {
                            this.trackPercentage(percent);
                        }
                    });

                    // Tracking de seções visíveis
                    const sections = document.querySelectorAll('section[id]');
                    sections.forEach(section => {
                        const rect = section.getBoundingClientRect();
                        const sectionId = section.id;

                        // Seção está visível em pelo menos 30%
                        if (rect.top < window.innerHeight * 0.7 && rect.bottom > window.innerHeight * 0.3) {
                            this.trackSection(sectionId);
                        }
                    });

                    ticking = false;
                });

                ticking = true;
            }
        });
    }
};

// ===== TRACKING DE VISUALIZAÇÃO DE PREÇOS =====
const pricingTracking = {
    tracked: new Set(),

    init() {
        // Detectar quando usuário visualiza seção de preços/serviços
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !this.tracked.has('pricing_view')) {
                    this.tracked.add('pricing_view');

                    if (typeof gtag !== 'undefined') {
                        gtag('event', 'view_pricing', {
                            event_category: 'engagement',
                            event_label: 'pricing_section',
                            value: 5 // Interesse moderado
                        });

                    }
                }
            });
        }, { threshold: 0.5 });

        const servicosSection = document.getElementById('servicos');
        if (servicosSection) {
            observer.observe(servicosSection);
        }
    }
};

// ===== TRACKING DE REVIEWS/DEPOIMENTOS =====
function trackReviewInteraction(action, reviewData = {}) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'review_interaction', {
            event_category: 'engagement',
            event_label: action,
            action: action,
            review_unit: reviewData.unit || 'unknown',
            value: 3 // Engagement com social proof é valioso
        });

    }
}

// ===== TRACKING DE FAQ =====
function trackFAQClick(question) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'faq_click', {
            event_category: 'engagement',
            event_label: question.substring(0, 100), // Limitar tamanho
            question_text: question,
            value: 2
        });

    }
}

// ===== TRACKING DE TEMPO NA PÁGINA =====
const timeTracking = {
    startTime: Date.now(),
    milestones: [30, 60, 120, 300], // 30s, 1min, 2min, 5min
    tracked: new Set(),

    init() {
        setInterval(() => {
            const timeOnPage = Math.floor((Date.now() - this.startTime) / 1000);

            this.milestones.forEach(milestone => {
                if (timeOnPage >= milestone && !this.tracked.has(milestone)) {
                    this.tracked.add(milestone);

                    if (typeof gtag !== 'undefined') {
                        gtag('event', 'time_on_page', {
                            event_category: 'engagement',
                            event_label: `${milestone}_seconds`,
                            seconds: milestone,
                            value: Math.floor(milestone / 30) // Valor aumenta com tempo
                        });

                    }
                }
            });
        }, 5000); // Check a cada 5 segundos
    }
};

// ===== TRACKING DE POPUP DE WHATSAPP =====
function trackWhatsAppPopup(action) {
    if (typeof gtag !== 'undefined') {
        gtag('event', 'whatsapp_popup', {
            event_category: 'engagement',
            event_label: action,
            action: action,
            value: action === 'opened' ? 3 : 1
        });

    }
}

// ===== INICIALIZAÇÃO AUTOMÁTICA =====
function initEnhancedAnalytics() {

    // Aguardar DOM estar pronto
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupTracking);
    } else {
        setupTracking();
    }
}

function setupTracking() {
    // Evitar múltiplas inicializações
    if (window._rippetAnalyticsInitialized) {
        return;
    }
    window._rippetAnalyticsInitialized = true;

    // 1. Iniciar tracking de scroll
    scrollTracking.init();

    // 2. Iniciar tracking de preços
    pricingTracking.init();

    // 3. Iniciar tracking de tempo
    timeTracking.init();

    // 4. Rastrear todos os links de WhatsApp (apenas cliques REAIS de usuário)
    function attachWhatsAppListeners() {
        const whatsappLinks = document.querySelectorAll('a[href*="wa.me"]');
        whatsappLinks.forEach(link => {
            // Evitar adicionar múltiplos listeners
            if (link.dataset.whatsappTracked) return;
            link.dataset.whatsappTracked = 'true';

            link.addEventListener('click', function(e) {
                // Proteção: só rastrear se foi clique real do usuário (não programático)
                if (!e.isTrusted) {
                    return;
                }

                trackWhatsAppClick(this);
            }, { passive: true });
        });
    }

    // Anexar listeners iniciais
    attachWhatsAppListeners();

    // 5. Rastrear todos os links de telefone (apenas cliques REAIS de usuário)
    function attachPhoneListeners() {
        const phoneLinks = document.querySelectorAll('a[href^="tel:"]');
        phoneLinks.forEach(link => {
            // Evitar adicionar múltiplos listeners
            if (link.dataset.phoneTracked) return;
            link.dataset.phoneTracked = 'true';

            link.addEventListener('click', function(e) {
                // Proteção: só rastrear se foi clique real do usuário (não programático)
                if (!e.isTrusted) {
                    return;
                }

                trackPhoneClick(this);
            }, { passive: true });
        });
    }

    // Anexar listeners iniciais
    attachPhoneListeners();

    // Observar mudanças no DOM para popups dinâmicos
    const observer = new MutationObserver(() => {
        attachPhoneListeners();
        attachWhatsAppListeners();
    });
    observer.observe(document.body, { childList: true, subtree: true });

    // 6. Interceptar abertura do popup de WhatsApp
    const whatsappPopupBtn = document.querySelector('.whatsapp-btn, [onclick*="openWhatsAppPopup"]');
    if (whatsappPopupBtn) {
        whatsappPopupBtn.addEventListener('click', function() {
            trackWhatsAppPopup('opened');
        });
    }

    const whatsappPopupClose = document.getElementById('whatsappPopupClose');
    if (whatsappPopupClose) {
        whatsappPopupClose.addEventListener('click', function() {
            trackWhatsAppPopup('closed');
        });
    }

    // 7. Rastrear cliques em reviews (modal)
    document.querySelectorAll('.review-card-carousel button').forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.review-card-carousel');
            const unit = card ? card.querySelector('.unit-badge')?.textContent : 'unknown';
            trackReviewInteraction('read_more', { unit });
        });
    });

    // 8. Rastrear FAQ (já existe trackEvent, vamos melhorar)
    document.querySelectorAll('.faq-question').forEach(question => {
        question.addEventListener('click', function() {
            const questionText = this.textContent.trim();
            trackFAQClick(questionText);
        });
    });

    // 9. Page View com informações extras
    if (typeof gtag !== 'undefined') {
        gtag('event', 'page_view_enhanced', {
            event_category: 'engagement',
            page_title: document.title,
            page_location: window.location.href,
            device_type: window.innerWidth < 768 ? 'mobile' : 'desktop'
        });
    }
}

// Iniciar quando script carregar
initEnhancedAnalytics();

// Exportar funções para uso global (se necessário)
window.RIPPETAnalytics = {
    trackWhatsAppClick,
    trackPhoneClick,
    trackReviewInteraction,
    trackFAQClick,
    trackWhatsAppPopup
};
