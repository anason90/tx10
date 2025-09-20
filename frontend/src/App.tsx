import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import ProjectDetail from './pages/ProjectDetail';
import UnitLifecycle from './pages/UnitLifecycle';
import styles from './styles/App.module.css';

const App = (): JSX.Element => {
  return (
    <BrowserRouter>
      <div className={styles.appShell}>
        <header className={styles.header}>
          <h1>Real Estate Lifecycle Portal</h1>
          <p className={styles.subtitle}>
            Track land ownership, project progress and unit sales with clarity.
          </p>
        </header>
        <nav className={styles.navigation}>
          <NavLink to="/" end className={({ isActive }) => isActive ? styles.activeLink : ''}>
            Dashboard
          </NavLink>
          <NavLink to="/projects" className={({ isActive }) => isActive ? styles.activeLink : ''}>
            Projects
          </NavLink>
          <NavLink to="/units" className={({ isActive }) => isActive ? styles.activeLink : ''}>
            Unit Lifecycle
          </NavLink>
        </nav>
        <main className={styles.mainContent}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/projects" element={<ProjectDetail />} />
            <Route path="/units" element={<UnitLifecycle />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
};

export default App;
