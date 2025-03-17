const generateCrudEndpoints = (urlEndpoint: string): CRUDEndpointCollection => ({
  LIST: {
    method: 'GET',
    url: urlEndpoint,
  },
  LIST_BRIEF: {
    method: 'GET',
    url: `${urlEndpoint}/brief`,
  },
  GET(id: number) {
    return {
      method: 'GET',
      url: `${urlEndpoint}/${id.toString()}`,
    };
  },
  STORE: {
    method: 'POST',
    url: urlEndpoint,
  },
  UPDATE(id: number) {
    return {
      method: 'PUT',
      url: `${urlEndpoint}/${id.toString()}`,
    };
  },
  DELETE(id: number) {
    return {
      method: 'DELETE',
      url: `${urlEndpoint}/${id.toString()}`,
    };
  },
});
