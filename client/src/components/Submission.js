import React, { useState, useContext } from "react";
// import { useNavigate } from "react-router-dom";
import { Formik, Field, Form } from 'formik';
import * as Yup from 'yup';
import UserContext from "./User";

// user_id
// description
// image
// honoree_id


function Submission () {

    const [submissionError, setSubmissionError] = useState("")

    // const navigate = useNavigate();

    const value = useContext(UserContext)
    // const updateUser = value[0]
    const user = value[2]

    const SubmissionSchema = Yup.object().shape({
        honoree_id: Yup.number()
          .required('Required'),
        description: Yup.string()
          .min(2, 'Too Short!')
          .max(500, 'Too Long!')
          .required('Required'),
        image: Yup.string(),
      });

    return (
        <div>
            <h2>Sign Up</h2>
            <Formik
                initialValues={{
                  user_id: user.user_id || 0,
                  description: '',
                  image: '',
                  honoree_id: '',
                }}
                validationSchema={SubmissionSchema}
                onSubmit={async (values) => {
                    fetch("/posts", {
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
                            setSubmissionError(data.errors);
                            throw (data.errors);
                        }
                        console.log("data = ", data)
                        alert("Thank you for being you!");
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
                            <label htmlFor="honoree_id">Honoree Id</label>
                            <Field id="honoree_id" name="honoree_id" placeholder="" type="number" autoComplete="off" />
                            {errors.honoree_id && touched.honoree_id ? (
                                <span> {errors.honoree_id}</span>
                            ) : null}
                        </div>
                        
                        <div>
                            <label htmlFor="image">Image Url</label>
                            <Field
                                id="image"
                                name="image"
                                placeholder="john@blaze.com"
                                // type="text"
                                autoComplete="off"
                            />
                            {errors.image && touched.image ? (
                                <span> {errors.image}</span>
                            ) : null}
                        </div>

                        <div>
                            <label htmlFor="description">Description</label>
                            <Field as="textarea" id="description" name="description" type="text" placeholder="description" autoComplete="off" />
                            {errors.description && touched.description ? (
                                <span> {errors.description}</span>
                            ) : null}
                        </div>
        
                        <button type="submit">Submit</button>

                    </Form>
                )}
            </Formik>
            <div>{submissionError}</div>
        </div>
    )
};

export default Submission;