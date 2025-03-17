<template>
  <div class="border-base-primary row s-py-lg items-center">
    <div class="s-ml-lg s-mr-lg gap-small row">
      <div>
        <s-icon
          class="s-icon hovered-color animated"
          :class="isRowCards && 'active'"
          icon-name="las la-bars"
          size="xl"
          @click="changeActiveView('row-cards')"
        />
      </div>
      <div>
        <s-icon
          class="s-icon hovered-color animated"
          :class="isColCards && 'active'"
          icon-name="las la-th-large"
          size="xl"
          @click="changeActiveView('col-cards')"
        />
      </div>
      <div>
        <s-icon
          class="s-icon hovered-color animated"
          :class="isTable && 'active'"
          icon-name="las la-table"
          size="xl"
          @click="changeActiveView('table')"
        />
      </div>
    </div>
    <slot></slot>
    <s-btn
      v-if="withClearBtn"
      class="s-ml-lg s-mr-lg"
      label="Сбросить"
      type="outline"
      width="base"
      @click="$emit('reset')"
    />
  </div>
</template>
<script lang="ts">
import { computed, defineComponent, ref } from 'vue';
import { BaseFilter } from 'SharedDir/declarations/base-filter';

export default defineComponent({
  name: 'SBaseFilter',
  props: {
    withClearBtn: {
      type: Boolean,
      default: true,
    },
  },
  emits: ['changeActiveView', 'reset'],
  setup(props, { emit }) {
    const activeViewVariant = ref<BaseFilter.ViewDataTypes>('table');

    const isRowCards = computed(() => activeViewVariant.value === 'row-cards');
    const isColCards = computed(() => activeViewVariant.value === 'col-cards');
    const isTable = computed(() => activeViewVariant.value === 'table');

    const changeActiveView = (type: BaseFilter.ViewDataTypes) => {
      activeViewVariant.value = type;
      emit('changeActiveView', type);
    };

    return {
      changeActiveView,
      isRowCards,
      isColCards,
      isTable,
    };
  },
});
</script>
