import { useEffect, useState } from 'react';
import { medicaoService } from '../services/medicaoService';
import { contaAguaService } from '../services/contaAguaService';
import { consumoAtipicoService } from '../services/consumoAtipicoService';
import InfoCard from '../components/InfoCard';
import PageHeader from '../components/PageHeader';
import ConsumoChart from '../components/ConsumoChart';
import '../styles/cards.css';

function Consumo() {
  const [litros, setLitros] = useState({ data: null, loading: true, error: false });
  const [m3, setM3] = useState({ data: null, loading: true, error: false });

  const [contas, setContas] = useState({ data: [], loading: true, error: false });
  const [referencia, setReferencia] = useState({ data: null, loading: true, error: false, insuficiente: false });
  const [statusHoje, setStatusHoje] = useState({ data: null, loading: true, error: false });
  const [historico, setHistorico] = useState({ data: null, loading: true, error: false });

  const [consumoM3Input, setConsumoM3Input] = useState('');
  const [mesReferenciaInput, setMesReferenciaInput] = useState('');
  const [enviando, setEnviando] = useState(false);
  const [mensagemForm, setMensagemForm] = useState('');

  function carregarContasEReferencia() {
    contaAguaService.list()
      .then((res) => setContas({ data: res.data, loading: false, error: false }))
      .catch(() => setContas({ data: [], loading: false, error: true }));

    contaAguaService.getReferenciaDiaria()
      .then((res) => setReferencia({ data: res.data, loading: false, error: false, insuficiente: false }))
      .catch((erro) => {
        const insuficiente = erro.response?.status === 422;
        setReferencia({ data: null, loading: false, error: !insuficiente, insuficiente });
      });

    consumoAtipicoService.getStatusHoje()
      .then((res) => setStatusHoje({ data: res.data, loading: false, error: false }))
      .catch(() => setStatusHoje({ data: null, loading: false, error: true }));
  }

  useEffect(() => {
    medicaoService.getConsumoTotal()
      .then((res) => setLitros({ data: res.data, loading: false, error: false }))
      .catch(() => setLitros({ data: null, loading: false, error: true }));

    medicaoService.getConsumoCubicMeters()
      .then((res) => setM3({ data: res.data, loading: false, error: false }))
      .catch(() => setM3({ data: null, loading: false, error: true }));

    consumoAtipicoService.getHistorico(14)
      .then((res) => setHistorico({ data: res.data, loading: false, error: false }))
      .catch(() => setHistorico({ data: null, loading: false, error: true }));

    carregarContasEReferencia();
  }, []);

  const handleSubmitConta = async (event) => {
    event.preventDefault();
    setEnviando(true);
    setMensagemForm('');

    try {
      await contaAguaService.create({
        consumoM3: parseFloat(consumoM3Input),
        mesReferencia: mesReferenciaInput || undefined,
      });

      setConsumoM3Input('');
      setMesReferenciaInput('');
      setMensagemForm('Conta registrada com sucesso.');

      setContas({ data: [], loading: true, error: false });
      setReferencia({ data: null, loading: true, error: false, insuficiente: false });
      setStatusHoje({ data: null, loading: true, error: false });
      carregarContasEReferencia();
    } catch (erro) {
      console.error(erro);
      setMensagemForm('Não foi possível registrar a conta.');
    } finally {
      setEnviando(false);
    }
  };

  const handleDeleteConta = async (id) => {
    try {
      await contaAguaService.delete(id);
      setContas({ data: [], loading: true, error: false });
      setReferencia({ data: null, loading: true, error: false, insuficiente: false });
      setStatusHoje({ data: null, loading: true, error: false });
      carregarContasEReferencia();
    } catch (erro) {
      console.error(erro);
    }
  };

  return (
    <div>
      <PageHeader
        title="Consumo de água"
        description="Consulte o volume total já utilizado e cadastre suas contas de água anteriores para que o sistema calcule sua referência de consumo diário e identifique dias com consumo fora do padrão."
      />

      <div className="info-grid" style={{ maxWidth: 500, marginBottom: 36 }}>
        <InfoCard
          title="Consumo total"
          value={litros.data ? litros.data.totalLiters.toFixed(3) : '--'}
          unit="L"
          loading={litros.loading}
          error={litros.error}
          highlight
        />
        <InfoCard
          title="Consumo em m³"
          value={m3.data ? m3.data.totalCubicMeters.toFixed(3) : '--'}
          unit="m³"
          loading={m3.loading}
          error={m3.error}
        />
      </div>

      <section style={{ marginBottom: 36 }}>
        <h3 style={{ fontSize: 15, fontWeight: 700, color: '#1e293b', marginBottom: 14, textTransform: 'uppercase', letterSpacing: '.4px' }}>
          Consumo nos últimos 14 dias
        </h3>

        {historico.loading && <p style={{ color: '#64748b', fontSize: 14 }}>Carregando...</p>}
        {!historico.loading && historico.error && (
          <p style={{ color: '#ef4444', fontSize: 14 }}>Não foi possível carregar o histórico.</p>
        )}
        {!historico.loading && !historico.error && historico.data && (
          <ConsumoChart serie={historico.data.serie} referenciaDiariaLitros={historico.data.referenciaDiariaLitros} />
        )}
      </section>

      <section style={{ marginBottom: 36 }}>
        <h3 style={{ fontSize: 15, fontWeight: 700, color: '#1e293b', marginBottom: 14, textTransform: 'uppercase', letterSpacing: '.4px' }}>
          Referência diária
        </h3>

        {referencia.loading && <p style={{ color: '#64748b', fontSize: 14 }}>Carregando...</p>}

        {!referencia.loading && referencia.insuficiente && (
          <p style={{ color: '#64748b', fontSize: 14 }}>
            Cadastre pelo menos 3 contas de água anteriores para calcular sua referência de consumo diário.
          </p>
        )}

        {!referencia.loading && referencia.error && !referencia.insuficiente && (
          <p style={{ color: '#ef4444', fontSize: 14 }}>Não foi possível carregar a referência.</p>
        )}

        {!referencia.loading && referencia.data && (
          <div className="info-grid" style={{ maxWidth: 500 }}>
            <InfoCard
              title="Referência diária"
              value={referencia.data.referenciaDiariaM3.toFixed(3)}
              unit="m³/dia"
              loading={false}
              error={false}
            />
            {!statusHoje.loading && !statusHoje.error && statusHoje.data && (
              <InfoCard
                title={statusHoje.data.atipico ? 'Consumo de hoje (atípico)' : 'Consumo de hoje'}
                value={statusHoje.data.consumoHojeM3.toFixed(3)}
                unit="m³"
                loading={false}
                error={false}
                highlight={statusHoje.data.atipico}
              />
            )}
          </div>
        )}

        {!statusHoje.loading && !statusHoje.error && statusHoje.data?.atipico && (
          <p style={{ marginTop: 12, color: '#ef4444', fontSize: 14, fontWeight: 600 }}>
            ⚠ Consumo de hoje está {statusHoje.data.variacaoPercentual}% acima da sua referência diária.
          </p>
        )}
      </section>

      <section>
        <h3 style={{ fontSize: 15, fontWeight: 700, color: '#1e293b', marginBottom: 14, textTransform: 'uppercase', letterSpacing: '.4px' }}>
          Contas de água anteriores
        </h3>

        <form onSubmit={handleSubmitConta} style={{ display: 'flex', gap: 12, flexWrap: 'wrap', marginBottom: 20, alignItems: 'flex-end' }}>
          <div>
            <label style={{ display: 'block', fontSize: 13, fontWeight: 600, color: '#334155', marginBottom: 6 }}>
              Consumo (m³)
            </label>
            <input
              type="number"
              step="0.01"
              min="0.01"
              required
              value={consumoM3Input}
              onChange={(e) => setConsumoM3Input(e.target.value)}
              style={{ padding: 10, borderRadius: 10, border: '1px solid #d7dce3', width: 140 }}
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: 13, fontWeight: 600, color: '#334155', marginBottom: 6 }}>
              Mês de referência (opcional)
            </label>
            <input
              type="text"
              placeholder="Ex: 2026-08"
              value={mesReferenciaInput}
              onChange={(e) => setMesReferenciaInput(e.target.value)}
              style={{ padding: 10, borderRadius: 10, border: '1px solid #d7dce3', width: 160 }}
            />
          </div>
          <button
            type="submit"
            disabled={enviando}
            style={{ padding: '11px 20px', borderRadius: 10, border: 'none', background: '#334155', color: 'white', fontWeight: 600, cursor: 'pointer' }}
          >
            {enviando ? 'Salvando...' : 'Adicionar conta'}
          </button>
        </form>

        {mensagemForm && <p style={{ marginBottom: 16, fontSize: 14, color: '#334155' }}>{mensagemForm}</p>}

        {contas.loading && <p style={{ color: '#64748b', fontSize: 14 }}>Carregando...</p>}
        {!contas.loading && contas.error && <p style={{ color: '#ef4444', fontSize: 14 }}>Não foi possível carregar as contas.</p>}
        {!contas.loading && !contas.error && contas.data.length === 0 && (
          <p style={{ color: '#64748b', fontSize: 14 }}>Nenhuma conta cadastrada ainda.</p>
        )}

        {!contas.loading && !contas.error && contas.data.length > 0 && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {contas.data.map((conta) => (
              <div
                key={conta.id}
                style={{
                  background: 'white',
                  borderRadius: 12,
                  padding: '14px 18px',
                  boxShadow: '0 4px 14px rgba(15,23,42,.05)',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  fontSize: 14,
                  color: '#334155',
                }}
              >
                <span>{conta.mesReferencia || 'Sem mês informado'}</span>
                <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
                  <strong>{conta.consumoM3.toFixed(2)} m³</strong>
                  <button
                    onClick={() => handleDeleteConta(conta.id)}
                    title="Excluir registro"
                    style={{
                      background: 'transparent',
                      border: 'none',
                      cursor: 'pointer',
                      color: '#ef4444',
                      fontSize: 16,
                      padding: 4,
                      lineHeight: 1,
                    }}
                  >
                    ✕
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

export default Consumo;