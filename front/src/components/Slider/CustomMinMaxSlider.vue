<template>
  <div class="range-slider-container range-slider">
    <input
      type="range"
      class="range-slider range-slider__input"
      :min="minValue"
      :max="maxLeft"
      :value="leftValue"
      @input="handleLeftThumbChange"
    >
    <input
      type="range"
      class="range-slider range-slider__input range-slider__input-second"
      :min="minRigth"
      :max="maxValue"
      :value="rightValue"
      @input="handleRightThumbChange"
    >
  </div>
</template>

<script>
import { defineComponent, ref, computed } from 'vue';

export default defineComponent({
  props: {
    minValue: {
      type: Number,
      default: 0,
    },
    maxValue: {
      type: Number,
      default: 100,
    },
    defaultLeftValue: {
      type: Number,
      default: 25,
    },
    defaultRightValue: {
      type: Number,
      default: 75,
    },
  },
  emits: ['range-change'],
  setup(props, { emit }) {
    const leftValue = ref(props.defaultLeftValue);
    const rightValue = ref(props.defaultRightValue);

    const maxLeft = ref((props.maxValue / 2) + 1);
    const minRigth = ref((props.minValue * 2) - 1);

    const handleLeftThumbChange = (event) => {
      leftValue.value = event.target.value;
      emit('range-change', leftValue.value, rightValue.value);
    };

    const handleRightThumbChange = (event) => {
      rightValue.value = event.target.value;
      emit('range-change', leftValue.value, rightValue.value);
    };

    return {
      leftValue: computed(() => leftValue.value),
      rightValue: computed(() => rightValue.value),
      handleLeftThumbChange,
      handleRightThumbChange,
      maxLeft,
      minRigth,
    };
  },
});
</script>

<style lang="scss">
.range-slider {
  display: flex;
  align-items: center;
  height: 8px;
}

.range-slider__input {
  width: 100%;
}

.range-slider__input {
  width: 100%;
  background-color: #eeeeee;
  border-radius: 10px 0px 0px 10px;
  -webkit-appearance: none; // убираем стандартный стиль для инпута range в Safari
  &::-webkit-slider-thumb {
    -webkit-appearance: none; // убираем стандартный стиль для ползунка в Safari
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background-color: #007aff;
    border: none;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.2);
    margin-top: -2px;
  }
  &::-moz-range-thumb {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background-color: #007aff;
    border: none;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
    margin-top: -2px;
  }
  &::-ms-thumb {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background-color: #007aff;
    border: none;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
    margin-top: -2px;
  }
}
.range-slider__input-second{
  border-radius: 0px 10px 10px 0px;
}
</style>
