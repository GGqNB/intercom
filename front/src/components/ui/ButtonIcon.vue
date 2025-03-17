<template>
  <q-btn
    :round="round"
    :square="!round"
    :icon="icon"
    :outline="outline"
    :flat="flat"
    :color="variant"
  >
    <template v-if="$slots.default">
      <slot></slot>
    </template>
  </q-btn>
</template>
<script lang="ts">
import { defineComponent, PropType, ref } from 'vue';

export type BtnIconVariants =
  | 'primary'
  | 'secondary'
  | 'accent'
  | 'dark';

const btnVariants = [
  'primary',
  'secondary',
  'accent',
  'dark',
];

export default defineComponent({
  name: 'ButtonIcon',
  props: {
    variant: {
      type: String as PropType<BtnIconVariants>,
      default: 'primary',
    },
    icon: {
      type: String,
      required: true,
    },
    round: {
      type: Boolean,
      default: true,
    },
    flat: {
      type: Boolean,
      default: false,
    },
    outline: {
      type: Boolean,
      default: false,
    }
  },
  setup() {
    return {};
  },
});
</script>
