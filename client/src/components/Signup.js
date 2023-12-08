import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Formik, Field, Form } from 'formik';
import * as Yup from 'yup';


function Signup () {

    const [signupError, setSignupError] = useState("")

    const navigate = useNavigate();

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
            <h2>Sign Up</h2>
            <Formik
                initialValues={{
                user_name: '',
                password: '',
                email: '',
                }}
                validationSchema={SignupSchema}
                onSubmit={async (values) => {
                    fetch("/users", {
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
                        alert("Thank you for being you!");
                        navigate('/main');
                    })
                    .catch(err => {
                        alert(err)
                    })
                    // navigate('/main')
                }}
            >
                {({errors, touched}) => (
                    <Form>

                        <div>
                            <label htmlFor="user_name">User Name</label>
                            <Field id="user_name" name="user_name" placeholder="John Blaze" autoComplete="off" />
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
                            />
                            {errors.email && touched.email ? (
                                <span> {errors.email}</span>
                            ) : null}
                        </div>

                        <div>
                            <label htmlFor="password">Password</label>
                            <Field id="password" name="password" type="password" placeholder="password" autoComplete="off" />
                            {errors.password && touched.password ? (
                                <span> {errors.password}</span>
                            ) : null}
                        </div>
        
                        <button type="submit">Submit</button>

                    </Form>
                )}
            </Formik>
            <div>{signupError}</div>
        </div>
    )
};

export default Signup;