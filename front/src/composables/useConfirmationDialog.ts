import { useQuasar } from 'quasar';

import ConfirmDialog from 'src/components/Dialog/SConfirmDialog.vue';

type ExtendedQDialogOptions = {
  title?: string;
  message?: string;
  cancelLabel?: string;
  confirmLabel?: string;
  cancel?: boolean;
  persistent?: boolean;
  reverseBtn?:boolean;
};

/**
 * Обвязка над окном подтверждения
 * В качестве опций почти всегда будет передаваться message, т.к. вряд ли кому то нужно стандартное поведение
 * Вторым аргументом передаётся вызываемая функция, которая сработает, когда пользователь подтвердит действие
 * Третьим аргументом, когда отклонит действие
 *
 * @returns
 */
export const useConfirmationDialog = () => {
  const $q = useQuasar();

  const withConfirmation = (
    options: ExtendedQDialogOptions,
    confirmedAction?: any,
    cancelledAction?: () => void
  ) => {
    const quasarConfirmDialog = {
      component: ConfirmDialog,
      componentProps: {
        message: 'Вы действительно хотите выполнить?',
        ...options,
      },
    }
    const dialog = $q.dialog(quasarConfirmDialog);

    if (confirmedAction) {
      dialog.onOk(confirmedAction);
    }
    if (cancelledAction) {
      dialog.onCancel(cancelledAction);
    }
  };

  return {
    withConfirmation,
  };
};