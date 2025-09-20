import UnitCard, { OwnerShare, UnitStatus } from '../components/UnitCard';
import styles from '../styles/Page.module.css';

const mockUnits: Array<{
  unitNumber: string;
  floor: number;
  area: number;
  status: UnitStatus;
  salesRepresentative?: string;
  owners?: OwnerShare[];
}> = [
  {
    unitNumber: 'Tower A • 12B',
    floor: 12,
    area: 145,
    status: 'available',
    salesRepresentative: 'Selim Kaya',
    owners: [
      { name: 'Lotus Holding', share: 100 }
    ]
  },
  {
    unitNumber: 'Tower B • 05A',
    floor: 5,
    area: 110,
    status: 'reserved',
    salesRepresentative: 'Gül Han',
    owners: [
      { name: 'Mert Yıldız', share: 60 },
      { name: 'Nida Yıldız', share: 40 }
    ]
  }
];

const Dashboard = (): JSX.Element => {
  return (
    <section className={styles.page}>
      <header>
        <h2>Portfolio overview</h2>
        <p className={styles.lead}>
          Monitor live inventory, reservations and sales assignments across your project pipeline.
        </p>
      </header>
      <div className={styles.grid}>
        {mockUnits.map((unit) => (
          <UnitCard key={unit.unitNumber} {...unit} />
        ))}
      </div>
    </section>
  );
};

export default Dashboard;
