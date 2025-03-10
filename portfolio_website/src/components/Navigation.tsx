import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const Nav = styled.nav`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  padding: 1rem 2rem;
  background: rgba(4, 7, 20, 0.8);
  backdrop-filter: blur(10px);
  z-index: 100;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Logo = styled(motion.div)`
  font-size: 1.5rem;
  font-weight: bold;
  color: ${props => props.theme.colors.accent};
  cursor: pointer;
`;

const NavLinks = styled.div`
  display: flex;
  gap: 2rem;
`;

const NavLink = styled(motion(Link))`
  color: ${props => props.theme.colors.text};
  text-decoration: none;
  font-size: 1.1rem;
  position: relative;
  
  &:after {
    content: '';
    position: absolute;
    width: 0;
    height: 2px;
    bottom: -5px;
    left: 0;
    background-color: ${props => props.theme.colors.accent};
    transition: width 0.3s ease;
  }
  
  &:hover:after {
    width: 100%;
  }
`;

const Navigation: React.FC = () => {
  const location = useLocation();
  
  return (
    <Nav>
      <Link to="/" style={{ textDecoration: 'none' }}>
        <Logo
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
        >
          🏰 Disney Data
        </Logo>
      </Link>
      <NavLinks>
        <NavLink 
          to="/"
          whileHover={{ y: -2 }}
          whileTap={{ y: 0 }}
        >
          Home
        </NavLink>
        <NavLink 
          to="/projects"
          whileHover={{ y: -2 }}
          whileTap={{ y: 0 }}
        >
          Projects
        </NavLink>
        <NavLink 
          to="/contact"
          whileHover={{ y: -2 }}
          whileTap={{ y: 0 }}
        >
          Contact
        </NavLink>
      </NavLinks>
    </Nav>
  );
};

export default Navigation; 