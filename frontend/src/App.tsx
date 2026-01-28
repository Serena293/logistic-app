import './App.css'
import CalculatePage from './components/CalculatePage';
import { Routes, Route } from 'react-router-dom';
import Footer from './components/Footer';
import HomePage from './components/HomePage';
import MyNavbar from './components/MyNavbar'
import NotFoundPage from './components/NotFoundPage';

import 'bootstrap/dist/css/bootstrap.min.css';




function App() {
 return (
  <>
    <MyNavbar />

    <div className="main-content">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/calculate" element={<CalculatePage />} />
        <Route path="*" element={<NotFoundPage />} /> 
      </Routes>
    </div>

    <Footer />
  </>
);

}

export default App
