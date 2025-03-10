import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const ProjectsContainer = styled(motion.div)`
  min-height: 100vh;
  padding: 6rem 2rem 2rem;
`;

const ProjectsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
`;

const ProjectCard = styled(motion.div)`
  background: rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  padding: 2rem;
  position: relative;
  overflow: hidden;
  
  &:before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      45deg,
      ${props => props.theme.colors.primary}22,
      ${props => props.theme.colors.accent}11
    );
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  &:hover:before {
    opacity: 1;
  }
`;

const ProjectTitle = styled.h2`
  color: ${props => props.theme.colors.accent};
  margin-bottom: 1rem;
  font-size: 1.8rem;
`;

const ProjectDescription = styled.p`
  color: ${props => props.theme.colors.secondary};
  margin-bottom: 1.5rem;
  line-height: 1.6;
`;

const TechStack = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
`;

const TechTag = styled(motion.span)`
  background: ${props => props.theme.colors.primary}33;
  color: ${props => props.theme.colors.text};
  padding: 0.3rem 0.8rem;
  border-radius: 15px;
  font-size: 0.9rem;
`;

const projects = [
  {
    title: "Disney+ Content Analysis",
    description: "Analyzing streaming patterns, content performance, and user behavior to optimize the Disney+ platform experience.",
    tech: ["Python", "Pandas", "Scikit-learn", "Streamlit", "Plotly"],
    link: "/projects/disney-plus"
  },
  {
    title: "Theme Park Experience Optimizer",
    description: "AI-powered solution for optimizing wait times, crowd flow, and visitor experience in Disney theme parks.",
    tech: ["Python", "TensorFlow", "FastAPI", "PostgreSQL", "React"],
    link: "/projects/theme-park"
  },
  {
    title: "Character Recognition AI",
    description: "Deep learning model that identifies Disney characters from images and analyzes their visual features.",
    tech: ["PyTorch", "Computer Vision", "CNN", "Transfer Learning"],
    link: "/projects/character-ai"
  },
  {
    title: "Box Office Predictor",
    description: "Machine learning model that predicts box office performance for upcoming Disney releases.",
    tech: ["Python", "XGBoost", "Time Series", "NLP"],
    link: "/projects/box-office"
  },
  {
    title: "Social Media Sentiment Analyzer",
    description: "Real-time analysis of social media sentiment about Disney properties and brands.",
    tech: ["Python", "BERT", "FastAPI", "React", "D3.js"],
    link: "/projects/sentiment"
  }
];

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.2
    }
  }
};

const cardVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: {
      duration: 0.5
    }
  }
};

const Projects: React.FC = () => {
  return (
    <ProjectsContainer
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <ProjectsGrid>
        {projects.map((project, index) => (
          <ProjectCard
            key={index}
            variants={cardVariants}
            whileHover={{ y: -10 }}
            whileTap={{ scale: 0.98 }}
          >
            <ProjectTitle>{project.title}</ProjectTitle>
            <ProjectDescription>{project.description}</ProjectDescription>
            <TechStack>
              {project.tech.map((tech, techIndex) => (
                <TechTag
                  key={techIndex}
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                >
                  {tech}
                </TechTag>
              ))}
            </TechStack>
          </ProjectCard>
        ))}
      </ProjectsGrid>
    </ProjectsContainer>
  );
};

export default Projects; 