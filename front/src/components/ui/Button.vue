<template>
  <q-btn :class="classes">
    <template #default>
      <slot />
    </template>
    <template v-for="(_, name) in $slots" #[name]="slotData">
      <slot :name="name" v-bind="slotData" />
    </template>
    <!-- Slot по умолчанию для загрузки -->
    <template #loading>
      <q-spinner-dots />
    </template>
  </q-btn>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from 'vue';
import { QBtn } from 'quasar';

export type BtnTypes = 'brand' | 'outline' | 'light' | 'icon' | 'success' | 'danger';

export const buttonTypes: Array<BtnTypes> = ['brand', 'outline', 'light', 'icon', 'danger', 'success'];

export default defineComponent({
  name: 'SBtn',
  components: {
    QBtn,
  },
  props: {
    type: {
      required: false,
      type: String as PropType<BtnTypes>,
      default: 'brand',
    },
    fat: {
      required: false,
      type: Boolean,
      default: false,
    },
    wide: {
      required: false,
      type: Boolean,
      default: false,
    },
  },

  setup(props, { attrs, slots }) {
    // console.log('props', props);
    // console.log('attrs', attrs);

    const classes = computed(() => {
      let result = 's-btn ';
      result += `${props?.type === 'outline' ? 's-btn__outline' : ''} `;
      result += `${props?.type === 'light' ? 's-btn__light' : ''} `;
      result += `${props?.type === 'danger' ? 's-btn__danger' : ''} `;
      result += `${props?.type === 'success' ? 's-btn__success' : ''} `;
      result += `${props?.type === 'icon' ? 's-btn__icon' : ''} `;
      result += `${props?.fat ? 's-btn__fat' : ''} `;
      result += `${props?.wide ? 's-btn__wide' : ''} `;
      return result;
    });

    return { classes, slots };
  },
});
</script>
