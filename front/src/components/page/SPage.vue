<template>
  <div class="s-page">
    <slot></slot>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'SPage',
  setup() {
    return {};
  },
});
</script>
