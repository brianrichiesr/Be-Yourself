import React from "react";

function Landing() {
  localStorage.clear()
  return (
    <div>
      <div id="heroBanner">
        <div className="heroDiv"><span className="altColorOne">Be</span>lieve In</div>
        <div className="heroDiv alignRight"><span className="altColorTwo">You</span>rself</div>
      </div>
      <main>
        <div id="motto"><span>Love</span> <span>Support</span> <span>Celebrate</span></div>
        <section className="imgBlock">
          <div className="imgContainer img-1"></div>
          <div className="imgText">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</div>
        </section>
        <section className="supportText">
          <div>Give The <span>Love</span> You Can</div>
          <div className="alignRight">Gain The Support You <span>Need</span></div>
          </section>
          <section className="imgBlock-2">
            <div className="imgBlock-2-container">
            <div className="imgContainer imgContainer-2 img-2"></div>
            <div className="imgText imgText-2">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</div>
            </div>
            <div className="imgBlock-2-container columnReverse">
            <div className="imgContainer imgContainer-2 img-3"></div>
            <div className="imgText imgText-2">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</div>
            </div>
          </section>
          <section className="supportText">
            <div className="center">Where Everyday Heroes Are <span>Heroes</span> Everyday</div>
          </section>
          <section className="imgBlock-3">
            <div className="imgContainer img-4"></div>
            <div className="imgText fullWidth">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</div>
          </section>
      </main>
    </div>
  );
}

export default Landing;