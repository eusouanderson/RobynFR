const baseUrl = process.env.API_URL || 'http://localhost:8080';

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${baseUrl}${endpoint}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`Erro HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}

export async function listDocuments<T>() {
  return request<T>('/documents');
}

export async function listIAResponses<T>() {
  return request<T>('/ia/responses');
}

export async function getIAResponseById<T>(iaId: number | string) {
  return request<T>(`/ia/responses/${iaId}`);
}
