<template>
  <q-select
    :class="classes"
    outlined
    dense
    :disable="disable"
    :hide-bottom-space="hideBottomSpace"
    :options-dense="optionsDense"
    popup-content-class="s-select--item"
    v-model="selectedValue" 
    :options="options"  
  >
    <template #default>
      <slot></slot>
    </template>
    <template v-for="(_, name) in $slots" #[name]="slotData">
      <slot :name="name" v-bind="slotData" />
    </template>
  </q-select>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'SSelect',
  props: {
    disable: {
      type: Boolean,
      default: false,
      required: false,
    },
    required: {
      type: Boolean,
      default: false,
      required: false,
    },
    hideBottomSpace: {
      type: Boolean,
      default: true,
    },
    optionsDense: {
      type: Boolean,
      default: true,
    },
    options: {
      type: Array,   // Передаем массив опций
      default: () => [],
      required: false,
    },
    value: [String, Number]  // Добавляем привязку значения через v-model
  },
  setup(props, { slots, emit }) {
    const classesArray = ref([
      's-select',
      props.disable ? 's-select--disable' : '',
      props.required ? 'required' : '',
    ] as Array<string>);

    const classes = ref(classesArray.value.join(' ') as string);

    return {
      classes,
      slots,
      selectedValue: props.value,
      emit,
    }
  },
})
</script>
