import { AxiosError, AxiosResponse } from 'axios';
import isObject from 'lodash/isObject';
// import { useNotifications } from './useNotifications';
import { MakeRequestOptions } from 'RootDir/declarations/composables/request';
import { useLoading } from './useLoading';
import { useNotifications } from './useNotifications';

const defaultMakeRequestOptions: MakeRequestOptions = {
  useLoader: true,
  catchErrors: true,
  skipHttpCodes: [401, 429],
  dontAlert: false,
  reThrow: true,
  defaultMessage: 'При выполнении запроса произошла ошибка',
  startLoading: () => {
    console.debug('Standard "startLoading" was used!');
    const { general, action } = useLoading();
    general.show();
    action.show();
  },
  finishLoading: () => {
    console.debug('Standard "finishLoading" was used!');
    const { general, action } = useLoading();
    general.hide();
    action.hide();
  },
};

export const ifAxiosError = (error: unknown): boolean => {
  if (isObject(error) && typeof (error as any)?.request !== 'undefined') {
    return true;
  }

  return false;
};

const shouldWeAlert = (error: unknown, options: MakeRequestOptions): boolean => {
  if (options.dontAlert === true) {
    return false;
  }

  // if (Array.isArray(options.dontAlert) && isInstanceOf(error, options.dontAlert) ) {
  //   return false;
  // }

  return true;
};

export const shouldWeCatch = (error: unknown, options: MakeRequestOptions): boolean => {
  if (!options.catchErrors) {
    return false;
  }

  if (
    ifAxiosError(error)
    && (error as AxiosError)?.response?.status
    && options.skipHttpCodes.includes((error as AxiosError)?.response?.status || 0)
  ) {
    return false;
  }

  return true;
};

const getErrorMessage = (error: unknown): undefined | string => {
  if (ifAxiosError(error)) {
    const detail = (
      ((error as AxiosError).response as AxiosResponse<{ detail: { detail : string} }>)?.data?.detail.detail
      || ((error as AxiosError).response as AxiosResponse<{ message: string }>)?.data?.message
      || ((error as AxiosError).response as AxiosResponse<{ detail: string }>)?.data?.detail
    );
  
    if(detail == 'Не удалось получить профиль'){
      return 'Укажите свой номер на главной странице'
    }
  

  if(detail == 'Phone aleady exists'){
    return 'Такой номер уже есть в системе'
  }

  if(detail != undefined){
    return detail.toString()
  }
  if (error instanceof Error) {
    return error.message;
  }

  if (typeof error === 'string') {
    return error;
  }

  return undefined;
  }
  
};
export const makeRequest = async <T>(
  request: () => Promise<T>,
  options: Partial<MakeRequestOptions> = {}
): Promise<T> => {
  const  { error }  = useNotifications();
  const o = { ...defaultMakeRequestOptions, ...options };
  console.debug('Making request with options...', options);
  try {
  
    o.useLoader && o.startLoading && (await o.startLoading());
    return await request();
  } catch (e) {
    if (shouldWeCatch(error, o) && shouldWeAlert(e, o)) {
      error(getErrorMessage(e) ?? o.defaultMessage);
      
    }
    throw e;
  } finally {
    o.useLoader && o.finishLoading && (await o.finishLoading());
  }
};
