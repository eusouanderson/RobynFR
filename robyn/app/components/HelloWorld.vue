<template>
  <div class="documents-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading">Carregando documentos...</div>

    <!-- Error State -->
    <div v-else-if="error" class="error">
      Erro: {{ error }}
      <button @click="loadDocuments" class="retry-btn">Tentar Novamente</button>
    </div>

    <!-- Content -->
    <div v-else class="documents-content">
      <!-- Documents List -->
      <section class="documents-section">
        <h2>Documentos</h2>
        <div v-if="documents.length === 0" class="empty-state">Nenhum documento encontrado.</div>
        <ul v-else class="documents-list">
          <li v-for="document in documents" :key="document.id" class="document-item">
            {{ document.name || `Documento ${document.id}` }}
          </li>
        </ul>
        <button @click="loadDocuments" class="refresh-btn">Atualizar Lista</button>
      </section>

      <!-- IA Responses List -->
      <section class="ia-responses-section">
        <h2>Respostas de IA</h2>
        <div v-if="iaResponses.length === 0" class="empty-state">
          Nenhuma resposta de IA encontrada.
        </div>
        <ul v-else class="ia-responses-list">
          <li
            v-for="response in iaResponses"
            :key="response.id"
            class="response-item"
            @click="selectIAResponse(response.id)"
          >
            <div class="response-header">
              <span class="response-id">ID: {{ response.id }}</span>
              <span class="response-date" v-if="response.createdAt">
                {{ formatDate(response.createdAt) }}
              </span>
            </div>
            <div class="response-preview" v-if="response.content">
              {{ truncateText(response.content, 100) }}
            </div>
          </li>
        </ul>
        <button @click="loadIAResponses" class="refresh-btn">Atualizar Respostas</button>
      </section>

      <!-- Selected IA Response Details -->
      <section v-if="selectedIAResponse" class="selected-response-section">
        <h2>Detalhes da Resposta de IA</h2>
        <div class="response-details">
          <button @click="selectedIAResponse = null" class="close-btn">Fechar</button>
          <pre class="response-content">{{ JSON.stringify(selectedIAResponse, null, 2) }}</pre>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { listDocuments, listIAResponses, getIAResponseById } from '@/api/index';

// Tipos (ajuste conforme sua API real)
interface Document {
  id: number | string;
  file_name?: string;
  text_content?: string;
  [key: string]: any;
}

interface IAResponse {
  id: number | string;
  question?: string;
  answer?: string;
  document_id?: number | string;
  created_at?: string;
  [key: string]: any;
}

// Estados reativos
const loading = ref(false);
const error = ref<string | null>(null);
const documents = ref<Document[]>([]);
const iaResponses = ref<IAResponse[]>([]);
const selectedIAResponse = ref<IAResponse | null>(null);

// Funções
const loadDocuments = async () => {
  try {
    loading.value = true;
    error.value = null;

    const res = await listDocuments<Document[]>();
    console.log('Documentos carregados:', res);
    documents.value = Array.isArray(res) ? res : [];
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Erro desconhecido';
    console.error('Erro ao carregar documentos:', err);
  } finally {
    loading.value = false;
  }
};

const loadIAResponses = async () => {
  try {
    loading.value = true;
    error.value = null;

    const res = await listIAResponses<IAResponse[]>();

    if (!Array.isArray(res)) {
      throw new Error('Formato inesperado da resposta de IA');
    }

    iaResponses.value = res;
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Erro desconhecido';
    console.error('Erro ao carregar respostas de IA:', err);
  } finally {
    loading.value = false;
  }
};

const selectIAResponse = async (iaId: number | string) => {
  try {
    loading.value = true;
    error.value = null;
    const res = await getIAResponseById<IAResponse>(iaId);
    selectedIAResponse.value = res;
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Erro ao carregar resposta de IA';
    console.error('Erro ao carregar resposta de IA:', err);
  } finally {
    loading.value = false;
  }
};

// Utilitários
const truncateText = (text: string, maxLength: number) =>
  text.length > maxLength ? text.substring(0, maxLength) + '...' : text;

const formatDate = (dateString: string) => new Date(dateString).toLocaleDateString('pt-BR');

// Carregar dados inicialmente
onMounted(() => {
  loadDocuments();
  // loadIAResponses();
});
</script>

<style scoped>
.documents-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading,
.error {
  text-align: center;
  padding: 40px;
  font-size: 18px;
}

.error {
  color: #d32f2f;
}

.retry-btn,
.refresh-btn,
.close-btn {
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.retry-btn:hover,
.refresh-btn:hover,
.close-btn:hover {
  background-color: #1565c0;
}

.documents-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-top: 20px;
}

.documents-section,
.ia-responses-section,
.selected-response-section {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  background-color: #f9f9f9;
}

.selected-response-section {
  grid-column: 1 / -1;
}

h2 {
  margin-top: 0;
  color: #333;
  border-bottom: 2px solid #1976d2;
  padding-bottom: 10px;
}

.documents-list,
.ia-responses-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.document-item,
.response-item {
  padding: 12px;
  margin-bottom: 8px;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  cursor: default;
}

.response-item {
  cursor: pointer;
  transition: background-color 0.2s;
}

.response-item:hover {
  background-color: #f0f0f0;
}

.response-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}

.response-id {
  font-weight: bold;
  color: #1976d2;
}

.response-date {
  color: #666;
}

.response-preview {
  color: #555;
  font-size: 14px;
  line-height: 1.4;
}

.empty-state {
  text-align: center;
  color: #666;
  font-style: italic;
  padding: 20px;
}

.response-details {
  position: relative;
}

.response-content {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 14px;
  margin-top: 15px;
}

.close-btn {
  position: absolute;
  top: 0;
  right: 0;
}
</style>
