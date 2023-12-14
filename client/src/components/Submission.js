import React, { useEffect, useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Formik, Field, Form } from 'formik';
import * as Yup from 'yup';
import UserContext from "./User";

function Submission () {

    const [submissionError, setSubmissionError] = useState("")

    const navigate = useNavigate();

    const user_data = useContext(UserContext)


    const SubmissionSchema = Yup.object().shape({
        honoree_id: Yup.number()
          .required('Required'),
        description: Yup.string()
          .min(2, 'Too Short!')
          .max(500, 'Too Long!')
          .required('Required'),
        image: Yup.string(),
      });
    
    const submitPost = (values) => {
      // const updateUser = user_data[0]
      const user = user_data[2]
      values["user_id"] = user["id"]
      console.log("values", values)
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
          console.log("submission -", data)
          alert("Successful Submission!");
      })
      .catch(err => {
          alert(err)
      })
    }

    const checkToken = (acc_token) => fetch("/check_token", {
      headers: {
        "Authorization": `Bearer ${acc_token}`
      }
    })
  
    const postRefreshToken = (ref_token) => {
      return fetch("/refresh", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${ref_token}`
        }
      })
    }
    
    useEffect(() => {
      const token = JSON.parse(localStorage.getItem('access_token'))
      if (!token) {
        localStorage.clear()
        navigate('/')
        return
      }
      const refresh_token = JSON.parse(localStorage.getItem('refresh_token'))
      checkToken(token)
  
      checkToken(token)
      .then(res => {
        if (res.ok) {
          return res.json()
        } else if (res.status === 401) {
          postRefreshToken(refresh_token)
          .then(resp => {
            if (resp.ok) {
              return resp.json()
            } else {
              localStorage.clear()
              alert("Access Has Expired, Please Login Again")
            }
          })
          .then(data => {
            localStorage.setItem("access_token", JSON.stringify(data["access_token"]))
          })
          .catch(err => alert(err))
        }
      })
      .catch(err => alert(err))
      
      }, [])

    return (
        <div>
            <h2>Submit A Post</h2>
            <Formik
                initialValues={{
                  description: '',
                  image: '',
                  honoree_id: '',
                }}
                validationSchema={SubmissionSchema}
                onSubmit={async (values) => {
                  // debugger
                    submitPost(values)
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