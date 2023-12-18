import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { useGoogleLogin } from "@react-oauth/google";
import toast, { Toaster } from "react-hot-toast";
import { Formik, Field, Form } from 'formik';
import * as Yup from 'yup';
import UserContext from "./User";


function Login () {

    const [loginError, setLoginError] = useState("");
    const [reveal, setReveal] = useState("password");
    const loginWithGoogle = useGoogleLogin({
        onSuccess: (codeResponse) => {
            fetch("/api/v1/login_with_google", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(codeResponse)
            })
            .then(res => {
                if (res.ok) {
                    return res.json()
                } else {
                    toast(res.statusText)
                    return
                }
            })
            .then(data => {
                if (!data.access_token) {
                    setLoginError("Invalid Creditials");
                    localStorage.clear()
                    toast("Access Denied");
                    return
                }
                updateUser(data["user"]);
                localStorage.setItem("access_token", JSON.stringify(data.access_token))
                localStorage.setItem("refresh_token", JSON.stringify(data.refresh_token))
                toast("Thank you for being you!");
                navigate('/posts');
            })
            .catch(err => toast(err))
        },
        onError: (error) => toast("Error", error)
    })

    const navigate = useNavigate();

    const LoginSchema = Yup.object().shape({
        password: Yup.string()
          .required('Password Is Required For Access'),
        email: Yup.string().email('Invalid email').required('Required'),
      });

    const value = useContext(UserContext)
    const updateUser = value[0]
    if (value[2].user_name) {
        return (
            <>
                <h2>You are already logged in.</h2>
            </>
        )
    }

    const showPassword = reveal => {
        if (reveal === "password") {
            setReveal("text")
            console.log("reveal", reveal)
        } else {
            setReveal("password")
            console.log("reveal", reveal)
        }
    };

    return (
        <div>
            <Formik
                initialValues={{
                password: '',
                email: '',
                }}
                validationSchema={LoginSchema}
                onSubmit={async (values) => {
                    fetch("/api/v1/user_login", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify(values)
                    })
                    .then(res => {
                        if (res.ok) {
                            return res.json();
                        } else {
                            toast(res.statusText);
                        }
                    })
                    .then(data => {
                        if (!data || !data.access_token) {
                            setLoginError("Invalid Creditials");
                            localStorage.clear()
                            toast("Access Denied");
                        } else {
                            updateUser(data["user"]);
                            localStorage.setItem("access_token", JSON.stringify(data.access_token))
                            localStorage.setItem("refresh_token", JSON.stringify(data.refresh_token))
                            toast("Thank you for being you!");
                            navigate('/posts');
                        }
                        
                    })
                    .catch(err => {
                        toast(err)
                    })
                }}
            >

                {({ errors, touched }) => (
                    <Form
                        className="loginForm"
                    >
                        <h2>Login</h2>
                        <div>
                            <label htmlFor="email">Email</label>
                            <Field
                                id="email"
                                name="email"
                                placeholder="john@blaze.com"
                                type="email"
                                autoComplete="off"
                                className="loginInput"
                            />
                            {errors.email && touched.email ? (
                                <span> {errors.email}</span>
                            ) : null}
                        </div>

                        <div>
                            <label htmlFor="password">Password</label>
                            <Field
                                id="password"
                                name="password"
                                type={reveal}
                                placeholder="password"
                                autoComplete="off"
                                className="loginInput"
                            />
                            <Field
                                id="reveal"
                                name="reveal"
                                type="checkbox"
                                // checked={user.admin}
                                autoComplete="off"
                                onClick={() => showPassword(reveal)}
                            />
                            <label htmlFor="reveal">{
                                reveal === "password" ? "Click To Show Password" : "Unclick To Hide Password"
                            }</label>
                            {errors.password && touched.password ? (
                                <span> {errors.password}</span>
                            ) : null}
                        </div>

                        <div>{loginError}</div>

                        <button
                            type="submit"
                            className="submitBtn"
                        >Submit</button>

                        <button
                            type="button"
                            className="loginBtn"
                            onClick={() => loginWithGoogle()}
                        >Sign In With Google</button>   
                    </Form>
                )}

            </Formik>

            
        </div>
    )
};

export default Login;