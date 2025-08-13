import { useEffect, useMemo } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, useParams } from "react-router-dom";
import { useModal } from "../../context/Modal";
import { thunkGetVendors, thunkDeleteVendor } from "../../redux/vendors";
import { thunkGetInvoices, thunkDeleteInvoice } from "../../redux/invoices";
import VendorFormModal from "../VendorFormModal";
import InvoiceFormModal from "../InvoiceFormModal";
import ConfirmModal from "../ConfirmModal/ConfirmModal";
import "./VendorDetailsPage.css";
import "../InvoicesPage/InvoicesPage.css";

function StatusPill({ status }) {
    const map = {
        "Pending approval": "pill--pending",
        Approved: "pill--approved",
        Declined: "pill--declined",
        Denied: "pill--declined",
        Reject: "pill--declined",
    };
    const cls = map[status] || "pill--pending";
    return <span className={`status-pill ${cls}`}>{status}</span>;
}

function VendorDetailsPage({ companyId }) {
    const { vendorId } = useParams();
    const id = Number(vendorId);
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { setModalContent } = useModal();

    const vendorsById = useSelector((s) => s.vendors || {});
    const vendor = vendorsById[id];
    const invoicesById = useSelector((s) => s.invoices || {});
    const invoicesForVendor = useMemo(
        () => Object.values(invoicesById).filter((inv) => Number(inv.vendor_id) === id),
        [invoicesById, id]
    );

    useEffect(() => {
        if (companyId) {
            dispatch(thunkGetVendors(Number(companyId)));
            dispatch(thunkGetInvoices(Number(companyId)));
        }
    }, [dispatch, companyId]);

    const balance = useMemo(() => {
        let sum = 0;
        for (const inv of invoicesForVendor) {
            const include =
                inv.status === "Pending approval" ||
                inv.status === "Approved" ||
                !inv.status;
            if (!include) continue;
            sum += Number(inv.amount || 0);
        }
        return sum;
    }, [invoicesForVendor]);

    const openEditVendor = () =>
        setModalContent(<VendorFormModal companyId={vendor?.company_id || companyId} vendor={vendor} />);

    const openAddVendor = () =>
        setModalContent(<VendorFormModal companyId={vendor?.company_id || companyId} />);

    const openDeleteVendor = () =>
        setModalContent(
            <ConfirmModal
                onConfirm={async () => {
                    await dispatch(thunkDeleteVendor(vendor.id));
                    navigate("/vendors");
                }}
            />
        );

    const openCreateInvoice = () =>
        setModalContent(<InvoiceFormModal companyId={vendor?.company_id || companyId} />);

    const openEditInvoice = (invoice) =>
        setModalContent(<InvoiceFormModal companyId={vendor?.company_id || companyId} invoice={invoice} />);

    const openDeleteInvoice = (invoiceId) =>
        setModalContent(
            <ConfirmModal
                onConfirm={async () => {
                    await dispatch(thunkDeleteInvoice(invoiceId));
                    await dispatch(thunkGetInvoices(Number(vendor?.company_id || companyId)));
                }}
            />
        );

    if (!vendor) return null;

    return (
        <div className="vendor-details">
            <div className="details-header">
                <h2>Vendor Details</h2>
                <div className="header-actions">
                    <button className="btn btn-danger" onClick={openDeleteVendor}>Delete Vendor</button>
                    <button className="btn btn-primary" onClick={openEditVendor}>Edit Vendor</button>
                    <button className="btn btn-primary" onClick={openAddVendor}>Add New Vendor</button>
                </div>
            </div>

            <div className="details-grid">
                <div className="label">Vendor Name</div><div className="value">{vendor.name}</div>
                <div className="label">Contact Name</div><div className="value">{vendor.contact_name || "-"}</div>
                <div className="label">Email</div><div className="value">{vendor.email || "-"}</div>
                <div className="label">Phone</div><div className="value">{vendor.phone || "-"}</div>
                <div className="label">Tax ID</div><div className="value">{vendor.tax_id || "-"}</div>
                <div className="label">Address</div><div className="value">{vendor.street || "-"}</div>
                <div className="label">Payment Terms</div><div className="value">{vendor.payment_terms ?? "-"}</div>
                <div className="label">W-9 Document url</div>
                <div className="value">
                    {vendor.w9_document_url ? (
                        <a href={vendor.w9_document_url} target="_blank" rel="noreferrer">Click here</a>
                    ) : (
                        "-"
                    )}
                </div>
                <div className="label">Balance</div>
                <div className="value">
                    {Number.isFinite(balance)
                        ? balance.toLocaleString("en-US", { style: "currency", currency: "USD" })
                        : "-"}
                </div>
            </div>

            <div className="invoices-header" style={{ marginTop: 32 }}>
                <h2>Invoices for [{vendor.name}]</h2>
                <button className="btn btn-primary" onClick={openCreateInvoice}>Add New Invoice</button>
            </div>

            <div className="invoices-table card">
                <div className="invoices-thead">
                    <div>Invoice number</div>
                    <div>Vendor</div>
                    <div>Amount</div>
                    <div>Status</div>
                    <div className="actions-col" />
                </div>

                <div className="invoices-tbody">
                    {invoicesForVendor.map((inv) => (
                        <div key={inv.id} className="invoices-row">
                            <div>{inv.invoice_number}</div>
                            <div>{vendor.name}</div>
                            <div>
                                {inv.amount != null
                                    ? Number(inv.amount).toLocaleString("en-US", { style: "currency", currency: "USD" })
                                    : "-"}
                            </div>
                            <div><StatusPill status={inv.status || "Pending approval"} /></div>
                            <div className="row-actions">
                                <button className="btn btn-dark" onClick={() => navigate(`/invoices/${inv.id}`)}>View</button>
                                <button className="btn btn-primary" onClick={() => openEditInvoice(inv)}>Edit</button>
                                <button className="btn btn-danger" onClick={() => openDeleteInvoice(inv.id)}>Delete</button>
                            </div>
                        </div>
                    ))}
                    {invoicesForVendor.length === 0 && (
                        <div className="invoices-empty">No invoices for this vendor yet.</div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default VendorDetailsPage;
