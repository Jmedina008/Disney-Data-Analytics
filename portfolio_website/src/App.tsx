import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import styled, { ThemeProvider } from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';

// Components
import Navigation from './components/Navigation';
import Home from './pages/Home';
import Projects from './pages/Projects';
import Contact from './pages/Contact';

// Theme
const theme = {
  colors: {
    primary: '#0063e5',    // Disney+ blue
    secondary: '#f9f9f9',  // Light gray
    accent: '#ffd500',     // Disney yellow
    background: '#040714', // Dark blue/black
    text: '#ffffff'
  },
  fonts: {
    main: "'Avenir Next', sans-serif",
    title: "'Avenir Next Bold', sans-serif"
  }
};

// Styled Components
const AppContainer = styled.div`
  min-height: 100vh;
  background-color: ${props => props.theme.colors.background};
  color: ${props => props.theme.colors.text};
  font-family: ${props => props.theme.fonts.main};
`;

const WandCursor = styled(motion.div)`
  position: fixed;
  width: 20px;
  height: 20px;
  pointer-events: none;
  z-index: 9999;
  background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 70%);
  mix-blend-mode: screen;
`;

const App: React.FC = () => {
  const [mousePosition, setMousePosition] = React.useState({ x: 0, y: 0 });

  React.useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <Router>
        <AppContainer>
          <WandCursor
            animate={{ x: mousePosition.x - 10, y: mousePosition.y - 10 }}
            transition={{ type: "spring", mass: 0.1, stiffness: 100 }}
          />
          <Navigation />
          <AnimatePresence mode="wait">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/projects" element={<Projects />} />
              <Route path="/contact" element={<Contact />} />
            </Routes>
          </AnimatePresence>
        </AppContainer>
      </Router>
    </ThemeProvider>
  );
};

export default App; 