<template>
  <q-banner dense class="s-banner" :class="type">
    <div class="row justify-around items-center">
      <div :class="{ 'col-xs-10 col-md-10 col-lg-10': closable, 'col-xs-12': !closable }">
        <s-icon v-if="withIcon" class="s-banner__icon q-pr-sm" :name="iconByType" />
        <span class="s-banner__text"><slot /></span>
      </div>
      <q-btn
        v-if="closable"
        class="col-xs-2 col-md-2 col-lg-2"
        color="white"
        icon="close"
        no-wrap
        flat
        @click="close"
      />
    </div>
  </q-banner>
</template>

<script lang="ts">
import { PropType, computed, defineComponent } from 'vue';

import { BannerType, bannerTypes } from './useBanner';

const iconTypeMapping = {
  error: 'las la-info',
  info: 'las la-info',
  success: 'las la-info',
  warning: 'las la-info',
};

export default defineComponent({
  name: 'SBanner',
  props: {
    type: {
      required: false,
      type: String as PropType<BannerType>,
      default: 'info',
      validator: (v: BannerType) => bannerTypes.includes(v),
    },
    withIcon: {
      required: false,
      type: Boolean,
      default: true,
    },
    closable: {
      required: false,
      type: Boolean,
      default: false,
    },
  },
  emits: ['close'],
  setup(props, { emit }) {
    const iconByType = computed(() => iconTypeMapping[props.type]);

    const close = (): void => {
      emit('close');
    };

    return {
      close,
      iconByType,
    };
  },
});
</script>
