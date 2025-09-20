import styles from '../styles/Page.module.css';

const milestones = [
  {
    title: 'Planning approval',
    description: 'Urban planning permit secured and land ownership verified.'
  },
  {
    title: 'Construction phase',
    description: 'Ground works underway with monthly progress inspections.'
  },
  {
    title: 'Sales launch',
    description: 'Primary inventory released to sales representatives with allocations.'
  },
  {
    title: 'Handover',
    description: 'Title transfer packages prepared for sold units.'
  }
];

const ProjectDetail = (): JSX.Element => {
  return (
    <section className={styles.page}>
      <header>
        <h2>Project journey</h2>
        <p className={styles.lead}>
          Highlight the critical steps required to move a development from planning to customer handover.
        </p>
      </header>
      <div className={styles.timeline}>
        {milestones.map((milestone) => (
          <div key={milestone.title} className={styles.timelineStage}>
            <h3>{milestone.title}</h3>
            <p>{milestone.description}</p>
          </div>
        ))}
      </div>
      <div className={styles.alert}>
        Tip: Align project status updates in the API with the stakeholder check-ins captured here.
      </div>
    </section>
  );
};

export default ProjectDetail;
