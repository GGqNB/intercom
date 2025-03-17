<!-- <template>
  <q-btn-toggle
    class="s-toggle"
    :class="styles?.variant"
    unelevated
    :toggle-color="styles?.toggleColor"
    :color="styles?.color"
    :no-caps="noCaps"
    :text-color="styles?.textColor"
    :options="options"
  />
</template>
<script lang="ts">
import { defineComponent, PropType, Ref, ref } from 'vue';
import { ButtonToggles } from './s-btn-toggle.d';
import { ComponentVariantsValidator } from 'RootDir/validators/components';

const toggleBtnVariants = [
  'main',
];

export default defineComponent({
  name: 'SBtnToggle',
  props: {
    variant: {
      type: String as PropType<ButtonToggles.ToggleBtnVariants>,
      default: 'main',
      validator: (el:string) => ComponentVariantsValidator(el, toggleBtnVariants, 'Button Toggle'),
    },
    options: {
      type: Array as PropType<ButtonToggles.ToggleBtnOption[]>,
      required: true
    },
    noCaps: {
      type: Boolean,
      default: true,
    }
  },
  setup(props) {
    const toggleVariantStyles: Ref<ButtonToggles.ToggleBtnStyles[]> = ref([
      {
        variant: 'main',
        toggleColor: 'primary',
        color: 'white',
        textColor: 'primary',
      },
    ]);
    const styles = ref(toggleVariantStyles.value.find(item => item.variant === props.variant));
    return {
      styles,
    }
  },
})
</script> -->
