import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";
import { Formik, Field, Form } from 'formik';
import * as Yup from 'yup';
import UserContext from "./User";


function Signup () {

    const [signupError, setSignupError] = useState("")

    const navigate = useNavigate();

    const value = useContext(UserContext)
    const updateUser = value[0]

    const SignupSchema = Yup.object().shape({
        user_name: Yup.string()
          .min(2, 'Too Short!')
          .max(50, 'Too Long!')
          .required('Required'),
        password: Yup.string()
          .min(2, 'Too Short!')
          .max(50, 'Too Long!')
          .required('Required'),
        email: Yup.string().email('Invalid email').required('Required'),
      });

    return (
        <div>
            <Toaster />
            <Formik
                initialValues={{
                user_name: '',
                password: '',
                email: '',
                }}
                validationSchema={SignupSchema}
                onSubmit={async (values) => {
                    fetch("/api/v1/users", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify(values)
                    })
                    .then(res => {
                        return res.json();
                    })
                    .then(data => {
                        if (data.errors) {
                            setSignupError(data.errors);
                            throw (data.errors);
                        }
                        updateUser(data["user"]);
                        localStorage.setItem("access_token", JSON.stringify(data.access_token))
                        toast("Thank you for being you!");
                        navigate('/posts');
                    })
                    .catch(err => {
                        toast(err)
                    })
                    // navigate('/main')
                }}
            >
                {({errors, touched}) => (
                    <Form
                        className="loginForm"
                    >
                        <h2>Sign Up</h2>
                        <div>
                            <label htmlFor="user_name">User Name</label>
                            <Field
                                id="user_name"
                                name="user_name"
                                placeholder="John Blaze"
                                autoComplete="off"
                                className="loginInput"
                            />
                            {errors.user_name && touched.user_name ? (
                                <span> {errors.user_name}</span>
                            ) : null}
                        </div>
                        
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
                                type="password"
                                placeholder="password"
                                autoComplete="off"
                                className="loginInput"
                            />
                            {errors.password && touched.password ? (
                                <span> {errors.password}</span>
                            ) : null}
                        </div>
        
                        <button
                            className="submitBtn"
                            type="submit"
                        >Submit</button>

                    </Form>
                )}
            </Formik>
            <div>{signupError}</div>
        </div>
    )
};

export default Signup;