<template>
  <q-page-container class="s-main-container">
    <router-view />
    <q-inner-loading class="preloader" :showing="showLoading">
      <q-spinner-facebook color="brand" size="56px" />
    </q-inner-loading>
  </q-page-container>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import { useLoadingStore } from 'src/stores/loading.store';

export default defineComponent({
  name: 'TheContainer',
  setup() {
    const loadingStore = useLoadingStore();

    const showLoading = computed(() => loadingStore.getLoading);

    // onMounted(async () => {});

    return {
      showLoading,
    };
  },
});
</script>
