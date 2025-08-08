import { csrfFetch } from "../csrf";

// Action Types
const LOAD_INVOICES = "invoices/load";
const ADD_INVOICE = "invoices/add";
const UPDATE_INVOICE = "invoices/update";
const DELETE_INVOICE = "invoices/delete";

// Action Creators
const loadInvoices = (invoices) => ({
  type: LOAD_INVOICES,
  invoices,
});

const addInvoice = (invoice) => ({
  type: ADD_INVOICE,
  invoice,
});

const updateInvoice = (invoice) => ({
  type: UPDATE_INVOICE,
  invoice,
});

const removeInvoice = (invoiceId) => ({
  type: DELETE_INVOICE,
  invoiceId,
});

// Thunks
export const thunkGetInvoices = (companyId) => async (dispatch) => {
  const res = await csrfFetch(`/api/companies/${companyId}/invoices`);
  if (res.ok) {
    const data = await res.json();
    // expecting { invoices: [...] }
    dispatch(loadInvoices(data.invoices));
  }
};

export const thunkGetInvoiceById = (invoiceId) => async (dispatch) => {
  const res = await csrfFetch(`/api/invoices/${invoiceId}`);
  if (res.ok) {
    const data = await res.json();
    dispatch(updateInvoice(data)); // Update the state with the fetched invoice
    return data;
  }
};

export const thunkCreateInvoice = (companyId, formData) => async (dispatch) => {
  const res = await csrfFetch(`/api/companies/${companyId}/invoices`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
  });

  if (res.ok) {
    const data = await res.json();
    dispatch(addInvoice(data));
    return data;
  }
};

export const thunkUpdateInvoice = (invoiceId, formData) => async (dispatch) => {
  const res = await csrfFetch(`/api/invoices/${invoiceId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
  });

  if (res.ok) {
    const data = await res.json();
    dispatch(updateInvoice(data));
    return data;
  }
};

export const thunkDeleteInvoice = (invoiceId) => async (dispatch) => {
  const res = await csrfFetch(`/api/invoices/${invoiceId}`, {
    method: "DELETE",
  });

  if (res.ok) {
    dispatch(removeInvoice(invoiceId));
  }
};

// Reducer
const initialState = {};

export default function invoicesReducer(state = initialState, action) {
  switch (action.type) {
    case LOAD_INVOICES: {
      const newState = {};
      action.invoices.forEach((inv) => {
        newState[inv.id] = inv;
      });
      return newState;
    }
    case ADD_INVOICE:
    case UPDATE_INVOICE:
      return { ...state, [action.invoice.id]: action.invoice };
    case DELETE_INVOICE: {
      const newState = { ...state };
      delete newState[action.invoiceId];
      return newState;
    }
    default:
      return state;
  }
}
