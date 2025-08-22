import { IEndpointData } from 'src/backend/endpoint';
import { API_SERVER } from 'src/constants/common';

const url = `${API_SERVER}api/city`;


export const CITY = {
  LIST: {
    method: 'GET',
    url: `${url}/`,
  } as IEndpointData,
  CREATE: {
    method: 'POST',
    url: `${url}/`,
  } as IEndpointData,
  UPDATE(id: number): IEndpointData {
    return {
      method: 'PUT',
      url: `${url}/${id}`,
    };
  },
  DELETE(id: number): IEndpointData {
    return {
      method: 'DELETE',
      url: `${url}/${id}`,
    };
  },
};


