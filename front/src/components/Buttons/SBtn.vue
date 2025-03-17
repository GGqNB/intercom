<template>
  <q-btn
    :loading="loading"
    :disable="disable"
    :class="classes"
    :label="label"
    :type="type"
    :no-caps="!caps"
  >
    <template v-if="$slots.default">
      <slot></slot>
    </template>
    <template #loading>
      <q-spinner-dots />
    </template>
  </q-btn>
</template>
<script lang="ts">
import { defineComponent, PropType, ref } from 'vue';
import { Button } from './s-btn.d';

const btnVariants = [
  'main',
  'danger',
  'success',
  'secondary',
  'white-dashed',
  'clear'
];

export default defineComponent({
  name: 'SBtn',
  props: {
    label: {
      type: String,
      required: true,
    },
    outline: {
      type: Boolean,
      default: false,
    },
    flat: {
      type: Boolean,
      default: false,
    },
    round: {
      type: Boolean,
      default: false,
    },
    loading: {
      type: Boolean,
    },
    disable: {
      type: Boolean,
      default: false,
    },
    type: {
      type: String,
      default: 'button',
    },
    caps: {
      type: Boolean,
      default: false,
    },
    width: {
      type: String as PropType<Button.BtnSizes>,
      default: 'base-xl',
    },
  },
  setup(props) {
    const classesArray = ref([
      's-btn',
      `w-${props.width}`,
      props.outline ? 's-btn--outline' : '',
      props.flat ? 's-btn--flat' : '',
      props.round ? 's-btn--round' : '',
    ] as Array<string>);

    const classes = ref(classesArray.value.join(' ') as string);
    return {
      classes,
    }
  },
})
</script>
