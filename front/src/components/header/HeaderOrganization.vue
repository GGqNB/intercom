<template>
  <q-btn-dropdown v-if="activeOrganization" stretch flat :label="activeOrganization.name">
    <q-list>
      <q-item-label header>Мои организации</q-item-label>
      <q-item
        v-for="item in organizations"
        :key="item.id"
        clickable
        v-close-popup
        tabindex="0"
        @click="changeActiveOrganization(item.id)"
      >
        <q-item-section avatar>
          <q-avatar
            icon="las la-briefcase"
            :color="isActiveOrganization(item.id) ? 'primary' : 'white'"
            :text-color="isActiveOrganization(item.id) ? 'white' : 'primary'"
          />
        </q-item-section>
        <q-item-section>
          <q-item-label>{{ item.name }}</q-item-label>
          <q-item-label v-if="item.inn" caption>ИНН: {{ item.inn }}</q-item-label>
        </q-item-section>
      </q-item>

      <q-separator />

      <q-item clickable @click="goToCreateOrganization">
        <q-item-section avatar>
          <q-avatar
            icon="las la-plus"
            text-color="primary"
          />
        </q-item-section>
        <q-item-section>
          <q-item-label>Добавить организацию</q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </q-btn-dropdown>
  <q-btn
    v-else
    icon="las la-plus"
    label="Добавить организацию"
    stretch
    flat
    @click="goToCreateOrganization"
  />
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  setup() {
    // TODO: Не пугаемся, я это добавил, чтобы прикинуть, как будет смотреться
    const organizations = ref([
      {
        id: 1,
        name: 'ООО "Технологии доставки"',
        inn: '8601024787',
      },
      {
        id: 2,
        name: 'ООО "Хорошие люди"',
        inn: null,
      },
      {
        id: 3,
        name: 'ООО "Квартал"',
        inn: '8601024787',
      },
    ]);

    const activeOrganization = ref(organizations.value[0]);

    const changeActiveOrganization = async (id: number) => {
      const item = organizations.value.find((item) => item.id === id);
      if (typeof item !== 'undefined') activeOrganization.value = item;
    };

    const isActiveOrganization = (id: number) => activeOrganization.value.id === id;

    const goToCreateOrganization = () => {
      // TODO: Навигация на создание организации
    };

    return {
      activeOrganization,
      organizations,
      changeActiveOrganization,
      isActiveOrganization,
      goToCreateOrganization,
    };
  },
});
</script>
