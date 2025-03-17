<template>
  <s-page>
    
    <s-header
      :create-btn="false"
      title="Перейдите в сайдабар"
    />
    <div class="home_wrapper">
    
      <h3>Перейдите в сайдабар</h3>
    </div>
  </s-page>
</template>
<script lang="ts">
import { computed, defineComponent, onMounted } from 'vue';
// import SInput from 'src/components/ui/Input.vue';
import { useList } from '../composables/useAddPhone';
import { useMeta } from 'quasar';


export default defineComponent({
  name: 'AddPhonePage',
  components: {
  },
  setup() {
    const {
  } = useList();

  
  // const handleInput = (value) => {
  //   // Убираем маску перед сохранением в переменную phone
  //   phoneData.value.phone = value.replace(/\D/g, '');
  // };
  onMounted(() => console.log('1'));
    // eslint-disable-next-line no-return-assign
    // mask=" +7 (###) ###-##-##"

    return {
    
    };
  },
});
</script>
