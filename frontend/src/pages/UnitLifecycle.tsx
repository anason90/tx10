import { useMemo, useState } from 'react';
import UnitCard, { UnitStatus } from '../components/UnitCard';
import styles from '../styles/Page.module.css';

const orderedStatuses: UnitStatus[] = ['design', 'available', 'reserved', 'sold', 'transferred'];

const UnitLifecycle = (): JSX.Element => {
  const [statusIndex, setStatusIndex] = useState(0);

  const status = orderedStatuses[statusIndex];

  const statusCopy = useMemo(() => {
    switch (status) {
      case 'design':
        return 'Architectural drawings are being finalised with land owner approvals.';
      case 'available':
        return 'Unit released to the sales pipeline and ready for reservation.';
      case 'reserved':
        return 'Reservation deposit received; completion pending final contracts.';
      case 'sold':
        return 'Sales contract executed; awaiting handover documentation.';
      case 'transferred':
        return 'Title deed transfer completed and archived.';
      default:
        return '';
    }
  }, [status]);

  const advance = (): void => {
    setStatusIndex((index) => Math.min(index + 1, orderedStatuses.length - 1));
  };

  return (
    <section className={styles.page}>
      <header>
        <h2>Unit lifecycle demo</h2>
        <p className={styles.lead}>{statusCopy}</p>
      </header>
      <UnitCard
        unitNumber="Penthouse 30"
        floor={30}
        area={280}
        status={status}
        salesRepresentative="Ayla Şen"
        owners={[{ name: 'Skyline Partners', share: 100 }]}
        ctaLabel={status === 'transferred' ? 'Process completed' : 'Advance to next step'}
        onAdvance={status === 'transferred' ? undefined : advance}
      />
      <ul className={styles.checklist}>
        {orderedStatuses.map((step, index) => (
          <li key={step}>
            <span className={styles.check} style={{ opacity: index <= statusIndex ? 1 : 0.2 }} />
            <span style={{ fontWeight: index === statusIndex ? 700 : 500 }}>
              {step.toUpperCase()}
            </span>
          </li>
        ))}
      </ul>
    </section>
  );
};

export default UnitLifecycle;
