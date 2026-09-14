function getApiBase(): string {
  if (typeof window !== 'undefined') {
    const envUrl = process.env.NEXT_PUBLIC_API_URL;
    if (envUrl && !envUrl.includes('localhost') && !envUrl.includes('127.0.0.1')) {
      return envUrl;
    }
    const { protocol, hostname } = window.location;
    return `${protocol}//${hostname}:8000/api`;
  }
  return process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
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
    // If current hostname failed and wasn't localhost, attempt fallback
    if (typeof window !== 'undefined' && window.location.hostname !== 'localhost') {
      try {
        res = await fetch(`http://localhost:8000/api${endpoint}`, {
          ...options,
          headers,
        });
      } catch {
        throw new Error(`Failed to connect to backend server at ${apiBase}. Please verify the server is running on port 8000.`);
      }
    } else {
      throw new Error(`Failed to connect to backend server at ${apiBase}. Please verify the server is running on port 8000.`);
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
