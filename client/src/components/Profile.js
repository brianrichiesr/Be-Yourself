import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import UserContext from "./User";
import { Formik, Field, Form } from 'formik';
import * as Yup from 'yup';

function Profile() {
    const value = useContext(UserContext)
    const [user, setUser] = useState(value[2])
    const [updateError, setUpdateError] = useState("")
    const updateUser = value[0]
    const navigate = useNavigate()

    const UpdateSchema = Yup.object().shape({
        user_name: Yup.string()
        .min(2, 'Too Short!')
        .max(50, 'Too Long!'),
        password: Yup.string()
        .min(2, 'Too Short!')
        .max(50, 'Too Long!'),
        email: Yup.string().email('Invalid email'),
    });
    const user_name = user.user_name || ""
    const email = user.email || ""
    const id = user.id || 0
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

      const deleteProfile = () => {
        const confirm = prompt("Are you sure you want to delete your profile? (y)es or (n)o?")
       if (confirm.toLowerCase() === "y" || confirm.toLowerCase() === "yes") {
        fetch(`/users/${id}`, {
            method: "DELETE"
        })
        .then(() => {
            updateUser({
                user_name: "",
                id: 0
            })
            localStorage.clear()
            navigate('/')
        })
       } else {
        console.log("No changes made")
       }
      }

      const updateProfile = (values) => {
        const confirm = prompt("Are you sure you want to update your profile? (y)es or (n)o?")
        if (confirm.toLowerCase() === "y" || confirm.toLowerCase() === "yes") {
            fetch(`/users/${id}`, {
                method: "PATCH",
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
                    setUpdateError(data.errors);
                    throw (data.errors);
                }
                updateUser(data["user"]);
                console.log("data = ", data)
                localStorage.setItem("access_token", JSON.stringify(data.access_token))
                alert("Your account has been updated!");
            })
            .catch(err => {
                alert(err)
            })
        }
      }
      
      useEffect(() => {
        const token = JSON.parse(localStorage.getItem('access_token'))
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
                setUser(data.user)
            })
            .catch(err => alert(err))
          }
        })
        .then(data => {
          if (data) {
            setUser(data.user)
          } 
        })
        .catch(err => alert(err))
        
        }, [])
    return (
        <div>
            <h2>Update Profile</h2>
            <Formik
                initialValues={{
                user_name: '',
                password: '',
                email: '',
                }}
                validationSchema={UpdateSchema}
                onSubmit={async (values) => {
                    updateProfile(values)
                }}
            >
                {({errors, touched}) => (
                    <Form>

                        <div>
                            <label htmlFor="user_name">User Name</label>
                            <Field id="user_name" name="user_name"
                            placeholder={user_name}
                            autoComplete="off" />
                            {errors.user_name && touched.user_name ? (
                                <span> {errors.user_name}</span>
                            ) : null}
                        </div>
                        
                        <div>
                            <label htmlFor="email">Email</label>
                            <Field
                                id="email"
                                name="email"
                                placeholder={email}
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
        
                        <button type="submit">Update</button>

                    </Form>
                )}
            </Formik>
            <button onClick={() => deleteProfile()}>Delete</button>
            <div>{updateError}</div>
        </div>
    )
};

export default Profile;