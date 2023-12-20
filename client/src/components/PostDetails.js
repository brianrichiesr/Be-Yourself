import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";
import { checkToken, postRefreshToken} from "./Authorize";
import { Formik, Field, Form } from 'formik';
import * as Yup from 'yup';
import { v4 as uuid } from 'uuid';

function PostDetails() {

    const [commentError, setCommentError] = useState("");

    const postObj = {
        comments: [],
        description: "",
        id: 0,
        image: "",
        post_author: {
            email: "",
            id: 0,
            user_name: ""
        },
        honoree: {
            email: "",
            id: 0,
            user_name: ""
        },
        status: "pending"
    }

    const [post, setPost] = useState(postObj)
    const { id } = useParams()
    const navigate = useNavigate()

    const get_post = () => {
        fetch(`/api/v1/posts/${id}`)
        .then(res => {
            if (res.ok) {
                return res.json()
            } else {
                throw (res.statusText)
            }
        })
        .then(data => setPost(data))
        .catch(err => {
            toast(err)
            navigate('/')
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
              get_post()
            })
            .catch(err => toast(err))
          }
        })
        .then(data => {
          if (data) {
            get_post()
          }
        })
        .catch(err => toast(err))
        
        }, [])
    
    const CommentSchema = Yup.object().shape({
        comment: Yup.string()
        .min(2, 'Too Short!')
        .max(100, "Too Long!!!")
        .required('Add a message!'),
    });

    return (
        <div className="formBackgroundDiv">
            <div id="post-details">
            <Toaster />
            <div className="postBox">
                <h2 className="postBoxH2">Post Details</h2>
                <div id="postCardBox" className="detailsCard">
                    <h2>Honoring: {post.honoree["user_name"]} / Id: {post.honoree["id"]}</h2>
                    <img src={post.image} alt="post image" />
                    <p>{post.description}</p>
                    <h3>Author: {post.post_author.user_name} / Id: {post.post_author.id}</h3>
                    <Formik
                        initialValues={{
                            comment: '',
                        }}
                        validationSchema={CommentSchema}
                        onSubmit={async (values) => {
                            const newObj = {...values}
                            newObj['post_id'] = post.id;
                            newObj['user_id'] = post.post_author.id;
                            fetch("/api/v1/comments", {
                                method: "POST",
                                headers: {
                                    "Content-Type": "application/json"
                                },
                                body: JSON.stringify(newObj)
                            })
                            .then(res => {
                                if (res.ok) {
                                    return res.json();
                                } else {
                                    toast(res.statusText);
                                }
                            })
                            .then(data => {
                                setPost(data);
                                toast("Comment Successfully Added!")
                                values.comment = "";
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
                                        id="comment"
                                        name="comment"
                                        placeholder="add a comment 100 characters max"
                                        type="comment"
                                        autoComplete="off"
                                        className="loginInput postDetailsCommentInput"
                                    />
                                    {errors.comment && touched.comment ? (
                                        <span> {errors.comment}</span>
                                    ) : null}
                                </div>

                                <div>{commentError}</div>

                                <button
                                    type="submit"
                                    className="submitBtn"
                                >Submit</button>  
                            </Form>
                        )}

                    </Formik>
                </div>
            </div>
            <div className="postBox">
                <h2 className="postBoxH2">Comments:</h2>
                <div className="commentBox">
                    {post.comments.map((item, idx) => {
                        return (
                            <div key={uuid()}>
                                <p>{item.comment}</p>
                                <p>Author: {item.user.user_name} / Id: {item.user.id}</p>
                                <hr />
                            </div>
                        )
                    })}
                </div>
                
            </div>
        </div>
        </div>
    );
}

export default PostDetails;