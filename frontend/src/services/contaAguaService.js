import { api } from '../API/api';

export const contaAguaService = {
  create: (data) => api.post('/contas-agua', data),
  list: () => api.get('/contas-agua'),
  delete: (id) => api.delete(`/contas-agua/${id}`),
  getReferenciaDiaria: () => api.get('/contas-agua/referencia-diaria'),
};