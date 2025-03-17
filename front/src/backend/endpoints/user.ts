import { IEndpointData } from 'src/backend/endpoint';
import { API_SERVER } from 'src/constants/common';

const userUrl = `${API_SERVER}/user`;


export const USER = {
  GET: {
    method: 'GET',
    url: `${userUrl}/`,
  } as IEndpointData,
  ME: {
    method: 'GET',
    url: `${userUrl}/profile/`,
  } as IEndpointData,
  CREATE: {
    method: 'POST',
    url: `${userUrl}/`,
  } as IEndpointData,
  LOGIN: {
    method: 'POST',
    url: `${userUrl}/auth`,
  } as IEndpointData,
  BIND_LOCK(id: number): IEndpointData {
    return {
      method: 'GET',
      url: `${userUrl}/bind/lock/${id}`,
    };
  },
    BIND_ALL_LOCK: {
    method: 'POST',
    url: `${userUrl}/bind/locks/`,
  } as IEndpointData,

  DELETE(): IEndpointData {
    return {
      method: 'DELETE',
      url: `${userUrl}/`,
    };
  },
};


