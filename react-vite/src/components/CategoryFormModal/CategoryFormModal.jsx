import { useEffect, useRef, useState } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { useModal } from "../../context/Modal";
import { thunkCreateCategory, thunkUpdateCategory } from "../../redux/categories";
import "./CategoryFormModal.css";

function CategoryFormModal({ companyId, category }) {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { closeModal } = useModal();
    const ref = useRef(null);

    const [name, setName] = useState(category?.name || "");
    const [errors, setErrors] = useState({});
    const [submitting, setSubmitting] = useState(false);

    useEffect(() => {
        const onDown = (e) => { if (ref.current && !ref.current.contains(e.target)) closeModal(); };
        document.addEventListener("mousedown", onDown);
        return () => document.removeEventListener("mousedown", onDown);
    }, [closeModal]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setErrors({});
        if (!name.trim()) { setErrors({ name: "Category name is required." }); return; }

        setSubmitting(true);
        const result = category
            ? await dispatch(thunkUpdateCategory(category.id, { name }))
            : await dispatch(thunkCreateCategory(Number(companyId), { name })); //number first
        setSubmitting(false);

        if (result?.errors) { setErrors(result.errors); return; }

        closeModal();
        navigate("/categories");
    };

    return (
        <div className="category-form-overlay">
            <form ref={ref} onSubmit={handleSubmit} className="category-form">
                <h2>{category ? "Edit Category" : "Add New Category"}</h2>

                {errors.auth && <p className="error top-error">{errors.auth}</p>}
                {errors.server && <p className="error top-error">{errors.server}</p>}

                <label>
                    Category Name
                    <input value={name} onChange={(e) => setName(e.target.value)} required />
                    {errors.name && <p className="error">{errors.name}</p>}
                </label>

                <button type="submit" className="btn-save" disabled={submitting}>
                    {submitting ? "Saving..." : "Save"}
                </button>
            </form>
        </div>
    );
}

export default CategoryFormModal;
