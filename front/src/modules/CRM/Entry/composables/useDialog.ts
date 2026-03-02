import { ref} from 'vue';
import { makeRequest } from 'src/composables/useRequest';
import { useNotifications } from 'src/composables/useNotifications';
import { useSelectBackend } from 'src/composables/useSelectBackend';
import { QForm } from 'quasar';
import { Crm } from 'src/declarations/responses/crm';
import EntryApi from 'src/backend/api/classes/EntryClass';
import { generateStringWithDashes } from 'src/utils/string';
export function useDialog(){ 
  const formVisible = ref(true);
  const formData = ref<Crm.EntryBare>({
    name: '',
    flat_first: 0,
    flat_last: 0,
    house_id: 0 
  });
  const form = ref<QForm>();
  const { getHouse } = useSelectBackend();
  const $notify = useNotifications();
  const onSubmit = async () => {
    const isValid = await form.value?.validate();
    if (!isValid) {
     $notify.warning('Необходимо заполнить обязательные поля');
      return;
    }
    const response = await makeRequest(async () =>
      EntryApi.create(formData.value));
      if (response) {
        $notify.success('Добавлено');
        formData.value.name = '';
        return response.data
      }
    
}

  return {
    form,
    formData,
    getHouse,
    onSubmit,
    // isEmptyOrNullString,
    // formVisible,
    // getWorkers,
    // getProcessTemplate,
    // stateOrg,
    // getOktmoGroups
  };
}