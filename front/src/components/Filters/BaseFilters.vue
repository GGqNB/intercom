<template>
  <div class="s-filter">
    <div class="s-filter--header row justify-between">
      <slot name="header" :show="show">
        <div class="col-auto row items-center">
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
            :class="{ 'rotate-180': show }"
            clickable flat no-wrap dense
            @click="show = !show"
            icon="settings"
          >
            <!-- <s-icon name="settings" /> -->
          </q-btn>
        </div>
      </slot>
    </div>

    <filter-body
      v-if="show"
      :visible-download="visibleDownload"
      @clear="reset"
      @apply-filter="$emit('apply-filter')"
      @download="$emit('download')"      
    >
      <slot></slot>
    </filter-body>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';

import FilterBody from './components/FilterBody.vue';

export default defineComponent({
  components: { FilterBody },
  props: {
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
    const show = ref(false);

    const reset = () => {
      emit('clear');
    };
    expose({ reset });


    return {
      emit,
      show,
      reset,
    };
  },
});
</script>
