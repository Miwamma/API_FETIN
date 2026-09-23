import { useState, useRef, useEffect } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import NotificationBell from './NotificationBell';
import './Sidebar.css';

const NAV_ITEMS = [
  { label: 'Visão geral', to: '/dashboard' },
  { label: 'Medições', to: '/medicoes' },
  { label: 'Consumo', to: '/consumo' },
  { label: 'Custo de água', to: '/custo' },
];

function Sidebar({ usuario }) {
  const [menuAberto, setMenuAberto] = useState(false);
  const menuRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    function handleClickFora(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuAberto(false);
      }
    }
    document.addEventListener('mousedown', handleClickFora);
    return () => document.removeEventListener('mousedown', handleClickFora);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/login');
  };

  const iniciais = usuario?.name ? usuario.name.trim().charAt(0).toUpperCase() : '?';

  return (
    <aside className="sidebar">
      <div className="sidebar__top">
        <h1 className="sidebar__logo">Water Flow Sensor</h1>
        <p className="sidebar__description">
          API para controle de gastos e visualização de consumo de água residencial.
        </p>
      </div>

      <div style={{ marginTop: 12 }}>
        <NotificationBell />
      </div>
    
      <nav className="sidebar__nav">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) => `sidebar__link ${isActive ? 'sidebar__link--active' : ''}`}
          >
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar__account" ref={menuRef}>
        {menuAberto && (
          <div className="sidebar__menu">
            <NavLink to="/perfil" className="sidebar__menu-item" onClick={() => setMenuAberto(false)}>
              Ver perfil
            </NavLink>
            <button className="sidebar__menu-item sidebar__menu-item--danger" onClick={handleLogout}>
              Sair
            </button>
          </div>
        )}

        <button className="sidebar__account-button" onClick={() => setMenuAberto((v) => !v)}>
          <span className="sidebar__avatar">{iniciais}</span>
          <span className="sidebar__account-name">{usuario?.name || 'Usuário'}</span>
        </button>
      </div>
    </aside>
  );
}

export default Sidebar;