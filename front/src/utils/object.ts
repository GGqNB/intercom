/**
 * Рекурсивно выставляет все значения ключей объекта в пустой эквивалент
 * @param array объект
 */
export const resetObject = (obj: any): any => {
  for (const key in obj) {
    if (Array.isArray(obj[key])) obj[key] = [];
    else if (typeof obj[key] === 'object' && obj[key] !== null) resetObject(obj[key]);
    else obj[key] = null;
  }
  return obj;
};
