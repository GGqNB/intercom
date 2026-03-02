import isObject from 'lodash/isObject';
import { AnyObject } from '../declarations/shared';
import { AxiosError } from 'axios';
import { HTTP_CODE_ERROR } from '../constants/http-codes';

type AxiosErrorCode = number | null;

/**
 * Проверяем является ли исключение ошибкой axios
 * @param error
 * @returns {boolean}
 */
export const ifAxiosError = (error: unknown): boolean => {
  if (isObject(error) && typeof (error as AnyObject)?.request !== 'undefined') {
    return true;
  }

  return false;
};

/**
 * Проверяем не ошибка ли это валидации
 *
 * @param error
 * @returns {boolean}
 */
export const ifValidationError = (error: unknown): boolean => {
  if (!ifAxiosError(error)) {
    return false;
  }
  return (error as AxiosError)?.response?.status === HTTP_CODE_ERROR.LOGIC_ERROR;
};

/**
 * Проверить равны ли HT коды
 *
 * @param errorCode
 * @param comparedErrorCode
 * @returns
 */
export const isErrorHasCode = (errorCode: AxiosErrorCode, comparedErrorCode: number): boolean => {
  if (errorCode) {
    return errorCode === comparedErrorCode;
  }
  return false;
};

/**
 * Получить наименование ошибки из axios
 *
 * @param e
 * @returns
 */
export const getErrorDetailMessageOrDefault = (error: AxiosError, defaultValue: string): string => {
  return (
    (error as AxiosError<any>)?.response?.data?.detail ??
    (error as AxiosError<any>)?.response?.data?.error ??
    defaultValue
  );
};

/**
 * Получить код ошибки из axios
 *
 * @param e
 * @returns
 */
export const getErrorCode = (e: AxiosError): AxiosErrorCode =>
  (e as AxiosError).response?.status ?? null;

/**
 * Парсинг JWT строки
 *
 * @param token
 * @returns
 */
export const parseJwt = (token: string) => {
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch (e) {
    return null;
  }
};
