import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, useParams } from "react-router-dom";
import { useModal } from "../../context/Modal";
import { thunkGetVendors, thunkDeleteVendor } from "../../redux/vendors";
import VendorFormModal from "../VendorFormModal";
import ConfirmModal from "../ConfirmModal/ConfirmModal";
import "./VendorDetailsPage.css";

function VendorDetailsPage({ companyId }) {
    const { vendorId } = useParams();
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { setModalContent } = useModal();
    const vendor = useSelector((s) => s.vendors?.[Number(vendorId)]);

    useEffect(() => {
        if (!vendor && companyId) dispatch(thunkGetVendors(companyId));
    }, [dispatch, companyId, vendor]);

    const openEdit = () =>
        setModalContent(
            <VendorFormModal companyId={vendor?.company_id || companyId} vendor={vendor} />
        );

    const openAddNew = () =>
        setModalContent(
            <VendorFormModal companyId={vendor?.company_id || companyId} />
        );

    const openDelete = () => {
        setModalContent(
            <ConfirmModal
                onConfirm={async () => {
                    await dispatch(thunkDeleteVendor(vendor.id));
                    navigate("/vendors");
                }}
            />
        );
    };

    if (!vendor) return null;

    return (
        <div className="vendor-details">
            <div className="details-header">
                <h2>Vendor Details</h2>
                <div className="header-actions">
                    <button className="btn btn-danger" onClick={openDelete}>Delete Vendor</button>
                    <button className="btn btn-primary" onClick={openEdit}>Edit Vendor</button>
                    <button className="btn btn-primary" onClick={openAddNew}>Add New Vendor</button>
                </div>
            </div>

            <div className="details-grid">
                <div className="label">Vendor Name</div><div className="value">{vendor.name}</div>
                <div className="label">Contact Name</div><div className="value">{vendor.contact_name || "-"}</div>
                <div className="label">Email</div><div className="value">{vendor.email || "-"}</div>
                <div className="label">Phone</div><div className="value">{vendor.phone || "-"}</div>
                <div className="label">Tax ID</div><div className="value">{vendor.tax_id || "-"}</div>
                <div className="label">Address</div><div className="value">{vendor.street || "-"}</div>
                <div className="label">Payment Terms</div><div className="value">{vendor.payment_terms || "-"}</div>
                <div className="label">W-9 Document url</div>
                <div className="value">
                    {vendor.w9_document_url ? <a href={vendor.w9_document_url} target="_blank" rel="noreferrer">Click here</a> : "-"}
                </div>
                <div className="label">Balance</div>
                <div className="value">
                    {vendor.balance != null
                        ? Number(vendor.balance).toLocaleString("en-US", { style: "currency", currency: "USD" }) // Format as currency
                        : "-"}
                </div>
            </div>
        </div>
    );
}

export default VendorDetailsPage;
