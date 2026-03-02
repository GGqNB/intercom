import { IEndpointData } from 'src/backend/endpoint';
import { API_SERVER } from 'src/constants/common';

const url = `${API_SERVER}api/stown`;


export const STOWN = {
  HOMES: {
    method: 'GET',
    url: `${url}/`,
  } as IEndpointData,
  STOWN_DEVICES: {
    method: 'GET',
    url: `${url}/devices`,
  } as IEndpointData,
  FLATS(house_id: number): IEndpointData {
      return {
        method: 'GET',
        url: `${url}/homes/${house_id}/flats`,
      };
    },
};


