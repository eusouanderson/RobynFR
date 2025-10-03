<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Documents</h1>

    <!-- Loading -->
    <div v-if="loading" class="text-gray-500">Carregando documentos...</div>

    <!-- Error -->
    <div v-if="error" class="text-red-500 mb-4">{{ error }}</div>

    <!-- Lista de documentos -->
    <ul v-if="!loading && documents.length">
      <li v-for="doc in documents" :key="doc.id" class="mb-2 border-b pb-2">
        <strong>{{ doc.file_name || 'Sem nome' }}</strong>
        <p class="text-gray-600">{{ doc.text_content?.slice(0, 100) || 'Sem conteúdo' }}...</p>
      </li>
    </ul>

    <!-- Sem documentos -->
    <div v-if="!loading && documents.length === 0" class="text-gray-500">
      Nenhum documento encontrado.
    </div>

    <!-- Botão para recarregar -->
    <button
      @click="loadDocuments"
      class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
    >
      Recarregar
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { listDocuments } from '@/api/index';

interface Document {
  id: number | string;
  file_name?: string;
  text_content?: string;
  [key: string]: any;
}

const loading = ref(false);
const error = ref<string | null>(null);
const documents = ref<Document[]>([]);

const loadDocuments = async () => {
  try {
    loading.value = true;
    error.value = null;

    const res = await listDocuments<{ documents: Document[] }>();
    documents.value = Array.isArray(res.documents) ? res.documents : [];
    console.log('Documentos carregados:', documents.value);
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Erro desconhecido';
    console.error('Erro ao carregar documentos:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(loadDocuments);
</script>

<style scoped></style>
