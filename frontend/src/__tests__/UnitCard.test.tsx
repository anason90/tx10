import { describe, expect, it, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import UnitCard from '../components/UnitCard';

describe('UnitCard', () => {
  it('renders unit information and ownership', () => {
    render(
      <UnitCard
        unitNumber="A1"
        floor={5}
        area={120}
        status="reserved"
        salesRepresentative="Selim Kaya"
        owners={[
          { name: 'Ayşe Demir', share: 60 },
          { name: 'Mehmet Demir', share: 40 }
        ]}
      />
    );

    expect(screen.getByText('A1')).toBeInTheDocument();
    expect(screen.getByText('Floor 5 • 120 m²')).toBeInTheDocument();
    expect(screen.getByText('Reserved')).toBeInTheDocument();
    expect(screen.getByText('Selim Kaya')).toBeInTheDocument();
    expect(screen.getByText('Ayşe Demir')).toBeInTheDocument();
  });

  it('fires advance callback when button clicked', async () => {
    const handler = vi.fn();
    const user = userEvent.setup();

    render(
      <UnitCard
        unitNumber="A2"
        floor={8}
        area={150}
        status="available"
        salesRepresentative="Gül Han"
        onAdvance={handler}
      />
    );

    await user.click(screen.getByRole('button', { name: /advance/i }));
    expect(handler).toHaveBeenCalledTimes(1);
  });
});
