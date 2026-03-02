import { isEmptyOrNullString } from './validators';

/**
 * Генерация полного ФИО
 * @param lastName
 * @param firstName
 * @param patronymic
 */
export const generateFIO = (lastName = '', firstName = '', middleName = ''): string => {
  const result: Array<string> = [];
  if (!isEmptyOrNullString(lastName)) {
    result.push(lastName);
  }
  if (!isEmptyOrNullString(firstName)) {
    result.push(firstName);
    if (!isEmptyOrNullString(middleName)) {
      result.push(middleName);
    }
  }
  return result.join(' ');
};

/**
 * Генерация Фамилии И.О.
 * @param lastName
 * @param firstName
 * @param patronymic
 */
export const generateFIOInitials = (lastName = '', firstName = '', middleName = ''): string => {
  const result: Array<string> = [];
  if (!isEmptyOrNullString(lastName)) {
    result.push(lastName);
  }
  if (!isEmptyOrNullString(firstName)) {
    result.push(`${firstName[0]}.`);
    if (!isEmptyOrNullString(middleName)) {
      result.push(`${middleName[0]}.`);
    }
  }
  return result.join(' ');
};

/**
 * Генерация пароля
 * @param length
 */
export const passwordGenerate = (length = 10): string => {
  const charSet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789^&/()';
  const passArray = Array.from({ length });

  return passArray.map((_, index) => charSet.charAt(Math.random() * charSet.length)).join('');
};
