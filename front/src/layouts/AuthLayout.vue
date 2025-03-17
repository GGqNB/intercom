<template>
  <q-layout view="hHh lpR fFf" class="auth__container row">
    <div class="col-xs-0 col-md-6 col-lg-7">
      <div class="auth__card auth__card--image row items-end auth__image_background" />
    </div>

    <q-page-container
      class="col-xs-12 col-sm-12 col-md-6 col-lg-5 row items-center justify-center s-card"
    >
      <div>
        <router-view />
      </div>
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { routerInitialPath } from 'src/router/router.constants';

export default defineComponent({
  name: 'AuthLayout',

  components: {},

  setup() {
    return { routerInitialPath };
  },
});
</script>
