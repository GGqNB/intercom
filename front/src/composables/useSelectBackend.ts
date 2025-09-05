// /* eslint-disable no-return-await */
import IntercomApi from 'src/backend/api/classes/IntercomClass';
import EntryApi from 'src/backend/api/classes/EntryClass';
import HouseApi from 'src/backend/api/classes/HouseClass';
import CityApi from 'src/backend/api/classes/CityClass';

export function useSelectBackend() {
  const getIntercom = async (params: any) => await IntercomApi.list(params);
  const getStownDevices = async (params: any) => await IntercomApi.stownDevices(params);
  const getEntry = async (params: any) => await EntryApi.list(params);
  const getCity = async (params: any) => await CityApi.list(params);
  const getHouse = async (params: any) => await HouseApi.list(params);


  return {
    getIntercom,
    getEntry,
    getCity,
    getHouse,
    getStownDevices
  };
}
