import clsx from 'clsx';
import styles from './UnitCard.module.css';

export type UnitStatus = 'design' | 'available' | 'reserved' | 'sold' | 'transferred';

export interface OwnerShare {
  name: string;
  share: number;
}

export interface UnitCardProps {
  unitNumber: string;
  floor: number;
  area: number;
  status: UnitStatus;
  salesRepresentative?: string;
  owners?: OwnerShare[];
  ctaLabel?: string;
  onAdvance?: () => void;
}

const STATUS_META: Record<UnitStatus, { label: string; accent: string }> = {
  design: { label: 'Design', accent: styles.statusDesign },
  available: { label: 'Available', accent: styles.statusAvailable },
  reserved: { label: 'Reserved', accent: styles.statusReserved },
  sold: { label: 'Sold', accent: styles.statusSold },
  transferred: { label: 'Transferred', accent: styles.statusTransferred }
};

const UnitCard = ({
  unitNumber,
  floor,
  area,
  status,
  salesRepresentative,
  owners = [],
  ctaLabel = 'Advance status',
  onAdvance
}: UnitCardProps): JSX.Element => {
  const statusMeta = STATUS_META[status];

  return (
    <article className={styles.card}>
      <div className={styles.cardHeader}>
        <div>
          <h2 className={styles.unitNumber}>{unitNumber}</h2>
          <p className={styles.metaText}>Floor {floor} • {area} m²</p>
        </div>
        <span className={clsx(styles.statusBadge, statusMeta.accent)}>
          {statusMeta.label}
        </span>
      </div>

      <section className={styles.ownersSection}>
        <h3>Ownership</h3>
        {owners.length === 0 ? (
          <p className={styles.placeholder}>No shareholders defined yet.</p>
        ) : (
          <ul className={styles.ownerList}>
            {owners.map((owner) => (
              <li key={owner.name}>
                <span className={styles.ownerName}>{owner.name}</span>
                <span className={styles.ownerShare}>{owner.share.toFixed(1)}%</span>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className={styles.salesSection}>
        <h3>Sales representative</h3>
        <p className={styles.metaText}>
          {salesRepresentative ?? 'Not assigned'}
        </p>
      </section>

      {onAdvance && (
        <button
          type="button"
          className={styles.advanceButton}
          onClick={onAdvance}
        >
          {ctaLabel}
        </button>
      )}
    </article>
  );
};

export default UnitCard;
