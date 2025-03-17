/**
 * образает текст в шаблоне vue по количеству указанных символов
 * @param text: исходный текст
 * @param length: количество символов, которое требуется оставить в тексте для шаблона (по умолчанию = 20)
 */
export const cropText = (text: string, length = 20) => {
  if (!text) return '';

  if (text.length <= length) {
    return text;
  }
  return `${text.substring(0, length)}...`;
};

/**
 * Транслитерирование строки
 * Привет -> privet
 *
 * @param str
 */
export const transliterateString = (str: string): string => {
  const converter: Record<string, string> = {
    а: 'a',
    б: 'b',
    в: 'v',
    г: 'g',
    д: 'd',
    е: 'e',
    ё: 'e',
    ж: 'zh',
    з: 'z',
    и: 'i',
    й: 'y',
    к: 'k',
    л: 'l',
    м: 'm',
    н: 'n',
    о: 'o',
    п: 'p',
    р: 'r',
    с: 's',
    т: 't',
    у: 'u',
    ф: 'f',
    х: 'h',
    ц: 'c',
    ч: 'ch',
    ш: 'sh',
    щ: 'sch',
    ь: '',
    ы: 'y',
    ъ: '',
    э: 'e',
    ю: 'yu',
    я: 'ya',
    А: 'A',
    Б: 'B',
    В: 'V',
    Г: 'G',
    Д: 'D',
    Е: 'E',
    Ё: 'E',
    Ж: 'Zh',
    З: 'Z',
    И: 'I',
    Й: 'Y',
    К: 'K',
    Л: 'L',
    М: 'M',
    Н: 'N',
    О: 'O',
    П: 'P',
    Р: 'R',
    С: 'S',
    Т: 'T',
    У: 'U',
    Ф: 'F',
    Х: 'H',
    Ц: 'C',
    Ч: 'Ch',
    Ш: 'Sh',
    Щ: 'Sch',
    Ь: '',
    Ы: 'Y',
    Ъ: '',
    Э: 'E',
    Ю: 'Yu',
    Я: 'Ya',
  };

  const transliteratedString = str
    .split('')
    .map((letter) => converter[letter] ?? letter)
    .join('');

  return transliteratedString;
};

export const transliterateRusStringToSlug = (str: string): string => {
  // Вырезаем цифры и другие символы вначале строки
  const translitString = transliterateString(str)
    .trim()
    .replaceAll(' ', '_')
    .replace(/_{1,}/g, '_') // Заменяем множество "__" на один "_"
    .toLowerCase();

  const normalizedString = translitString
    .replace(/(^[^a-z]*)([.]*)/, '')
    .replace(/[^a-z0-9_]/g, '');
  return normalizedString;
};

/**
 * Проверяет является ли строка числом
 * @param value string
 */
export const isNumberInString = (value: string | number): boolean => {
  const re = /^0|(-?[1-9]{1}[0-9]*[.,]?[0-9]*)$/;
  if (re.test(`${value}`)) {
    return true;
  }
  return false;
};

export const capitalize = (value: string) => {
  if (!value) return '';
  value = value.toString();
  return value.charAt(0).toUpperCase() + value.slice(1);
};

export const ucfirst = (str: string) => {
  return str.charAt(0).toUpperCase() + str.slice(1);
};

export const getFirstLettersFromText = (text = '') => {
  if (text.length === 0 || text === null) {
    return '';
  }
  return text.split(' ').reduce((prevStr, str) => prevStr + str.charAt(0).toUpperCase(), '');
};

export const extractPhoneNumber = (phoneNumber: string): string => {
  
  let phoneUpdateNumber = phoneNumber.slice(3)
  phoneUpdateNumber = phoneUpdateNumber.replace('-', '')
  phoneUpdateNumber = phoneUpdateNumber.replace('-', '')
  phoneUpdateNumber = phoneUpdateNumber.replace(' ', '')
  phoneUpdateNumber = phoneUpdateNumber.replace(' ', '')
  phoneUpdateNumber = phoneUpdateNumber.replace('(', '')
  phoneUpdateNumber = phoneUpdateNumber.replace(')', '')
  console.log(phoneUpdateNumber)
  return phoneUpdateNumber;
} 