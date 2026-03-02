<template>
  <q-btn-dropdown class="classes" color="dark" :label="label">
    <q-list>
      <q-item
        v-for="item in items"
        :key="item.index"
        clickable
        v-close-popup
        @click="onItemClick(item.event)"
      >
        <q-item-section>
          <q-item-label>{{ item.label }}</q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </q-btn-dropdown>
</template>
<script lang="ts">
import { defineComponent, PropType, ref } from 'vue';
import { BtnDropdown } from './s-btn-dropdown.d';

export default defineComponent({
  props: {
    label: {
      type: String,
      required: true,
    },
    items: {
      type: Array as PropType<BtnDropdown.Items[]>,
      required: true,
    },
    width: {
      type: String as PropType<BtnDropdown.BtnSizes>,
      default: 'base-xl',
    },
  },
  setup(props, { emit }) {

    const onItemClick = (eventName: string) => {
      emit(eventName);
    }

    const classesArray = ref([
      's-btn',
      `w-${props.width}`,
    ] as Array<string>);

    const classes = ref(classesArray.value.join(' ') as string);

    return {
      onItemClick,
      classes,
    }
  },
})
</script>

