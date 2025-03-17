<template>
  <q-input
    ref="refQInput"
    :class="classes"
    outlined
    hide-bottom-space
    clear-icon="delete"
    :maxlength="maxLength"
  >
    <template #default>
      <slot></slot>
    </template>
    <template v-for="(_, slotName) in slots" #[slotName]>
      <slot :name="slotName" />
    </template>
  </q-input>
</template>

<script lang="ts">
import { QInput } from 'quasar';
import { computed, defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'SInput',
  props: {
    required: {
      type: Boolean,
      default: false,
      required: false,
    },
    indent: {
      type: Boolean,
      required: false,
      default: false,
    },
    maxLength: {
      type: String,
      required: false,
      default: '255',
    },
  },
  expose: ['validate'],
  setup(props, { slots, attrs }) {
    const classes = computed(() => {
      let result = 's-input ';
      result += `${props.required ? 's-input--required' : ''} `;
      result += `${attrs.readonly ? 's-input--readonly' : ''} `;
      result += `${attrs.disable ? 's-input--disable' : ''} `;
      result += `${typeof attrs.dense !== 'undefined' ? 's-input--dense' : ''} `;
      result += `${props.indent ? 's-input--indent' : ''} `;

      return result;
    });

    const refQInput = ref<QInput>(null as any);

    const validate = () => refQInput.value.validate();

    return {
      classes, slots, validate, refQInput
    };
  },
});
</script>
