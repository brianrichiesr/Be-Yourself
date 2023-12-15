import React from "react";

  /* Function that will send current access JWT to server to check validity and if expired */
  const checkToken = (acc_token) => fetch("/check_token", {
    headers: {
      "Authorization": `Bearer ${acc_token}`
    }
  });
  /* Function that will send current refresh JWT to server to check validity and if expired
    If refresh still valid, will return a new access access token */
  const postRefreshToken = (ref_token) => fetch("/refresh", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${ref_token}`
    }
  });

export { checkToken, postRefreshToken};