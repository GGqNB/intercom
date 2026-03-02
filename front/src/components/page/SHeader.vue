<template>
  <div class="s-page__header m-none-auto">
    <s-btn
      v-if="backBtn"
      label="Назад"
      type="outline"
      width="base"
      :outline="true"
      icon="las la-arrow-left"
      @click="$router.back()"
    />
    <div class="flex items-center mt-medium">
      <div class="fs-xl">{{ title }}</div>
      <s-btn
        v-if="createBtn"
        class="s-page-header--btn"
        :label="labelBtn"
        color="green"
        width="base"
        @click="$emit('clickBtn')"
      />
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'SHeader',
  props: {
    title: {
      type: String,
      required: true,
    },
    backBtn: {
      type: Boolean,
      default: false,
    },
    createBtn: {
      type: Boolean,
      default: false,
    },
    labelBtn: {
      type: String,
      default: 'Добавить',
    }
  },
  emits: ['clickBtn'],
  setup() {
    const $router = useRouter();
    return {
      $router,
    };
  },
});
</script>
