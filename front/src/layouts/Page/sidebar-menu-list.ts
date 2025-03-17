
export type MenuItem = {
  id: number;
  ordinalNum: number;
  index: string | number;
  title: string;
  routeName: string;
  icon: string | null;
  children: Array<MenuItem> | [];
  permission?: (user: any) => boolean;
};

// const userCanAny = (...args: Array<string | Array<string>>) => (user: UserInfo) => {
//   const flatPermissions = flatten(args);
//   const permitted = hasPermission(flatPermissions, false, user);
//   if (!permitted) {
//     console.warn(`${user.email} failed permission check(any) for [${flatPermissions}]`);
//   }

//   return permitted;
// };

const menuItemsList: Array<MenuItem> = [
  {
    id: 1,
    ordinalNum: 1,
    title: 'Добавление номера телефона',
    routeName: 'add_number',
    index: '1',
    icon: 'add_call',
    children: [],
    // permission: userCanAny(permissionSet.service.list),
  },
  {
    id: 5,
    ordinalNum: 5,
    title: 'Домофон',
    routeName: 'domophone',
    index: '4',
    icon: 'tune',
    children: [],

    // permission: userCanAny(permissionSet.service.list),
  },
  {
    id: 6,
    ordinalNum: 6,
    title: 'Клиент',
    routeName: 'client',
    index: '4',
    icon: 'tune',
    children: [],

    // permission: userCanAny(permissionSet.service.list),
  },
];

export default menuItemsList;
