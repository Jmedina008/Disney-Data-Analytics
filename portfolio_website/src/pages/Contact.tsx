import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const ContactContainer = styled(motion.div)`
  min-height: 100vh;
  padding: 6rem 2rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

const ContactCard = styled(motion.div)`
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 3rem;
  max-width: 600px;
  width: 100%;
`;

const Title = styled(motion.h1)`
  color: ${props => props.theme.colors.accent};
  font-size: 2.5rem;
  margin-bottom: 2rem;
  text-align: center;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const InputGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const Label = styled.label`
  color: ${props => props.theme.colors.text};
  font-size: 1.1rem;
`;

const Input = styled.input`
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid ${props => props.theme.colors.primary}44;
  border-radius: 10px;
  padding: 0.8rem;
  color: ${props => props.theme.colors.text};
  font-size: 1rem;
  transition: border-color 0.3s ease;
  
  &:focus {
    outline: none;
    border-color: ${props => props.theme.colors.accent};
  }
`;

const TextArea = styled.textarea`
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid ${props => props.theme.colors.primary}44;
  border-radius: 10px;
  padding: 0.8rem;
  color: ${props => props.theme.colors.text};
  font-size: 1rem;
  min-height: 150px;
  resize: vertical;
  transition: border-color 0.3s ease;
  
  &:focus {
    outline: none;
    border-color: ${props => props.theme.colors.accent};
  }
`;

const SubmitButton = styled(motion.button)`
  background: ${props => props.theme.colors.primary};
  color: ${props => props.theme.colors.text};
  border: none;
  border-radius: 10px;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background 0.3s ease;
  
  &:hover {
    background: ${props => props.theme.colors.accent};
  }
`;

const SocialLinks = styled.div`
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 2rem;
`;

const SocialLink = styled(motion.a)`
  color: ${props => props.theme.colors.text};
  text-decoration: none;
  font-size: 1.1rem;
  
  &:hover {
    color: ${props => props.theme.colors.accent};
  }
`;

const Contact: React.FC = () => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission
  };

  return (
    <ContactContainer
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <ContactCard
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <Title>Let's Create Magic Together ✨</Title>
        <Form onSubmit={handleSubmit}>
          <InputGroup>
            <Label>Name</Label>
            <Input type="text" required />
          </InputGroup>
          <InputGroup>
            <Label>Email</Label>
            <Input type="email" required />
          </InputGroup>
          <InputGroup>
            <Label>Message</Label>
            <TextArea required />
          </InputGroup>
          <SubmitButton
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            type="submit"
          >
            Send Message
          </SubmitButton>
        </Form>
        <SocialLinks>
          <SocialLink
            href="https://github.com/Jmedina008"
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ y: -3 }}
          >
            GitHub
          </SocialLink>
          <SocialLink
            href="https://linkedin.com/in/yourprofile"
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ y: -3 }}
          >
            LinkedIn
          </SocialLink>
        </SocialLinks>
      </ContactCard>
    </ContactContainer>
  );
};

export default Contact; 