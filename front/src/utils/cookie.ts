/**
 * Выставление cookie
 * @param name
 * @param val
 * @param days
 */
export function setCookie(name: string, val: string, days = 30) {
  const date = new Date();
  const value = val;

  // Время жизни Cookie в днях
  date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);

  // Выставление куки по имени
  document.cookie = `${name}=${value}; expires=${date.toUTCString()}; path=/`;
}

/**
 * Получение cookie
 * @param name
 * @returns
 */
export function getCookie(name: string): string {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);

  if (parts.length === 2) {
    // @ts-ignore
    return parts.pop().split(';').shift();
  }

  return '';
}

/**
 * Удаление Cookie
 * @param name
 */
export function deleteCookie(name: string) {
  const date = new Date();

  // Удаление Cookie
  date.setTime(date.getTime() + -1 * 24 * 60 * 60 * 1000);

  // Выставить удаление Cookie
  document.cookie = `${name}=; expires=${date.toUTCString()}; path=/`;
}

/**
 * Удаление всех Cookie
 * @param name
 */
 export function deleteAllCookies() {
  const cookies = document.cookie.split(';');

  for (let i = 0; i < cookies.length; i+=1) {
    const cookie = cookies[i];
    const eqPos = cookie.indexOf('=');
    const name = eqPos > -1 ? cookie.substring(0, eqPos) : cookie;
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT`;
  }
}
