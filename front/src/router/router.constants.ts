export const routerMainPageName = 'add_number';

export const routerInitialPath = '/';

export const loginPageName = 'login';

// Страницы на которые разрешено входить не авторизованным пользователям
export const whiteListRouteNames: Array<string | symbol> = [
  'login',
  'ui-kit',
  'reset-password',
  'reset-password-confirm',
  'change-temp-password',
  'registration',
];

export const authorizedOnly = <T extends Record<string, unknown> = Record<string, unknown>>(
  roles?: Array<number> | number,
  meta?: T
): Record<string, unknown> & { authorization: true | Array<number> } => {
  const extraMeta = meta || ({} as T);
  if (!roles) {
    return { ...extraMeta, authorization: true };
  }
  const authorizedRoles = Array.isArray(roles) ? roles : [roles];
  return { ...extraMeta, authorization: authorizedRoles };
};
