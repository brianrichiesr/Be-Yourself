import React from "react";
import { Link } from "react-router-dom";

function Footer() {
  return (
    <div id="footer">
      <div id="tagline">Made With 💙 By </div>
      <div id="blogDiv">
      <div id="author"></div>
      <Link
        to="https://brianrichiesr.hashnode.dev/"
        id="blog"
        target="_blank">
          Visit My Blog
      </Link>
      </div>
    </div>
  );
}

export default Footer;