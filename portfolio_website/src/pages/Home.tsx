import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { Canvas } from '@react-three/fiber';
import { Stars } from '@react-three/drei';

const HomeContainer = styled(motion.div)`
  min-height: 100vh;
  padding: 6rem 2rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  overflow: hidden;
`;

const HeroSection = styled(motion.div)`
  text-align: center;
  max-width: 800px;
  margin: 2rem auto;
  z-index: 1;
`;

const Title = styled(motion.h1)`
  font-size: 3.5rem;
  margin-bottom: 1.5rem;
  color: ${props => props.theme.colors.text};
  font-family: ${props => props.theme.fonts.title};
  
  span {
    color: ${props => props.theme.colors.accent};
  }
`;

const Subtitle = styled(motion.p)`
  font-size: 1.5rem;
  margin-bottom: 2rem;
  color: ${props => props.theme.colors.secondary};
  line-height: 1.6;
`;

const StarsCanvas = styled(Canvas)`
  position: absolute !important;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
`;

const ProjectsGrid = styled(motion.div)`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  width: 100%;
  max-width: 1200px;
  margin-top: 4rem;
  z-index: 1;
`;

const ProjectCard = styled(motion.div)`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 2rem;
  cursor: pointer;
  
  h3 {
    color: ${props => props.theme.colors.accent};
    margin-bottom: 1rem;
  }
  
  p {
    color: ${props => props.theme.colors.secondary};
  }
`;

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.3
    }
  }
};

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: {
      duration: 0.5
    }
  }
};

const Home: React.FC = () => {
  return (
    <HomeContainer
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <StarsCanvas>
        <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade />
      </StarsCanvas>
      
      <HeroSection>
        <Title
          variants={itemVariants}
        >
          Welcome to <span>Disney Data</span> Magic
        </Title>
        <Subtitle
          variants={itemVariants}
        >
          Where data science meets the wonder of Disney. Explore projects that bring
          analytics magic to entertainment, theme parks, and storytelling.
        </Subtitle>
      </HeroSection>

      <ProjectsGrid>
        {[
          {
            title: "Disney+ Analytics",
            description: "Analyzing streaming patterns and content performance"
          },
          {
            title: "Theme Park Optimizer",
            description: "AI-powered solutions for park operations"
          },
          {
            title: "Character Recognition",
            description: "Deep learning for Disney character identification"
          }
        ].map((project, index) => (
          <ProjectCard
            key={index}
            variants={itemVariants}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <h3>{project.title}</h3>
            <p>{project.description}</p>
          </ProjectCard>
        ))}
      </ProjectsGrid>
    </HomeContainer>
  );
};

export default Home; 