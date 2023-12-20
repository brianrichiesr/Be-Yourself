import React, { useEffect, useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";
import { checkToken, postRefreshToken} from "./Authorize";
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
          .max(200, 'Too Long!')
          .required('Required'),
        image: Yup.string(),
      });
    
    const submitPost = (values) => {
      const user = user_data[2]
      values["user_id"] = user["id"]
      fetch("/api/v1/posts", {
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
              toast(data.errors);
              return
          }
          toast("Successful Submission!");
          navigate('/posts')

      })
      .catch(err => {
          toast(err)
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
              toast("Access Has Expired, Please Login Again")
            }
          })
          .then(data => {
            localStorage.setItem("access_token", JSON.stringify(data["access_token"]))
          })
          .catch(err => toast(err))
        }
      })
      .catch(err => toast(err))
      
      }, [])

    return (
        <div className="formBackgroundDiv">
            <Toaster />
            <h2 className="headerH2">Submit A Post</h2>
            <div className="formBox">
            <Formik
                initialValues={{
                  description: '',
                  image: '',
                  honoree_id: '',
                }}
                validationSchema={SubmissionSchema}
                onSubmit={async (values) => {
                    submitPost(values)
                }}
            >
                {({errors, touched}) => (
                    <Form
                      className="loginForm"
                    >
                        <div>
                            <label htmlFor="honoree_id">Honoree Id</label>
                            <Field
                              id="honoree_id"
                              name="honoree_id"
                              placeholder=""
                              type="number"
                              autoComplete="off"
                              className="loginInput"
                            />
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
                                autoComplete="off"
                                className="loginInput"
                            />
                            {errors.image && touched.image ? (
                                <span> {errors.image}</span>
                            ) : null}
                        </div>

                        <div>
                            <label htmlFor="description">Description</label>
                            <Field
                              as="textarea"
                              id="description"
                              name="description"
                              type="text"
                              placeholder="description 200 characters max."
                              autoComplete="off"
                              className="loginInput textArea"
                            />
                            {errors.description && touched.description ? (
                                <span> {errors.description}</span>
                            ) : null}
                        </div>
        
                        <div>{submissionError}</div>

                        <button
                          type="submit"
                          className="submitBtn"
                        >Submit</button>
                        
                    </Form>
                )}
            </Formik>
            </div>
        </div>
    )
};

export default Submission;