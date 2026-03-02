<template>
  <q-dialog v-model="visible" persistent>
    <q-card
      class="s-modal--form"
      :class="{
        's-modal--xs': size === 'xs',
        's-modal--sm': size === 'sm',
        's-modal--md': size === 'md',
        's-modal--lg': size === 'lg',
        's-modal--xl': size === 'xl',
      }"
    >
      <q-toolbar class="s-modal--form__header">
        <q-toolbar-title>
          <span class="s-modal--form__header-title">{{ title }}</span>
        </q-toolbar-title>

        <q-btn
          v-if="rightIconClose"
          v-close-popup
          no-caps
          icon="close"
          flat
          round
          dense
          color="white"
        />
      </q-toolbar>

      <q-separator />

      <div class="s-modal--form__body">
        <slot></slot>

        <div class="row justify-end full-width s-modal--form__footer">
          <slot name="footer"></slot>
        </div>
      </div>
    </q-card>
  </q-dialog>
</template>
<script lang="ts">
import { computed, defineComponent, PropType } from 'vue';

export type DialogSizes =
  | 'xs'
  | 'sm'
  | 'md'
  | 'lg'
  | 'xl'

export default defineComponent({
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    rightIconClose: {
      type: Boolean,
      default: true,
    },
    title: {
      type: String,
      required: true,
    },
    size: {
      type: String as PropType<DialogSizes>,
      default: 'middle',
    }
  },
  emits: ['update:show'],
  setup(props, { emit }) {
    const visible = computed({
      get: () => props.show,
      set: (value) => emit('update:show', value),
    });
    return {
      visible,
    };
  },
});
</script>
