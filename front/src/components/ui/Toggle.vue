<template>
  <q-toggle
    :label="label"
    :checked-icon="checkedIcon"
    :color="color"
    :unchecked-icon="uncheckedIcon"
    keep-color
    :disable="disable"
  />
</template>
<script lang="ts">
import { defineComponent, PropType } from 'vue';

export type Variants = 'dark' | 'negative' | 'positive' | 'info';

export default defineComponent({
  props: {
    color: {
      type: String as PropType<Variants>,
      default: 'dark',
    },
    checkedIcon: {
      type: String,
      default: 'check',
    },
    uncheckedIcon: {
      type: String,
      default: 'clear',
    },
    disable: {
      type: Boolean,
      default: false,
    },
    label: {
      type: String,
      default: '',
    }
  },
  setup() {
    return {};
  },
});
</script>
