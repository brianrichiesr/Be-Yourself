import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";
import { checkToken, postRefreshToken} from "./Authorize";
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
    const id = user.id || 0;

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
            toast("No changes made")
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
                    toast(data.errors);
                    return
                }
                updateUser(data["user"]);
                localStorage.setItem("access_token", JSON.stringify(data.access_token))
                toast("Your account has been updated!");
            })
            .catch(err => {
                toast(err)
            })
        }
    }

    const get_user = (id) => {
        fetch(`/users/${id}`)
        .then(res => {
            if (res.ok) {
                return res.json()
            } else {
                toast(res.statusText)
                return
            }
        })
        .catch(err => toast(err))
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
                return
                }
            })
            .then(data => {
                localStorage.setItem("access_token", JSON.stringify(data["access_token"]))
                get_user(data.user.id)
                setUser(data.user)
            })
            .catch(err => toast(err))
            }
        })
        .then(data => {
            if (data) {
                get_user(data.user.id)
                setUser(data.user)
            } 
        })
        .catch(err => toast(err))
        
    }, [])
    return (
        <div>
            <Toaster />
            <h2>Profile</h2>
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