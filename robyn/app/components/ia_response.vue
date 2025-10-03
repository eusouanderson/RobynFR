<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Respostas da IA</h1>

    <!-- Loading -->
    <div v-if="loading" class="text-gray-500">Carregando respostas...</div>

    <!-- Error -->
    <div v-if="error" class="text-red-500 mb-4">{{ error }}</div>

    <!-- Lista de respostas -->
    <ul v-if="!loading && iaResponses.length">
      <li v-for="resp in iaResponses" :key="resp.id" class="mb-4 border-b pb-2">
        <p><strong>Pergunta:</strong> {{ resp.question || 'Sem pergunta' }}</p>
        <p class="text-gray-600"><strong>Resposta:</strong> {{ resp.answer || 'Sem resposta' }}</p>
        <small class="text-gray-400"
          >Documento ID: {{ resp.document_id }}, Criado em: {{ formatDate(resp.created_at) }}</small
        >
      </li>
    </ul>

    <!-- Sem respostas -->
    <div v-if="!loading && iaResponses.length === 0" class="text-gray-500">
      Nenhuma resposta encontrada.
    </div>

    <!-- Botão para recarregar -->
    <button
      @click="loadIAResponses"
      class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
    >
      Recarregar
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { listIAResponses } from '@/api/index';

interface IAResponse {
  id: number | string;
  question?: string;
  answer?: string;
  document_id?: number | string;
  created_at?: string;
  [key: string]: any;
}

const loading = ref(false);
const error = ref<string | null>(null);
const iaResponses = ref<IAResponse[]>([]);

const loadIAResponses = async () => {
  try {
    loading.value = true;
    error.value = null;

    const res = await listIAResponses<IAResponse[]>();
    iaResponses.value = Array.isArray(res) ? res : [];
    console.log('Respostas carregadas:', iaResponses.value);
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Erro desconhecido';
    console.error('Erro ao carregar respostas da IA:', err);
  } finally {
    loading.value = false;
  }
};

const formatDate = (dateStr?: string) => {
  if (!dateStr) return '-';
  return new Date(dateStr).toLocaleString();
};

onMounted(loadIAResponses);
</script>

<style scoped>
/* Ajustes rápidos de estilo */
</style>
