import { useRef } from 'react'
import './App.css';
import Navbar from './components/Navbar';
import { Parallax, ParallaxLayer } from '@react-spring/parallax';
import bg1 from './bg_1.jpg';
import bg2 from './bg_2.jpg';
import bg3 from './bg_3.jpg';
import pic1 from './pic1.jpg';
import pic2 from './pic2.jpg';
import pic3 from './pic3.jpg';
import darkBg from './dark_bg.jpg';

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
        <ParallaxLayer offset={0} speed={0.5} factor={1}> 
          <header className="App-header">
            <div className="hero">
              <h1>Welcome to Budget Manager</h1>
                <p>Manage your finances easily and efficiently!</p>
                  <button className="cta-button" onClick={redirectToDjango}>Get Started</button>
            </div>
          </header>
        </ParallaxLayer>


        {/* About Section */}
        <ParallaxLayer offset={1} speed={0.5} factor={1} style={{ backgroundImage: `url(${darkBg})`, }}>
          <section className="section about">
            <h2>About</h2>
            <p>Budget Manager is a comprehensive tool designed to help you manage your finances, track expenses, and achieve your financial goals.</p>
            <img src={pic1} alt="About Budget Manager" />
          </section>
        </ParallaxLayer>

        {/* Services Section */}
        <ParallaxLayer offset = {2} speed = {0.5} factor = {1} style={{ backgroundImage: `url(${darkBg})`, }}>
          <section className="section services">
            <h2>Our Services</h2>
            <p>We offer a range of services to help you stay on top of your finances, including budgeting tools, expense tracking, and financial planning.</p>
            <img src={pic2} alt="Our Services" />
          </section>
        </ParallaxLayer>

        {/* Contact Section */}
        <ParallaxLayer offset = {3} speed = {0.5} factor = {1} style={{ backgroundImage: `url(${darkBg})`, }}>
          <section className="section contact">
            <h2>Contact Us</h2>
            <p>If you have any questions or need assistance, feel free to reach out to us any way you can! 
              <br /><strong>Email:</strong> velkonrt115@gs.viser.edu.rs 
              <br /><strong>Github:</strong> https://github.com/vradaca
              <br /><strong>Linkedin:</strong> https://www.linkedin.com/in/veljko-rada%C4%8Da-535485265/ </p>
            <img src={pic3} alt="Contact Us" />
          </section>
        </ParallaxLayer>

        <ParallaxLayer offset={0.8} speed={1.5} factor={2} style={{ backgroundImage: `url(${bg1})`, backgroundSize: 'cover', }}/>
        <ParallaxLayer offset={1.8} speed={1.5} factor={2} style={{ backgroundImage: `url(${bg2})`, backgroundSize: 'cover', }} />
        <ParallaxLayer offset={2.8} speed={1.5} factor={2} style={{ backgroundImage: `url(${bg3})`, backgroundSize: 'cover', }} />
      </Parallax>
    </div>
  );
}

export default App;