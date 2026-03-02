<template>
  <q-layout view="hHh Lpr lFf">
    <the-header />
    <the-sidebar />
    <the-container />
  </q-layout>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import TheSidebar from './Page/TheSidebar.vue';
import TheHeader from './Page/TheHeader.vue';
import TheContainer from './Page/TheContainer.vue';

export default defineComponent({
  name: 'MainLayout',

  components: {
    TheSidebar,
    TheHeader,
    TheContainer,
  },

  setup() {
    const drawer = ref(false);
    return {
      drawer,
    };
  },
});
</script>
