<template>
  <q-list>
    <template v-for="item in filteredMenuItemsList" :key="item.index">
      <template v-if="hasChildren(item)">
        <q-item
          v-ripple="{ color: 'ripple-menu' }"
          clickable
          :to="{ name: item.routeName }"
          active-class="s-sidebar-item--active"
          class="s-sidebar-item"
          :class="`level-${level}`"
          :style="`padding-left:${
            (item.icon !== null ? level : level * 3) * 5 + paddingLeftLevel
          }px`"
        >
          <q-tooltip
          
            anchor="center right"
            self="center middle"
            :offset="[20, 0]"
            :delay="400"
          >
            {{ item.title }}
          </q-tooltip>
          <q-item-section avatar>
            <div v-if="item.icon !== null" class="s-sidebar__icon-wrapper">
              <q-icon :name="item.icon" class="s-sidebar__icon" />
            </div>
          </q-item-section>
          <q-item-section class="s-sidebar__title">{{ item.title }}</q-item-section>
        </q-item>
      </template>
      <template v-else>
        <q-expansion-item
          :key="item.index"
          clickable
          exact
          active-class="s-sidebar-item--active"
          class="s-sidebar-expansion-item"
          expand-icon="arrow_right"
          expanded-icon="arrow_drop_down"
          expand-icon-class="s-sidebar-expansion-item__icon"
        >
          <template #header>
            <q-item-section avatar>
              <div v-if="item.icon !== null" class="s-sidebar__icon-wrapper">
                <q-icon name="home" class="s-sidebar__icon" />
              </div>
            </q-item-section>
            <q-item-section class="s-sidebar__title">{{ item.title }}</q-item-section>
          </template>
          <the-sidebar-menu-list :menu-items-list="item.children" :level="level + 1" />
        </q-expansion-item>
      </template>
    </template>
  </q-list>
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue';



import { MenuItem } from './sidebar-menu-list';

export default defineComponent({
  name: 'TheSidebarMenuList',
  props: {
    menuItemsList: {
      required: true,
      type: Array<MenuItem>,
      default() {
        return [];
      },
    },
    level: {
      required: true,
      type: Number,
      default: 1,
    },
  },
  setup(props) {

    // const appStore = useAppStore();
    // const userStore = useUserStore();

    // const { miniCollapseSidebar } = storeToRefs(appStore);

    const paddingLeftLevel = 12;

    const filteredMenuItemsList = computed(() => props.menuItemsList.filter((item: any) => {
      if (typeof item.permission === 'undefined') {
        return true;
      }

      // return item.permission(userStore.user);
    }));

    const hasChildren = (item: MenuItem): boolean => item.children.length === 0;

    /**
     * Открываем пункт меню родителя, если один из его детей выбран активным элементом
     * Срабатывает только при рендере элементов
     */
    // const isItemHaveActiveChild = (item: MenuItem): boolean => {
    //   if (item?.children && item.children.length > 0) {
    //     const routeName: RouteRecordName | null | undefined = route.name;
    //     if (typeof routeName === 'string') {
    //       // @ts-ignore
    //       return item.children.some((val) => val.routeName === routeName);
    //     }
    //   }
    //   return false;
    // };

    // onMounted(async () => {});

    return {
      paddingLeftLevel,
      // miniCollapseSidebar,

      filteredMenuItemsList,
      hasChildren,
      // isItemHaveActiveChild,
    };
  },
});
</script>
