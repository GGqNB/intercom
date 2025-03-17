<template>
  <div :class="classes">
    <slot></slot>
  </div>
</template>
<script lang="ts">
import { defineComponent, PropType, ref } from 'vue';

export type FormWrapperWidth = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'xxl' | 'xxxl';

export default defineComponent({
  props: {
    width: {
      type: String as PropType<FormWrapperWidth>,
      default: 'lg'
    },
  },
  setup(props) {
    const classesArray = ref([
      's-form--wrapper',
      `w-${props.width}`,
    ] as Array<string>);

    const classes = ref(classesArray.value.join(' ') as string);
    return {
      classes,
    }
  },
});
</script>
