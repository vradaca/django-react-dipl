import { useRef } from 'react'
import './App.css';
import Navbar from './components/Navbar';
import { Parallax, ParallaxLayer } from '@react-spring/parallax';
import bg1 from './bg_1.jpg';
import bg2 from './bg_2.jpg';
import bg3 from './bg_3.jpg';
import pic1 from './pic1.png';
import pic2 from './pic2.png';
import pic3 from './pic3.png';

function App() {

  const parallaxRef = useRef(null);

  const scrollToLayer = (index) => {
    if (parallaxRef.current) {
      parallaxRef.current.scrollTo(index);
    }
  };

  const redirectToDjango = () => {
    window.location.href = 'http://localhost:8000/authentication/register';  // redirect to signup page
  };

  return (
    <div className="App">
      <Navbar scrollToLayer={scrollToLayer} />
      <Parallax ref={parallaxRef} pages={4}>
        <ParallaxLayer offset={0} speed={0.5} factor={1.1}> 
          <header className="App-header">
            <div className="hero">
              <h1>Welcome to Budget Manager</h1>
                <p>Manage your finances easily and efficiently!</p>
                  <button className="cta-button" onClick={redirectToDjango}>Get Started</button>
            </div>
          </header>
        </ParallaxLayer>


        {/* About Section */}
        <ParallaxLayer offset={1} speed={0.5} factor={1} style={{ backgroundImage: `url(${bg1})`, backgroundSize: 'cover', }}>
          <section className="section about">
            <h2>About</h2>
            <p>Budget Manager is a comprehensive tool designed to help you manage your finances, track expenses, and achieve your financial goals.</p>
            <img style={{width: '600px', height: '400px'}}src={pic1} alt="About Budget Manager" />
          </section>
        </ParallaxLayer>

        {/* Services Section */}
        <ParallaxLayer offset = {2} speed = {0.5} factor = {1} style={{ backgroundImage: `url(${bg2})`, backgroundSize: 'cover', }}>
          <section className="section services">
            <h2>Our Services</h2>
            <p>We offer a range of services to help you stay on top of your finances, including budgeting tools, expense tracking, and financial planning.</p>
            <img src="https://via.placeholder.com/400x300" alt="Our Services" />
          </section>
        </ParallaxLayer>

        {/* Contact Section */}
        <ParallaxLayer offset = {3} speed = {0.5} factor = {1} style={{ backgroundImage: `url(${bg3})`, backgroundSize: 'cover', }}>
          <section className="section contact">
            <h2>Contact Us</h2>
            <p>If you have any questions or need assistance, feel free to reach out to us at support@budgetmanager.com.</p>
            <img src="https://via.placeholder.com/400x300" alt="Contact Us" />
          </section>
        </ParallaxLayer>

        <ParallaxLayer offset={0.8} speed={1.5} factor={2} style={{ backgroundImage: `url(${pic1})`, backgroundSize: 'cover', }} />
        <ParallaxLayer offset={1.8} speed={1.5} factor={2} style={{ backgroundImage: `url(${pic2})`, backgroundSize: 'cover', }} />
        <ParallaxLayer offset={2.8} speed={1.5} factor={2} style={{ backgroundImage: `url(${pic3})`, backgroundSize: 'cover', }} />
      </Parallax>
      
      <footer className="App-footer">
        <p>&copy; 2024. Budget Manager. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;