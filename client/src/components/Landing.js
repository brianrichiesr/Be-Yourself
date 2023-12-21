import React from "react";

function Landing() {
  return (
    <div id="landing">
      <div id="heroBanner">
        <div className="heroDiv"><span className="altColorOne">Be</span>lieve In</div>
        <div className="heroDiv alignRight"><span className="altColorTwo">You</span>rself</div>
      </div>
      <main>
        <div id="motto"><span>Love</span> <span>Support</span> <span>Celebrate</span></div>
        <section className="imgBlock">
          <div className="imgContainer img-1"></div>
          <div className="imgText">"The best and most beautiful things in this world cannot be seen or even heard, but must be felt with the heart." — Helen Keller</div>
        </section>
        <section className="supportText">
          <div>Give The <span>Love</span> You Can</div>
          <div className="alignRight">Gain The Support You <span>Need</span></div>
          </section>
          <section className="imgBlock-2">
            <div className="imgBlock-2-container">
            <div className="imgContainer imgContainer-2 img-2"></div>
            <div className="imgText imgText-2">"Where there is love there is life."<p> — Mahatma Gandhi</p></div>
            </div>
            <div className="imgBlock-2-container columnReverse">
            <div className="imgContainer imgContainer-2 img-3"></div>
            <div className="imgText imgText-2">"I can't promise to fix all your problems, but I can promise you will never have to face them alone." — Anonymous</div>
            </div>
          </section>
          <section className="supportText">
            <div className="center">Where Everyday Heroes Are <span>Heroes</span> Everyday</div>
          </section>
          <section className="imgBlock-3">
            <div className="imgContainer img-4"></div>
            <div className="imgText fullWidth">"The greatest happiness of life is the conviction that we are loved; loved for ourselves, or rather, loved in spite of ourselves." — Victor Hugo</div>
          </section>
      </main>
    </div>
  );
}

export default Landing;