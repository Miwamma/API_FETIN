import { useState, useRef, useEffect } from 'react';
import { notificacaoService } from '../services/notificacaoService';
import './NotificationBell.css';

function formatarData(iso) {
  return new Date(iso).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });
}

function NotificationBell() {
  const [notificacoes, setNotificacoes] = useState([]);
  const [aberto, setAberto] = useState(false);
  const ref = useRef(null);

  function carregar() {
    notificacaoService.list()
      .then((res) => setNotificacoes(res.data))
      .catch(() => setNotificacoes([]));
  }

  useEffect(() => {
    carregar();
    const intervalo = setInterval(carregar, 30000);
    return () => clearInterval(intervalo);
  }, []);

  useEffect(() => {
    function handleClickFora(event) {
      if (ref.current && !ref.current.contains(event.target)) setAberto(false);
    }
    document.addEventListener('mousedown', handleClickFora);
    return () => document.removeEventListener('mousedown', handleClickFora);
  }, []);

  const handleMarcarComoLida = async (id) => {
    await notificacaoService.marcarComoLida(id);
    carregar();
  };

  const naoLidas = notificacoes.filter((n) => !n.read).length;

  return (
    <div className="notification-bell" ref={ref}>
      <div className="notification-bell__button-row">
        <button className="notification-bell__button" onClick={() => setAberto((v) => !v)}>
          🔔
          {naoLidas > 0 && <span className="notification-bell__badge">{naoLidas}</span>}
        </button>
      </div>

      {aberto && (
        <div className="notification-bell__panel">
          {notificacoes.length === 0 && (
            <p className="notification-bell__empty">Nenhuma notificação ainda.</p>
          )}
          {notificacoes.map((n) => (
            <div key={n.id} className={`notification-bell__item ${n.read ? '' : 'notification-bell__item--unread'}`}>
              <p className="notification-bell__message">{n.message}</p>
              <div className="notification-bell__meta">
                <span>{formatarData(n.createdAt)}</span>
                {!n.read && (
                  <button onClick={() => handleMarcarComoLida(n.id)}>Marcar como lida</button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default NotificationBell;