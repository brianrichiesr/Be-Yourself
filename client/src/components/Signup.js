import React from "react";
import { useNavigate } from "react-router-dom";
import { Formik, Field, Form } from 'formik';
import * as Yup from 'yup';


function Signup () {

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
                    await new Promise((r) => setTimeout(r, 500));
                    alert(JSON.stringify(values, null, 2));
                    fetch("/")
                    // navigate('/main')
                }}
            >
                <Form>
                <label htmlFor="user_name">First Name</label>
                <Field id="user_name" name="user_name" placeholder="John Blaze" />
        
                <label htmlFor="email">Email</label>
                <Field
                    id="email"
                    name="email"
                    placeholder="john@blaze.com"
                    type="email"
                />
        
                <label htmlFor="password">Last Name</label>
                <Field id="password" name="password" type="password" placeholder="password" />

                <button type="submit">Submit</button>
                </Form>
            </Formik>
        </div>
    )
};

export default Signup;