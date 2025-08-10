import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, useOutletContext } from "react-router-dom";
import { useModal } from "../../context/Modal";
import { thunkGetVendors, thunkDeleteVendor } from "../../redux/vendors";
import VendorFormModal from "../VendorFormModal/VendorFormModal";
import ConfirmModal from "../ConfirmModal/ConfirmModal";
import "./VendorsPage.css";

function VendorsPage() {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { setModalContent } = useModal();
    const { companyId } = useOutletContext(); // Retrieve companyId from the Outlet context
    const vendors = Object.values(useSelector((s) => s.vendors || {}));
    console.log('VendorsPage mounted:', { companyId, vendors });

    useEffect(() => {
        // Fetch vendors when the component mounts or companyId changes
        if (companyId) dispatch(thunkGetVendors(companyId));
    }, [dispatch, companyId]);

    const openCreate = () => {
        setModalContent(<VendorFormModal companyId={companyId} />);
    };

    const openEdit = (vendor) => {
        setModalContent(<VendorFormModal companyId={companyId} vendor={vendor} />);
    };

    const openDelete = (vendorId) => {
        setModalContent(
            <ConfirmModal
                message="Are you sure you want to proceed?"
                onConfirm={async () => {
                    await dispatch(thunkDeleteVendor(vendorId));
                }}
            />
        );
    };

    return (
        <div className="vendors-page">
            <div className="vendors-header">
                <h2>Vendors</h2>
                <button className="btn btn-primary" onClick={openCreate}>Add New Vendor</button>
            </div>

            <div className="vendors-table card">
                <div className="vendors-thead">
                    <div>Vendor Name</div>
                    <div>email</div>
                    <div>Balance</div>
                    <div className="actions-col" />
                </div>

                <div className="vendors-tbody">
                    {vendors.map((v) => (
                        <div className="vendors-row" key={v.id}>
                            <div>{v.name}</div>
                            <div>{v.email || "-"}</div>
                            <div>{v.balance != null ? Number(v.balance).toLocaleString("en-US", { style: "currency", currency: "USD" }) : "-"}</div>
                            <div className="row-actions">
                                <button className="btn btn-view" onClick={() => navigate(`/vendors/${v.id}`)}>View</button>
                                <button className="btn btn-edit" onClick={() => openEdit(v)}>Edit</button>
                                <button className="btn btn-danger" onClick={() => openDelete(v.id)}>Delete</button>
                            </div>
                        </div>
                    ))}
                    {vendors.length === 0 && (
                        <div className="vendors-empty">No vendors yet.</div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default VendorsPage;
