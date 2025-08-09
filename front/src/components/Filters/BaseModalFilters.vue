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

        <div class="col-auto row items-center q-gutter-sm">
          <div>
            <q-btn
              icon="settings"
              clickable flat no-wrap dense
              @click="changeVisible"
            >
            </q-btn>
          </div>
          <div v-if="appliedFiltersCount > 0">
            <q-btn
              class="s-close--btn"
              clickable flat no-wrap dense
              @click="$emit('clear')"
              :class="{ 'rotate-180': show }"

            >
              <s-icon name="close" />
            </q-btn>
          </div>
          
        </div>
      </slot>
    </div>

    <s-modal-filters
      v-model="show"
      :applied-filters-count="appliedFiltersCount"
      :visible-download="visibleDownload"
      @apply-filter="applyFilter"
      @clear="clear"
      @download="download"
    >
      <slot></slot>
    </s-modal-filters>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  props: {
    appliedFiltersCount: {
      type: Number,
      default: 0,
    },
    visibleDownload: {
      type: Boolean,
      default: true,
    },
  },
  setup(props, { emit }) {
    const show = ref(false);

    function changeVisible() {
      show.value = !show.value;
    }

    function applyFilter() {
      changeVisible();
      emit('apply-filter');
    }

    function download() {
      changeVisible();
      emit('download');
    }

    function clear() {
      changeVisible();
      emit('clear');
    }

    return {
      show,

      changeVisible,
      applyFilter,
      clear,
      download
    };
  },
});
</script>
