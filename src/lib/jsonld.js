/* Builds the schema.org JSON-LD graph for Linen Legends. */
export function buildJsonLd(site, LIVE_PC) {
  const domain = 'https://linenlegends.com.au';
  const businessId = `${domain}/#business`;

  const areaServed = Object.entries(LIVE_PC).map(([postcode, suburb]) => ({
    '@type': 'PostalAddress',
    addressLocality: suburb,
    postalCode: String(postcode),
    addressRegion: 'QLD',
    addressCountry: 'AU',
  }));

  const localBusiness = {
    '@context': 'https://schema.org',
    '@type': 'LocalBusiness',
    '@id': businessId,
    name: site.brand,
    slogan: 'We wash it well',
    description:
      'Laundry pickup and delivery across Brisbane, Logan and South East Queensland, with GST-inclusive pricing.',
    url: domain,
    areaServed,
    priceRange: '$$',
    currenciesAccepted: 'AUD',
  };

  const service = {
    '@context': 'https://schema.org',
    '@type': 'Service',
    serviceType: 'Laundry pickup and delivery',
    provider: { '@id': businessId },
    offers: {
      '@type': 'Offer',
      priceCurrency: 'AUD',
    },
    description:
      'Wash and fold from $32 per load (about 5 kg). Collection and return $13.50. Minimum $73.50 per collection. All prices include GST.',
  };

  const faqPage = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: (site.faqs || []).map((f) => ({
      '@type': 'Question',
      name: f.q,
      acceptedAnswer: {
        '@type': 'Answer',
        text: f.a,
      },
    })),
  };

  return [localBusiness, service, faqPage];
}
