<template>
  <s-modal
    v-model="innerValue"
    class="s-filter--modal"
    position="right"
    :use-toolbar="false"
    size="small"
  >
    <div class="s-filter--header row justify-between">
      <slot name="header">
        <div class="col-auto row items-center full-width justify-between q-px-xs">
          <div class="row items-center">
            <div class="s-pr-sm">Фильтры</div>
            <q-badge
              v-if="appliedFiltersCount"
              class="s-badge s-badge--mini"
              outline
              color="brand"
            >
              {{ appliedFiltersCount }}
            </q-badge>
          </div>

          <div class="col-auto">
            <q-btn
              class="s-close--btn"
              clickable flat no-wrap dense
              @click="innerValue = !innerValue"
            >
              <s-icon name="close" />
            </q-btn>
          </div>
        </div>
      </slot>
    </div>
    <filter-body
      classes="s-filter--elem"
      @clear="reset"
      @apply-filter="$emit('apply-filter')"
      @download="$emit('download')"
      :visible-download="visibleDownload"
    >
      <slot></slot>
    </filter-body>
  </s-modal>
</template>
<script lang="ts">
import { computed, defineComponent } from 'vue';

import FilterBody from './components/FilterBody.vue';

export default defineComponent({
  components: { FilterBody },
  props: {
    modelValue: {
      type: Boolean,
      default: false,
    },
    appliedFiltersCount: {
      type: Number || null,
      default: null,
    },
    visibleDownload: {
      type: Boolean,
      default: true,
    },
  },
  setup(props, { emit, expose }) {
    const innerValue = computed({
      get: () => props.modelValue,
      set: (value) => emit('update:modelValue', value),
    });

    const reset = () => {
      emit('clear');
    };

    expose({ reset });

    return {
      innerValue,
      reset,
    };
  },
});
</script>
