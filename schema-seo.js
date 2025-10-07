/**
 * =====================================================
 * RIP PET - STRUCTURED DATA (Schema.org)
 * =====================================================
 *
 * SEO avançado com JSON-LD para Google Rich Snippets
 * - LocalBusiness (7 unidades)
 *   • Pindamonhangaba (Matriz)
 *   • Vale do Paraíba (São José dos Campos)
 *   • São Paulo
 *   • Santos
 *   • Campinas
 *   • Resende (RJ)
 *   • Pouso Alegre (MG)
 * - Services
 * - Reviews/Ratings
 * - FAQs
 * - Videos
 * - HowTo
 *
 * =====================================================
 */

// ===== 1. LOCAL BUSINESS SCHEMA (7 UNIDADES) =====
const localBusinessSchemas = [
    {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": "https://rippet.com.br/#pindamonhangaba",
        "name": "R.I.P PET Crematório de Animais Pindamonhangaba - 24h",
        "image": "https://rippet.com.br/rippet_logo_horizontal_fundo_claro.png",
        "description": "Serviços funerários para animais de estimação em Pindamonhangaba. Matriz com crematório próprio, atendimento 24h humanizado e total transparência.",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Estrada Municipal Francisco Barros Abreu, Estr. Mun. José Benedito Marcondes Vieira, 800 - Goiabal",
            "addressLocality": "Pindamonhangaba",
            "addressRegion": "SP",
            "postalCode": "12412-847",
            "addressCountry": "BR"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": -22.9760647,
            "longitude": -45.4157029
        },
        "telephone": "+55-12-99799-6543",
        "url": "https://rippet.com.br",
        "priceRange": "$$",
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59"
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": "90",
            "bestRating": "5",
            "worstRating": "1"
        },
        "sameAs": [
            "https://www.instagram.com/rippetcrematorio/",
            "https://www.facebook.com/rippetcrematorio/",
            "https://www.google.com/maps/place/R.I.P+PET+Cremat%C3%B3rio+de+Animais+Pindamonhangaba+-+24h/@-22.9760647,-45.4157029,17z/"
        ]
    },
    {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": "https://rippet.com.br/#vale-paraiba",
        "name": "R.I.P. Pet Crematório de Animais São José dos Campos - 24h",
        "image": "https://rippet.com.br/rippet_logo_horizontal_fundo_claro.png",
        "description": "Serviços funerários para animais de estimação em São José dos Campos e Vale do Paraíba. Atendimento 24h humanizado com total transparência.",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Av. Dr. Ademar de Barros, 1257 - Vila Ema",
            "addressLocality": "São José dos Campos",
            "addressRegion": "SP",
            "postalCode": "12245-010",
            "addressCountry": "BR"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": -23.2034305,
            "longitude": -45.8933872
        },
        "telephone": "+55-12-99799-6543",
        "url": "https://rippet.com.br",
        "priceRange": "$$",
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59"
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "5.0",
            "reviewCount": "304",
            "bestRating": "5",
            "worstRating": "1"
        },
        "sameAs": [
            "https://www.instagram.com/rippetcrematorio/",
            "https://www.facebook.com/rippetcrematorio/",
            "https://www.google.com/maps/place/R.I.P.+Pet+Cremat%C3%B3rio+de+Animais+S%C3%A3o+Jos%C3%A9+dos+Campos+-+24h/@-23.2034305,-45.8933872,17z/"
        ]
    },
    {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": "https://rippet.com.br/#sao-paulo",
        "name": "R.I.P. Pet Funeral e Crematório de Animais",
        "image": "https://rippet.com.br/rippet_logo_horizontal_fundo_claro.png",
        "description": "Cemitério e crematório de animais de estimação em São Paulo. Atendimento 24h humanizado com total transparência.",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "R. Roque Friguglieti - Santa Cecilia",
            "addressLocality": "São Paulo",
            "addressRegion": "SP",
            "addressCountry": "BR"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": -23.5341326,
            "longitude": -46.6577966
        },
        "telephone": "+55-11-99160-3041",
        "url": "https://rippet.com.br",
        "priceRange": "$$",
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59"
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "5.0",
            "reviewCount": "1491",
            "bestRating": "5",
            "worstRating": "1"
        },
        "sameAs": [
            "https://www.instagram.com/rippetcrematorio/",
            "https://www.facebook.com/rippetcrematorio/",
            "https://www.google.com/maps/place/R.I.P.+Pet+Funeral+e+Cremat%C3%B3rio+de+Animais/@-23.5341326,-46.6577966,17z/"
        ]
    },
    {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": "https://rippet.com.br/#santos",
        "name": "RIP Pet - Funeral e Crematório de Animais - Santos",
        "image": "https://rippet.com.br/rippet_logo_horizontal_fundo_claro.png",
        "description": "Crematório e serviços funerários para animais de estimação em Santos. Atendimento 24h humanizado com total transparência.",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Av. Cel. Joaquim Montenegro, 334 - Ponta da Praia",
            "addressLocality": "Santos",
            "addressRegion": "SP",
            "postalCode": "11035-002",
            "addressCountry": "BR"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": -23.9793001,
            "longitude": -46.3028134
        },
        "telephone": "+55-13-99806-8262",
        "url": "https://rippet.com.br",
        "priceRange": "$$",
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59"
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "5.0",
            "reviewCount": "371",
            "bestRating": "5",
            "worstRating": "1"
        },
        "sameAs": [
            "https://www.instagram.com/rippetcrematorio/",
            "https://www.facebook.com/rippetcrematorio/",
            "https://www.google.com/maps/place/RIP+Pet+-+Funeral+e+Cremat%C3%B3rio+de+Animais+-+Santos/@-23.9793001,-46.3028134,17z/"
        ]
    },
    {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": "https://rippet.com.br/#campinas",
        "name": "R.I.P. PET Crematório de Animais Campinas - 24h",
        "image": "https://rippet.com.br/rippet_logo_horizontal_fundo_claro.png",
        "description": "Serviços funerários para animais de estimação em Campinas. Atendimento 24h humanizado com total transparência.",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Av. Dr. Heitor Penteado, 841 - Parque Taquaral",
            "addressLocality": "Campinas",
            "addressRegion": "SP",
            "postalCode": "13075-185",
            "addressCountry": "BR"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": -22.8743698,
            "longitude": -47.0610401
        },
        "telephone": "+55-19-99916-1977",
        "url": "https://rippet.com.br",
        "priceRange": "$$",
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59"
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "5.0",
            "reviewCount": "816",
            "bestRating": "5",
            "worstRating": "1"
        },
        "sameAs": [
            "https://www.instagram.com/rippetcrematorio/",
            "https://www.facebook.com/rippetcrematorio/",
            "https://www.google.com/maps/place/R.I.P.+PET+Cremat%C3%B3rio+de+Animais+Campinas+-+24h/@-22.8743698,-47.0610401,17z/"
        ]
    },
    {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": "https://rippet.com.br/#resende",
        "name": "R.I.P. PET Crematório de animais",
        "image": "https://rippet.com.br/rippet_logo_horizontal_fundo_claro.png",
        "description": "Serviços funerários para animais de estimação em Resende (RJ). Atendimento 24h humanizado com total transparência.",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "R. Santa Teresinha, 168 - Paraíso",
            "addressLocality": "Resende",
            "addressRegion": "RJ",
            "postalCode": "27535-200",
            "addressCountry": "BR"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": -22.4526892,
            "longitude": -44.4335443
        },
        "telephone": "+55-24-99837-9825",
        "url": "https://rippet.com.br",
        "priceRange": "$$",
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59"
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "5.0",
            "reviewCount": "186",
            "bestRating": "5",
            "worstRating": "1"
        },
        "sameAs": [
            "https://www.instagram.com/rippetcrematorio/",
            "https://www.facebook.com/rippetcrematorio/",
            "https://www.google.com/maps/place/R.I.P.+PET+Cremat%C3%B3rio+de+animais/@-22.4526892,-44.4335443,17z/"
        ]
    },
    {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": "https://rippet.com.br/#pouso-alegre",
        "name": "R.I.P. Pet - Crematório de Animais",
        "image": "https://rippet.com.br/rippet_logo_horizontal_fundo_claro.png",
        "description": "Serviços funerários para animais de estimação em Pouso Alegre (MG). Atendimento 24h humanizado com total transparência.",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "R. Paulino Pereira da Silva, 69 - Saude",
            "addressLocality": "Pouso Alegre",
            "addressRegion": "MG",
            "postalCode": "37551-110",
            "addressCountry": "BR"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": -22.2250931,
            "longitude": -45.939912
        },
        "telephone": "+55-35-99904-2223",
        "url": "https://rippet.com.br",
        "priceRange": "$$",
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59"
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "5.0",
            "reviewCount": "35",
            "bestRating": "5",
            "worstRating": "1"
        },
        "sameAs": [
            "https://www.instagram.com/rippetcrematorio/",
            "https://www.facebook.com/rippetcrematorio/",
            "https://www.google.com/maps/place/R.I.P.+Pet+-+Cremat%C3%B3rio+de+Animais/@-22.2250931,-45.939912,17z/"
        ]
    }
];

