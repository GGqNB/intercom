import { Notify } from 'quasar';
import { Notifications } from 'RootDir/declarations/composables/notifications';

export function useNotifications(): Notifications.NotificationTypes {

  const callNotification = (message: string, additionalParameters: Notifications.NotificationParamsType = {}) => {
    const quasarNotifyConfig: Notifications.NotificationParamsType = {
      ...{
        message,
        color: 'primary',
        position: 'top-right',
        textColor: 'white',
        timeout: 2500,
        actions: [{ icon: 'close', color: 'white' }],
      },
      ...additionalParameters,
    };
    Notify.create(quasarNotifyConfig);
  };

  function success(message = 'Данные успешно сохранены') {
    callNotification(message, { color: 'positive', type: 'positive' });
  }

  function warning(message = 'Произошла ошибка!') {
    callNotification(message, { color: 'orange-6', type: 'warning' });
  }

  function error(message = 'При сохранении произошла ошибка!') {
    callNotification(message, { color: 'negative', type: 'negative' });
  }

  function info(message = 'Добро пожаловать!') {
    callNotification(message, { color: 'accent', type: 'info' });
  }

  return {
    success,
    error,
    info,
    warning,
  };
}
