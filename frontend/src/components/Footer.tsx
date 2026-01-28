import { Container } from "react-bootstrap";

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer>
      <Container
        fluid
        className="bg-primary text-light text-center py-3"
      >
        &copy; {currentYear} All rights reserved.
      </Container>
    </footer>
  );
};

export default Footer;
