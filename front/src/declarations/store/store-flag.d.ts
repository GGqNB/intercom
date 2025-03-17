/* eslint-disable @typescript-eslint/no-empty-interface */
import { User } from '../responses/user';

export namespace StoreFlag {
  /**
   * Декларация для всех модулей
   */
   export interface StateInterface {
    app: AppStateInterface;
    auth: AuthStateInterface;
    user: UserStateInterface;
  }

  /**
  * Декларация модуля приложения
  */
  export interface AppStateInterface {
    collapseSidebar: boolean;
  }

  /**
  * Декларация модуля авторизации
  */
  export interface AuthStateInterface {
    accessToken: null | string;
  }

  /**
   * Декларация модуля пользователя
   */
  export interface UserStateInterface {
    user: null |  User.UserNewBare
    haveWorkers: boolean;
  }

  /**
   * Декларация для фильтров
   */
  export interface FiltersStateInterface {
 
  }

  /**
   * Декларация для пагинации
   */
}
