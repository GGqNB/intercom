<template>
  <q-drawer
    v-model="collapseSidebar"
    show-if-above
    :width="sidebarFullWidth"
    :breakpoint="1023"
    side="left"
    class="s-sidebar"
  >
    <div class="s-sidebar-container">
      <the-sidebar-menu-list
        class="s-sidebar-list"
        :menu-items-list="menuItemsList"
        :level="0"
      />
    </div>
  </q-drawer>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { storeToRefs } from 'pinia';
import { useAppStore } from 'src/stores/app.store';
import { routerMainPageName, routerInitialPath } from 'src/router/router.constants';

import TheSidebarMenuList from './TheSidebarMenuList.vue';
import menuItemsList from './sidebar-menu-list';

export default defineComponent({
  name: 'TheSidebar',
  components: {
    TheSidebarMenuList,
  },
  setup() {
    const appStore = useAppStore();
    const { collapseSidebar } = storeToRefs(appStore);

    const sidebarFullWidth = 296;

    return {
      collapseSidebar,
      sidebarFullWidth,
      routerMainPageName,
      routerInitialPath,
      menuItemsList,
    };
  },
});
</script>
