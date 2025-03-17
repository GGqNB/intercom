import { boot } from 'quasar/wrappers';
import { useLocalAuthStore } from 'src/stores/auth.store';
import { useUserStore } from 'src/stores/user.store';
import { useIndicatorStore } from 'src/stores/indicator.store';
import { useNotifications } from 'src/composables/useNotifications';

export interface MetaParams {
    /**
     * `true` или список идентификаторов ролей пользователей
     * которым доступен данный роут
     */
    authorization?: boolean | Array<number>;
    noAuthorization?: boolean;
    userBinded? : boolean;
  }
  export default boot(({ router }) => {
    router.beforeResolve(async (to ) => {
      const auth = (m?: MetaParams) => m && m.authorization;
      const needNoAuth = (m?: MetaParams) => m && m.noAuthorization;
  
      const $notify = useNotifications();

      const authStore = useLocalAuthStore();
      const indicatorStore = useIndicatorStore();
      const { meta } = to;
      if (!auth(meta) && !needNoAuth(meta)) {
        // Если роут не имеет пометку только авторизованным и не имеет пометку требуется не авторизованый, то все ОК, пропускаем
        
        return;
      }
      // Если такая пометка есть, то проверяем вообще что пользователь авторизован или не авторизован
      if ((auth(meta) && !authStore.isAuthenticated) || (needNoAuth(meta) && authStore.isAuthenticated)) {
    
        router.push('/login')
      }

    });
  },);
