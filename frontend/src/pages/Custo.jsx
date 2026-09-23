import { useEffect, useState } from 'react';
import { custoService } from '../services/custoService';
import InfoCard from '../components/InfoCard';
import PageHeader from '../components/PageHeader';
import { formatDateTime } from '../utils/format';
import '../styles/cards.css';

function Custo() {
  const [custo, setCusto] = useState({ data: null, loading: true, error: false });
  const [reiniciando, setReiniciando] = useState(false);

  function carregar() {
    custoService.getCusto()
      .then((res) => setCusto({ data: res.data, loading: false, error: false }))
      .catch(() => setCusto({ data: null, loading: false, error: true }));
  }

  useEffect(() => {
    carregar();
  }, []);

  const handleReiniciar = async () => {
    const confirmado = window.confirm(
      'Isso vai zerar o consumo e custo contabilizados até agora nesta aba. As medições não são apagadas, só deixam de contar no ciclo atual. Confirmar?'
    );
    if (!confirmado) return;

    setReiniciando(true);
    try {
      await custoService.reiniciarCiclo();
      setCusto({ data: null, loading: true, error: false });
      carregar();
    } catch (erro) {
      console.error(erro);
    } finally {
      setReiniciando(false);
    }
  };

  return (
    <div>
      <PageHeader
        title="Custo de água"
        description="Estimativa de quanto o consumo do ciclo atual representa em reais, com base na tarifa por metro cúbico configurada no sistema."
      />

      <div className="info-grid" style={{ maxWidth: 260, marginBottom: 16 }}>
        <InfoCard
          title="Custo estimado"
          value={custo.data ? `R$ ${custo.data.totalCost.toFixed(2).replace('.', ',')}` : '--'}
          loading={custo.loading}
          error={custo.error}
          highlight
        />
      </div>

      {custo.data && !custo.loading && (
        <p style={{ marginBottom: 8, color: '#64748b', fontSize: 14 }}>
          Baseado em {custo.data.totalCubicMeters.toFixed(3)} m³ e tarifa de{' '}
          R$ {custo.data.waterTariffPerCubicMeter.toFixed(2)}/m³.
        </p>
      )}

      <p style={{ marginBottom: 24, color: '#94a3b8', fontSize: 13 }}>
        {custo.data?.cicloIniciadoEm
          ? `Ciclo iniciado em ${formatDateTime(custo.data.cicloIniciadoEm)}`
          : 'Contabilizando desde a primeira medição registrada.'}
      </p>

      <button
        onClick={handleReiniciar}
        disabled={reiniciando}
        style={{
          padding: '11px 20px',
          borderRadius: 10,
          border: '1px solid #ef4444',
          background: 'white',
          color: '#ef4444',
          fontWeight: 600,
          cursor: 'pointer',
        }}
      >
        {reiniciando ? 'Reiniciando...' : 'Reiniciar ciclo'}
      </button>
    </div>
  );
}

export default Custo;