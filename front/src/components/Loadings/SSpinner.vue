<template>
  <div v-if="visible" class="spinner-container">
    <q-spinner :size="size" :color="color" class="s-spinner" />
  </div>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    visible: {
      type: Boolean,
      default: false,
    },
    size: {
      type: Number,
      default: 50,
    },
    color: {
      type: String,
      default: 'primary',
    },
  },
});
</script>

<style>
/* .spinner-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 9999;
}

.s-spinner {
  color: white;
} */
</style>