// ===== 2. SERVICE SCHEMA =====
const serviceSchema = {
    "@context": "https://schema.org",
    "@type": "Service",
    "serviceType": "Cremação de Animais",
    "provider": {
        "@type": "Organization",
        "name": "RIP PET",
        "url": "https://rippet.com.br"
    },
    "areaServed": {
        "@type": "State",
        "name": "São Paulo"
    },
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Serviços de Cremação",
        "itemListElement": [
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": "Cremação Individual",
                    "description": "Cremação individual com acompanhamento completo e urna personalizada"
                }
            },
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": "Cremação Coletiva",
                    "description": "Cremação coletiva com dignidade e respeito"
                }
            },
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": "Velório Pet",
                    "description": "Espaço dedicado para despedida do seu animal de estimação"
                }
            },
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": "Busca Domiciliar 24h",
                    "description": "Busca do pet em sua residência a qualquer hora"
                }
            }
        ]
    }
};

// ===== 3. FAQ SCHEMA =====
const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {
            "@type": "Question",
            "name": "Como funciona a remoção 24 horas?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Nosso serviço de remoção funciona 24 horas por dia, 7 dias por semana. Entre em contato conosco a qualquer momento e nossa equipe especializada irá até sua residência para buscar seu pet com todo cuidado e respeito."
            }
        },
        {
            "@type": "Question",
            "name": "O que é cremação individual?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Na cremação individual, apenas o seu pet é cremado por vez, garantindo que as cinzas retornadas sejam exclusivamente dele. Você pode acompanhar o processo e recebe uma urna personalizada."
            }
        },
        {
            "@type": "Question",
            "name": "Quanto tempo demora o processo?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "O processo completo geralmente leva de 24 a 48 horas, dependendo do tamanho do animal e do tipo de cremação escolhido. Mantemos você informado em cada etapa."
            }
        },
        {
            "@type": "Question",
            "name": "Posso acompanhar a cremação?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Sim! Na cremação individual, você pode acompanhar todo o processo presencialmente ou por vídeo, garantindo total transparência e tranquilidade."
            }
        },
        {
            "@type": "Question",
            "name": "Qual a diferença entre cremação individual e coletiva?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Na cremação individual, apenas seu pet é cremado e você recebe as cinzas em uma urna. Na cremação coletiva, vários animais são cremados juntos e as cinzas são depositadas em um jardim memorial."
            }
        }
    ]
};

