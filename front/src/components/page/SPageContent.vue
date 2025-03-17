<template>
  <div class="s-page__body">
    <slot></slot>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'SPageContainer',
  setup() {
    return {};
  },
});
</script>
