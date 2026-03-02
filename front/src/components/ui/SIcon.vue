<template>
  <q-icon :name="iconName" :size="iconSize" :color="type">
    <q-tooltip
      v-if="isVisibleTooltip"
      class="s-tooltip"
      :delay="500"
    >{{ tooltip }}</q-tooltip>
  </q-icon>
</template>
<script lang="ts">
import { computed, defineComponent, PropType } from 'vue';
import { isEmptyOrNullString } from 'src/utils/validators';

export type IconTypes = 'primary' | 'secondary' | 'accent' | 'dark';

export type IconSizes = 'small' | 'medium' | 'large' | 'xl' | 'xxl' | 'xxxl';

export default defineComponent({
  name: 'SIcon',
  props: {
    iconName: {
      type: String,
      required: true,
    },
    tooltip: {
      type: String,
      default: '',
    },
    type: {
      type: String as PropType<IconTypes>,
      default: 'dark',
    },
    size: {
      type: String as PropType<IconSizes>,
      default: 'medium',
    },
  },
  setup(props) {
    const iconSize = computed((): string => {
      switch (props.size) {
        case 'small':
          return '16px';
        case 'medium':
          return '18px';
        case 'large':
          return '20px';
        case 'xl':
          return '24px';
        case 'xxl':
          return '28px';
        case 'xxxl':
          return '35px';
        default:
          return '24px';
      }
    });

    const isVisibleTooltip = computed((): boolean => !isEmptyOrNullString(props.tooltip));
    return {
      iconSize,
      isVisibleTooltip,
    };
  },
});
</script>
