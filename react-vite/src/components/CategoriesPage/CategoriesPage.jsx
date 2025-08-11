import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, useOutletContext } from "react-router-dom";
import { useModal } from "../../context/Modal";
import { thunkGetCategories, thunkDeleteCategory } from "../../redux/categories";
import CategoryFormModal from "../CategoryFormModal";
import ConfirmModal from "../ConfirmModal/ConfirmModal";
import "./CategoriesPage.css";

export default function CategoriesPage() {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { setModalContent } = useModal();

    const outletCtx = useOutletContext(); // { companyId: 1 } returns the outlet context
    const companyId = Number(outletCtx?.companyId ?? 1); // guarantee number for companyId

    const categories = Object.values(useSelector((s) => s.categories || {}));

    useEffect(() => {
        dispatch(thunkGetCategories(companyId));
    }, [dispatch, companyId]);

    const openCreate = () =>
        setModalContent(<CategoryFormModal companyId={companyId} />);

    const openEdit = (category) =>
        setModalContent(<CategoryFormModal companyId={companyId} category={category} />);

    const openDelete = (id) =>
        setModalContent(
            <ConfirmModal onConfirm={async () => { await dispatch(thunkDeleteCategory(id)); }} />
        );

    const viewInvoices = (id) => navigate(`/categories/${id}/invoices`);

    return (
        <div className="categories-page">
            <div className="categories-header">
                <h2>Categories</h2>
                <button className="btn btn-primary" onClick={openCreate}>Add New Category</button>
            </div>

            <div className="categories-table card">
                <div className="categories-thead">
                    <div>Category Name</div>
                    <div className="actions-col" />
                </div>

                <div className="categories-tbody">
                    {categories.map((c) => (
                        <div className="categories-row" key={c.id}>
                            <div>{c.name}</div>
                            <div className="row-actions">
                                <button className="btn btn-dark" onClick={() => viewInvoices(c.id)}>View Invoices</button>
                                <button className="btn btn-primary" onClick={() => openEdit(c)}>Edit</button>
                                <button className="btn btn-danger" onClick={() => openDelete(c.id)}>Delete</button>
                            </div>
                        </div>
                    ))}
                    {categories.length === 0 && <div className="categories-empty">No categories yet.</div>}
                </div>
            </div>
        </div>
    );
}
