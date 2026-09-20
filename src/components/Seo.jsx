import { useEffect } from 'react';
import { buildJsonLd } from '../lib/jsonld.js';
import site from '../data/site.js';
import { LIVE_PC } from '../data/coverageData.js';

export default function Seo({ title, description, path }) {
  useEffect(() => {
    document.title = title
      ? `${title} — Linen Legends`
      : 'Linen Legends — Laundry collected, washed and returned';

    if (description) {
      let meta = document.querySelector('meta[name="description"]');
      if (!meta) {
        meta = document.createElement('meta');
        meta.setAttribute('name', 'description');
        document.head.appendChild(meta);
      }
      meta.setAttribute('content', description);
    }

    let canonical = document.querySelector('link[rel="canonical"]');
    if (!canonical) {
      canonical = document.createElement('link');
      canonical.setAttribute('rel', 'canonical');
      document.head.appendChild(canonical);
    }
    canonical.setAttribute('href', `https://linenlegends.com.au${path || ''}`);

    if (!document.getElementById('ll-jsonld')) {
      const script = document.createElement('script');
      script.type = 'application/ld+json';
      script.id = 'll-jsonld';
      script.textContent = JSON.stringify(buildJsonLd(site, LIVE_PC));
      document.head.appendChild(script);
    }
  }, [title, description, path]);

  return null;
}
