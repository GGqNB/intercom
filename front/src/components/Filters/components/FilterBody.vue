<template>
  <div class="s-filter--body row items-center">
    <slot></slot>

    <div class="col-12 s-filter--controls" :class="classes">
      <slot name="controls" :reset="reset">
        <div class="row q-gutter-y-md justify-start">
          <div class="col-12 col-md-auto">
            <div class="row q-gutter-x-lg q-gutter-y-sm items-center justify-center">
              <div class="col-auto">
                <s-btn
                  label="Очистить"
                  icon="close"
                  width="full"
                  :outline="true"
                  @click="reset"
                />
              </div>

              <div class="col-auto">
                <s-btn label="Применить" @click="$emit('apply-filter')" />
              </div>
              <div class="col-auto" v-if="visibleDownload">
                <s-btn icon="download" label="Скачать таблицу" @click="$emit('download')"></s-btn>
              </div>
            </div>
          </div>
        </div>
      </slot>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    classes: {
      type: String,
      default: '',
    },
    visibleDownload: {
      type: Boolean,
      default: true,
    },
  },
  emits: ['apply-filter', 'clear', 'download'],
  setup(props, { emit, expose }) {
    const reset = () => {
      emit('clear');
    };

    expose({ reset });

    return {
      reset,
    };
  },
});
</script>
