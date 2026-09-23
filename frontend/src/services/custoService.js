import { api } from '../API/api';

export const custoService = {
  getCusto: () => api.get('/custo'),
  reiniciarCiclo: () => api.post('/custo/reiniciar'),
};