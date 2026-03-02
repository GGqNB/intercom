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
import { BtnIcons } from './s-btn-icon.d';
import { ComponentVariantsValidator } from 'SharedDir/validators/components';

const btnVariants = [
  'primary',
  'secondary',
  'accent',
  'dark',
];

export default defineComponent({
  name: 'SBtnIcon',
  props: {
    variant: {
      type: String as PropType<BtnIcons.BtnIconVariants>,
      default: 'primary',
      validator: (el:string) => ComponentVariantsValidator(el, btnVariants, 'Button icon'),
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
    return {}
  },
})
</script>
