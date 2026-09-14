function getApiBase(): string {
  if (typeof window !== 'undefined') {
    // In browser context:
    // Always use relative '/api' so all requests stay on the same origin (port 3000)
    // and are proxied by Next.js rewrites to the backend.
    // This completely eliminates phone / mobile "Failed to fetch" network errors,
    // cross-origin port 8000 blocks, and Windows Defender Firewall restrictions.
    return '/api';
  }
  // Server-side rendering / Node context:
  return process.env.INTERNAL_BACKEND_URL
    ? `${process.env.INTERNAL_BACKEND_URL}/api`
    : (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api');
}

export async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const token = typeof window !== 'undefined' ? localStorage.getItem('learnwise_token') : null;
  const apiBase = getApiBase();
  
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {}),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  let res: Response;
  try {
    res = await fetch(`${apiBase}${endpoint}`, {
      ...options,
      headers,
    });
  } catch {
    // Fallback: If relative /api failed in browser, attempt direct backend connection
    if (typeof window !== 'undefined') {
      const { protocol, hostname } = window.location;
      try {
        res = await fetch(`${protocol}//${hostname}:8000/api${endpoint}`, {
          ...options,
          headers,
        });
      } catch {
        try {
          res = await fetch(`http://localhost:8000/api${endpoint}`, {
            ...options,
            headers,
          });
        } catch {
          throw new Error('Failed to connect to backend server. Please verify the server is running.');
        }
      }
    } else {
      throw new Error('Failed to connect to backend server. Please verify the server is running.');
    }
  }

  if (!res.ok) {
    let errorDetail = 'An unexpected error occurred';
    try {
      const errorJson = await res.json();
      errorDetail = errorJson.detail || JSON.stringify(errorJson);
    } catch {
      errorDetail = await res.text();
    }
    throw new Error(errorDetail);
  }

  // Handle blob or text if required
  const contentType = res.headers.get('content-type');
  if (contentType && contentType.includes('text/csv')) {
    return res.text();
  }

  return res.json();
}
