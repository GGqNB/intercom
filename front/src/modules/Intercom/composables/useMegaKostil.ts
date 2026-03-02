import { computed, ref } from 'vue';
import { useAppStore } from 'stores/app.store';
import { makeRequest } from 'src/composables/useRequest';
import  IntercomCallApi from 'src/backend/api/classes/IntercomCallClass'
import { useNotifications } from 'src/composables/useNotifications';
import {
    storeToRefs
} from 'pinia';
//снести все к чертям и избавиться от этого костыля
export function useList() {
  const appStore = useAppStore();
  const localUrlControlBoard = computed(() => appStore.localUrlControlBoard)
  const $notify = useNotifications();
  const {
            localIdLock,
        } = storeToRefs(appStore);
  const openLock = async (code : string) => {

  if(localUrlControlBoard.value == '') { 
    $notify.error('Не заполнен роут')
     return 
    }
    console.info(JSON.stringify({
      'code' : code, 
      'url': localUrlControlBoard.value,
      'lock_id' : localIdLock.value
    }))
  
  //  const response = await makeRequest(async () =>
  //       IntercomCallApi.open(1, code, localUrlControlBoard.value));
  //       if (response) {
  //         $notify.info('Запрос на открытие ушел');
  //       }
};


  return {
      openLock,  

    }
  }
  