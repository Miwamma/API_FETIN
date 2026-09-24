import { useEffect, useState } from 'react';
import { api } from '../API/api';
import PageHeader from '../components/PageHeader';

function Perfil() {
  const [usuario, setUsuario] = useState(null);
  const [erro, setErro] = useState(false);

  useEffect(() => {
    api.get('/users/me')
      .then((res) => setUsuario(res.data))
      .catch(() => setErro(true));
  }, []);

  return (
    <div>
      <PageHeader title="Perfil" description="Dados da conta utilizada para acessar a API do Smart Flow." />

      {erro && <p style={{ color: '#ef4444' }}>Não foi possível carregar o perfil.</p>}
      {!erro && !usuario && <p style={{ color: '#64748b' }}>Carregando...</p>}

      {!erro && usuario && (
        <div style={{
          background: 'white',
          padding: 24,
          borderRadius: 16,
          maxWidth: 420,
          boxShadow: '0 8px 24px rgba(15,23,42,.06)',
          fontSize: 15,
          color: '#334155',
          lineHeight: 2,
        }}>
          <p><strong>Nome:</strong> {usuario.name}</p>
          <p><strong>E-mail:</strong> {usuario.email}</p>
          <p><strong>Celular:</strong> {usuario.cell}</p>
          <p><strong>Sensor vinculado:</strong> {usuario.deviceId}</p>
        </div>
      )}
    </div>
  );
}

export default Perfil;