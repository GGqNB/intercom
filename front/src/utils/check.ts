export const isObject = (v: any) => {
  return v !== null && typeof v === 'object' && Array.isArray(v) !== true;
};

export const isDate = (v: any) => {
  return Object.prototype.toString.call(v) === '[object Date]';
};

export const isRegexp = (v: any) => {
  return Object.prototype.toString.call(v) === '[object RegExp]';
};

export const isNumber = (v: any) => {
  return typeof v === 'number' && isFinite(v);
};

export const isBoolean = (v: any): boolean => typeof v === 'boolean';

export const isArray = (v: any): boolean => Array.isArray(v);

export const isString = (v: any): boolean => typeof v === 'string';

/**
 * Функция проверяет являться ли объект
 * экземпляром одного из указанных классов
 *
 * @param obj
 * @param {Array<unknown>} arrayOfClasses
 * @returns {boolean}
 */
export const isInstanceOf = (obj: unknown, arrayOfClasses: Array<unknown>): boolean => {
  const comparator = (isInstance: boolean, classObject: any) =>
    isInstance || obj instanceof classObject;

  // @ts-ignore
  return arrayOfClasses.reduce(comparator, false);
};
