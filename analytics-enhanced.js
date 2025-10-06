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
        '5524998379825': { name: 'regiao_lagos', label: 'Região dos Lagos' }
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
        console.warn('⚠️ trackWhatsAppClick chamado sem elemento válido');
        return;
    }

    const url = element.href || element.getAttribute('href');
    if (!url || !url.includes('wa.me')) {
        console.warn('⚠️ trackWhatsAppClick chamado em elemento que não é WhatsApp:', url);
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
            phone_number: info.phone,
            page_section: section,
            button_location: context.location || 'popup',
            value: 10 // Valor estimado do lead
        });

        console.log('📊 WhatsApp Click (User Action):', {
            unit: info.unit_label,
            section: section,
            phone: info.phone
        });
    }
}

// ===== TRACKING DE TELEFONE GRANULAR =====
function trackPhoneClick(element, context = {}) {
    // Proteção contra chamadas acidentais
    if (!element || !element.href) {
        console.warn('⚠️ trackPhoneClick chamado sem elemento válido');
        return;
    }

    const tel = element.href || element.getAttribute('href');

    // Verificar se é realmente um link tel:
    if (!tel.startsWith('tel:')) {
        console.warn('⚠️ trackPhoneClick chamado em elemento que não é tel:', tel);
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
            phone_number: phoneNumber,
            page_section: section,
            value: 15 // Telefone tem valor maior que WhatsApp (mais comprometido)
        });

        console.log('📞 Phone Click (User Action):', {
            unit: unit.label,
            section: section,
            phone: phoneNumber
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

                console.log(`📜 Scroll: ${percent}%`);
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

                console.log(`👁️ Section Viewed: ${sectionId}`);
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

                        console.log('💰 Visualizou Preços');
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

        console.log('⭐ Review Interaction:', action);
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

        console.log('❓ FAQ Clicked:', question);
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

                        console.log(`⏱️ Tempo na Página: ${milestone}s`);
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

        console.log('📱 WhatsApp Popup:', action);
    }
}

// ===== INICIALIZAÇÃO AUTOMÁTICA =====
function initEnhancedAnalytics() {
    console.log('🚀 Iniciando Analytics Avançado RIP PET...');

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
        console.warn('⚠️ Analytics já inicializado, ignorando duplicata');
        return;
    }
    window._rippetAnalyticsInitialized = true;

    // 1. Iniciar tracking de scroll
    scrollTracking.init();

    // 2. Iniciar tracking de preços
    pricingTracking.init();

    // 3. Iniciar tracking de tempo
    timeTracking.init();

    // 4. Rastrear todos os links de WhatsApp
    const whatsappLinks = document.querySelectorAll('a[href*="wa.me"]');
    console.log(`🔗 Encontrados ${whatsappLinks.length} links de WhatsApp`);
    whatsappLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            console.log('👆 Clique detectado em WhatsApp');
            trackWhatsAppClick(this);
        });
    });

    // 5. Rastrear todos os links de telefone
    const phoneLinks = document.querySelectorAll('a[href^="tel:"]');
    console.log(`📞 Encontrados ${phoneLinks.length} links de telefone`);
    phoneLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            console.log('👆 Clique detectado em telefone');
            trackPhoneClick(this);
        });
    });

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

    console.log('✅ Analytics Avançado Configurado!');
    console.log('📊 Eventos disponíveis:', [
        'click_whatsapp',
        'click_phone',
        'scroll_depth',
        'section_view',
        'view_pricing',
        'review_interaction',
        'faq_click',
        'time_on_page',
        'whatsapp_popup'
    ]);
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
