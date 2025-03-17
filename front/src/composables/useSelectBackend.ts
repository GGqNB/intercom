// /* eslint-disable no-return-await */
import PhoneApi from 'src/backend/api/classes/PhoneApiClass';
import LocksApi from 'src/backend/api/classes/LocksApiClass';

export function useSelectBackend() {
  const getPhones = async (params: any) => await PhoneApi.phoneList(params);
  const getLocks = async (params: any) => await LocksApi.list(params);


  return {
    getPhones,
    getLocks
  };
}
