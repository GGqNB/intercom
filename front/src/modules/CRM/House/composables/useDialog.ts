import { ref} from 'vue';
import { makeRequest } from 'src/composables/useRequest';
import { useNotifications } from 'src/composables/useNotifications';
import { useSelectBackend } from 'src/composables/useSelectBackend';
import { QForm } from 'quasar';
import { Crm } from 'src/declarations/responses/crm';
import HouseApi from 'src/backend/api/classes/HouseClass';

export function useDialog(){ 
  const formVisible = ref(true);
  const formData = ref<Crm.HouseBare>({
    name: '',
    geo_adress: '',
    flat_count: 0,
    city_id: 0 

  });
  const form = ref<QForm>();
  const { getCity } = useSelectBackend();
  const $notify = useNotifications();
  const onSubmit = async () => {
    const isValid = await form.value?.validate();
    if (!isValid) {
     $notify.warning('Необходимо заполнить обязательные поля');
      return;
    }
    const response = await makeRequest(async () =>
      HouseApi.create(formData.value));
      if (response) {
        $notify.success('Добавлено');
        formData.value.name = '';
        return response.data
      }
    
}

  return {
    form,
    formData,
    getCity,
    onSubmit,
    // isEmptyOrNullString,
    // formVisible,
    // getWorkers,
    // getProcessTemplate,
    // stateOrg,
    // getOktmoGroups
  };
}