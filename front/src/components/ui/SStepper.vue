<!-- <template>
  <q-stepper
    header-nav
    animated
    flat
    header-class="s-stepper__header"
    class="s-stepper-horizontal"
    done-color="info"
    inactive-color="blue"
    active-color="info"
    :active-icon="activeIcon"
    horizontal
    @transition="(newVal, oldVal) => $emit('changeActiveStep', {newVal, oldVal})"
  >
    <q-step
      v-for="step in steps"
      :key="step.index"
      class="s-step__empty"
      :name="step.index"
      :title="step.name"
      :disable="step.isDisabled"
      :done="step.isDone"
      :error="step.hasError"
      :icon="step.icon"
    />
  </q-stepper>
</template>
<script lang="ts">
import { defineComponent, PropType } from 'vue';

export interface StepperData {
  index: number;
  name: string;
  isDisabled: boolean;
  isDone: boolean;
  hasError: boolean;
  icon: string;
}

export default defineComponent({
  props: {
    steps: {
      type: Array as PropType<StepperData[]>,
      required: true
    },
    activeIcon: {
      type: String,
      default: 'none',
    },
  },
  emits: ['changeActiveStep'],
  setup() {
    return {};
  },
});
</script> -->
