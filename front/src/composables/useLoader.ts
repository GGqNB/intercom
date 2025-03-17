
import { useQuasar } from 'quasar'
import { Ref } from 'vue';
export function useLoading() {
  const $q = useQuasar()

   function showLoading() {
    $q.loading.show({
      message: 'Загрузка...',
      spinnerSize: 100,
      spinnerColor: 'blue',
    });
  }

  function hideLoading() {
    $q.loading.hide();
  }
  return {
    showLoading,
    hideLoading,
  }
}
