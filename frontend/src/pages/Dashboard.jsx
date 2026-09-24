import PageHeader from '../components/PageHeader';
import TopicCard from '../components/TopicCard';

function Dashboard() {
  return (
    <div>
      <PageHeader
        title="Visão geral"
        description="Bem-vindo ao Smart Flow. Sua ferramenta de controle de gastos e visualização de consumo de água residencial. Aqui você acompanha, em tempo real, o quanto de água está sendo utilizado na sua residência, entende o padrão de uso ao longo do tempo e tem uma estimativa clara de quanto isso representa no seu bolso."
      />

      <div className="topic-grid">
        <TopicCard
          title="Medições"
          description="Cada vez que a água passa pelo sensor, o Smart Flow registra automaticamente o volume utilizado, a duração daquele uso e o momento exato em que ele começou, formando um histórico detalhado de cada consumo, sem depender de leituras manuais."
        />
        <TopicCard
          title="Consumo"
          description="Veja o quanto de água já foi utilizado no total, tanto em litros quanto em metros cúbicos, a mesma unidade usada pela sua conta de água para comparar facilmente com o que está sendo cobrado."
        />
        <TopicCard
          title="Custo de água"
          description="A partir do consumo acumulado e da tarifa configurada, o Smart Flow estima quanto esse uso representa em reais, ajudando a identificar padrões de gasto antes mesmo da fatura chegar."
        />
      </div>
    </div>
  );
}

export default Dashboard;