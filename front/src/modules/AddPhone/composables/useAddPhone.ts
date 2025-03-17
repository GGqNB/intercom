import { ref } from 'vue';
import { Network } from 'src/declarations/responses/network';
import { makeRequest } from 'src/composables/useRequest';
import { useNotifications } from 'src/composables/useNotifications';
import UserApi from 'src/backend/api/classes/UserApiClass';
import { useCurrentUser } from 'src/composables/useCurrentUser'; 
import { stringNumberWithoutSymbols }  from 'src/utils/helpers';
import { useLoading } from 'src/composables/useLoader';
import { useIndicator } from 'src/composables/useIndicator';
import { useRoute } from "vue-router";
import { useIndicatorStore } from 'src/stores/indicator.store';

export function useList() {

    return {

    }
}
  