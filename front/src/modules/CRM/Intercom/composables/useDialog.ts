import { ref} from 'vue';
import { makeRequest } from 'src/composables/useRequest';
import { useNotifications } from 'src/composables/useNotifications';
import { useSelectBackend } from 'src/composables/useSelectBackend';
import { QForm } from 'quasar';
import { Crm } from 'src/declarations/responses/crm';
import IntercomApi from 'src/backend/api/classes/IntercomClass';
import { generateStringWithDashes } from 'src/utils/string';
export function useDialog(){ 
  const formVisible = ref(true);
  const formData = ref<Crm.IntercomBare>({
    name: '',
    tech_name: '',
    entry_id: 0 
  });
  const form = ref<QForm>();
  const { getEntry } = useSelectBackend();
  const $notify = useNotifications();
  const onSubmit = async () => {
    const isValid = await form.value?.validate();
    if (!isValid) {
     $notify.warning('Необходимо заполнить обязательные поля');
      return;
    }
    formData.value.tech_name = generateStringWithDashes(15);
    const response = await makeRequest(async () =>
      IntercomApi.create(formData.value));
      if (response) {
        $notify.success('Добавлено');
        formData.value.tech_name = '';
        return response.data
      }
    
}

  return {
    form,
    formData,
    getEntry,
    onSubmit,
    // isEmptyOrNullString,
    // formVisible,
    // getWorkers,
    // getProcessTemplate,
    // stateOrg,
    // getOktmoGroups
  };
}