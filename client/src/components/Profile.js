import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";
import { checkToken, postRefreshToken} from "./Authorize";
import UserContext from "./User";
import { Formik, Field, Form } from 'formik';
import * as Yup from 'yup';
import { v4 as uuid } from 'uuid';

function Profile() {
    const value = useContext(UserContext)
    const [user, setUser] = useState(value[2])
    const [updateError, setUpdateError] = useState("");
    const [connectionError, setConnectionError] = useState("");
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
    const ConnectionSchema = Yup.object().shape({
        receiver_id: Yup.number()
        .min(1, 'Number Too Low!')
        .required('Please Select A User Id'),
    });
    const user_name = user.user_name || ""
    const email = user.email || ""
    const id = user.id || 0;

    const deleteProfile = () => {
        const confirm = prompt("Are you sure you want to delete your profile? (y)es or (n)o?")
        if (confirm.toLowerCase() === "y" || confirm.toLowerCase() === "yes") {
            fetch(`/api/v1/users/${id}`, {
                method: "DELETE"
            })
            updateUser({
                user_name: "",
                id: 0
            })
            localStorage.clear()
            navigate('/')
        } else {
            toast("No changes made")
        }
    }

    const updateProfile = (values) => {
        const confirm = prompt("Are you sure you want to update your profile? (y)es or (n)o?")
        if (confirm.toLowerCase() === "y" || confirm.toLowerCase() === "yes") {
            fetch(`/api/v1/users/${id}`, {
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

    const get_user = (id, load=true) => {
        fetch(`/api/v1/users/${id}`)
        .then(res => {
            if (res.ok) {
                return res.json()
            } else {
                toast(res.statusText)
                return
            }
        })
        .then(data => {
            if (load) {
                setUser(data);
            }
        })
        .catch(err => toast(err))
    }

    const deleteConnectionRequestSent = (sender_id, receiver_id) => {
        const confirm = prompt("Are you sure you want to delete this request? (y)es or (n)o?")
        if (confirm.toLowerCase() === "y" || confirm.toLowerCase() === "yes") {
            fetch(`/api/v1/user_connections_sender/${sender_id}/${receiver_id}`, {
                method: "DELETE"
            })
            .then(() => {
                toast("Request Deleted");
                get_user(id);
            })
            .catch(err => {
                toast(err);
            })
        } else {
            toast("No changes made")
        }
    }

    const deleteConnectionRequestReceived = (sender_id, receiver_id) => {
        const confirm = prompt("Are you sure you want to refuse this connection? (y)es or (n)o?")
        if (confirm.toLowerCase() === "y" || confirm.toLowerCase() === "yes") {
            fetch(`/api/v1/user_connections_sender/${sender_id}/${receiver_id}`, {
                method: "DELETE"
            })
            .then(() => {
                toast("Request Refused");
                get_user(id);
            })
            .catch(err => {
                toast(err);
            })
        } else {
            toast("No changes made")
        }
    }

    const deleteConnection = (sender_id, receiver_id) => {
        const confirm = prompt("Are you sure you want to delete this connection? (y)es or (n)o?")
        if (confirm.toLowerCase() === "y" || confirm.toLowerCase() === "yes") {
            fetch(`/api/v1/user_connections_sender/connection/${sender_id}/${receiver_id}`, {
                method: "DELETE"
            })
            .then(() => {
                toast("Connection Deleted");
                get_user(id);
            })
            .catch(err => {
                toast(err);
            })
        } else {
            toast("No changes made")
        }
    }

    const acceptConnection = (sender_id, receiver_id) => {
        const confirm = prompt("Are you sure you want to accept this request? (y)es or (n)o?")
        if (confirm.toLowerCase() === "y" || confirm.toLowerCase() === "yes") {
            fetch(`/api/v1/user_connections_receiver/${sender_id}/${receiver_id}`, {
                method: "PATCH"
            })
            .then(data => {
                toast("Request Accepted");
                get_user(id);
            })
            .catch(err => {
                toast(err);
            })
        } else {
            toast("No changes made")
        }
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
            })
            .catch(err => toast(err))
        }
    })
    .then(data => {
        if (data) {
            get_user(data.user.id)
            } 
        })
        .catch(err => toast(err))
        
    }, [])
    
    

    return (
        <div className="formBackgroundDiv">
            <Toaster />
            <div id="h2Div">
            <h2 className="headerH2">Profile</h2>
            <h2 className="headerH2 leftH2">Connections:</h2>
            </div>
            <div id="profileContainer">
                <div className="formBox profileBoxRight">
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
                            <Form
                                className="loginForm"
                            >
                                <div>
                                    <label htmlFor="user_name">User Name</label>
                                    <Field
                                        id="user_name"
                                        name="user_name"
                                        placeholder={user_name}
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
                                        placeholder={email}
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
                                    type="submit"
                                    className="submitBtn"
                                >Update</button>


                            </Form>
                        )}
                    </Formik>
                    <button
                        className="deleteBtn"
                        onClick={() => deleteProfile()}
                        >Delete</button>
                    <div>{updateError}</div>
                </div>
                <div className="formBox profileBoxLeft">
                    <div id="connectionsDiv">
                        {
                            user["accepted_received"] ? user["accepted_received"].reverse().map(item => {
                                return <p className="commentP" key={uuid()}>
                                    <span>Current: 
                                        <span className="user_name"> {item.user_name}</span> / Id: <span className="user_id">{item.id}</span> 
                                    </span>
                                    
                                    <button
                                        className="disconnect"
                                        onClick={() => deleteConnection(id, item.id)}>Disconnect</button>
                                </p>
                            }) : null
                        }
                        {
                            user["accepted_sent"] ? user["accepted_sent"].reverse().map(item => {
                                return <p className="commentP" key={uuid()}>
                                    <span>Current: 
                                        <span className="user_name"> {item.user_name}</span> / Id: <span className="user_id">{item.id}</span> 
                                    </span>
                                    
                                    <button
                                        className="disconnect"
                                        onClick={() => deleteConnection(id, item.id)}>Disconnect</button>
                                </p>
                            }) : null
                        }
                        {
                            user["pending_received"] ? user["pending_received"].map(item => {
                               return item.id !== id ? (
                                     <p className="commentP" key={uuid()}>
                                    <span>From: 
                                        <span className="user_name"> {item.user_name}</span> / Id: <span className="user_id">{item.id}</span> 
                                    </span>
                                    
                                    <span className="commentBtns">
                                        <button
                                            className="accept"
                                            onClick={() => acceptConnection(id, item.id)}>Accept</button>
                                        
                                        <button
                                            className="disconnect"
                                            onClick={() => deleteConnectionRequestReceived(item.id, id)}>Refuse</button></span>
                                </p>
                                ) : null
                            }) : null
                        }
                        {
                            user["pending_sent"] ? user["pending_sent"].map(item => {
                                return item.id !== id ? (
                                    <p key={uuid()}>
                                        <span>Sent To: 
                                            <span className="user_name"> {item.user_name}</span> / Id: <span className="user_id">{item.id}</span>
                                        </span> 
                                        
                                        <button
                                            className="disconnect"
                                            onClick={() => deleteConnectionRequestSent(id, item.id)}>Withdraw</button>
                                    </p>
                               ) : null
                           }) : null
                        }
                    </div>
                    <Formik
                        initialValues={{
                            receiver_id: "",
                            reason: '',
                        }}
                        validationSchema={ConnectionSchema}
                        onSubmit={async (values) => {
                            values["sender_id"] = id;
                            fetch("/api/v1/user_connections", {
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
                                    setConnectionError(res.statusText);
                                }
                            })
                            .then(data => {
                                if (data.Message) {
                                    values.receiver_id = "";
                                    toast(data.Message);
                                    get_user(id)
                                } else {
                                    values.receiver_id = "";
                                    toast("Request Created")
                                    get_user(id)
                                }
                                
                            })
                            .catch(err => {
                                toast(err)
                            })
                        }}
                    >

                        {({ errors, touched }) => (
                            <Form
                                id="commentForm"
                                className="loginForm"
                            >
                                <div id="commentDiv">
                                    <Field
                                        id="receiver_id"
                                        name="receiver_id"
                                        placeholder="select a user by id to connect with"
                                        type="number"
                                        autoComplete="off"
                                        className="loginInput postDetailsCommentInput"
                                    />
                                    {errors.receiver_id && touched.receiver_id ? (
                                        <span> {errors.receiver_id}</span>
                                    ) : null}
                                </div>

                                <div>{connectionError}</div>

                                <button
                                    type="submit"
                                    className="submitBtn"
                                >Submit</button>  
                            </Form>
                        )}

                    </Formik>
                </div>
            </div>
        </div>
    )
};

export default Profile;