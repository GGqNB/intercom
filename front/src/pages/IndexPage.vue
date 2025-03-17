<template>
  <q-page class="">
    <h1>dsaad</h1>
  </q-page>
</template>

<script lang="ts">
import { defineComponent  } from 'vue';

export default defineComponent({
  name: 'IndexPage',
  components: { 

  },
  setup () {
    
    const onDragEnd = (event) => {
      console.log('Событие окончания перетаскивания:', event);
    };

    return {
      items: [1,2,3,4,4],
      dragOptions: {
        animation: 200,
      },
      drag: true,
      onDragEnd,
     };
  }
});
</script>