// ===== 4. VIDEO SCHEMA =====
const videoSchema = {
    "@context": "https://schema.org",
    "@type": "VideoObject",
    "name": "Nosso compromisso com a Transparência - RIP PET",
    "description": "Conheça nosso processo transparente de cremação de animais. Tenha certeza que seu pet será cremado conforme sua escolha.",
    "thumbnailUrl": "https://rippet.com.br/images/video-thumbnail.jpg",
    "uploadDate": "2024-01-01",
    "contentUrl": "https://rippet.com.br/transparencia.mp4",
    "embedUrl": "https://rippet.com.br/#processo"
};

// ===== 5. HOWTO SCHEMA (Processo de Cremação) =====
const howToSchema = {
    "@context": "https://schema.org",
    "@type": "HowTo",
    "name": "Como funciona o processo de cremação na RIP PET",
    "description": "Passo a passo completo do processo de cremação de animais com transparência e dignidade",
    "step": [
        {
            "@type": "HowToStep",
            "name": "Primeiro Contato",
            "text": "Entre em contato conosco por WhatsApp ou telefone. Nossa equipe está disponível 24 horas para atendê-lo.",
            "position": 1
        },
        {
            "@type": "HowToStep",
            "name": "Busca Domiciliar",
            "text": "Nossa equipe vai até sua residência buscar seu pet com todo cuidado e respeito, em até 2 horas.",
            "position": 2
        },
        {
            "@type": "HowToStep",
            "name": "Velório (Opcional)",
            "text": "Oferecemos espaço dedicado para você se despedir do seu companheiro com tranquilidade.",
            "position": 3
        },
        {
            "@type": "HowToStep",
            "name": "Cremação",
            "text": "Processo de cremação realizado com dignidade. Na cremação individual, você pode acompanhar.",
            "position": 4
        },
        {
            "@type": "HowToStep",
            "name": "Entrega",
            "text": "Entregamos as cinzas em urna personalizada, com certificado de cremação individual.",
            "position": 5
        }
    ]
};

// ===== 6. ORGANIZATION SCHEMA (Principal) =====
const organizationSchema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "RIP PET",
    "url": "https://rippet.com.br",
    "logo": "https://rippet.com.br/rippet_logo_horizontal_fundo_claro.png",
    "description": "Cremação de animais com dignidade. Atendimento 24h humanizado, com total transparência e confiança. Milhares de famílias atendidas.",
    "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+55-12-99799-6543",
        "contactType": "customer service",
        "areaServed": "BR",
        "availableLanguage": "Portuguese"
    },
    "sameAs": [
        "https://www.instagram.com/rippetcrematorio/",
        "https://www.facebook.com/rippetcrematorio/"
    ]
};

// ===== 7. BREADCRUMB SCHEMA =====
const breadcrumbSchema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://rippet.com.br"
        },
        {
            "@type": "ListItem",
            "position": 2,
            "name": "Serviços",
            "item": "https://rippet.com.br/#servicos"
        },
        {
            "@type": "ListItem",
            "position": 3,
            "name": "Sobre Nós",
            "item": "https://rippet.com.br/#processo"
        }
    ]
};

// ===== FUNÇÃO DE INICIALIZAÇÃO =====
function injectSchemas() {
    const schemas = [
        organizationSchema,
        ...localBusinessSchemas,
        serviceSchema,
        faqSchema,
        videoSchema,
        howToSchema,
        breadcrumbSchema
    ];

    schemas.forEach((schema, index) => {
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.text = JSON.stringify(schema);
        script.id = `schema-${index}`;
        document.head.appendChild(script);
    });

    console.log('✅ SEO Schemas injetados:', schemas.length);
}

// Executar quando DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectSchemas);
} else {
    injectSchemas();
}
