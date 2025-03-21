import { IEndpointData } from 'src/backend/endpoint';
import { API_SERVER } from 'src/constants/common';

const authUrl = `https://${API_SERVER}api/valid-key`;


export const AUTH = {
  // GET: {
  //   method: 'GET',
  //   url: `${authUrl}/`,
  // } as IEndpointData,
  ME(token: string): IEndpointData {
    return {
      method: 'GET',
      url: `${authUrl}/${token}`,
    };
  },
  LOGIN: {
    method: 'POST',
    url: `${authUrl}/login`,
  } as IEndpointData,
};


