import { csrfFetch } from "../csrf";

// Action Types
const LOAD_VENDORS = "vendors/LOAD";
const ADD_VENDOR = "vendors/ADD";
const UPDATE_VENDOR = "vendors/UPDATE";
const DELETE_VENDOR = "vendors/DELETE";

// Action Creators
const loadVendors = (vendors) => ({
  type: LOAD_VENDORS,
  vendors,
});

const addVendor = (vendor) => ({
  type: ADD_VENDOR,
  vendor,
});

const updateVendor = (vendor) => ({
  type: UPDATE_VENDOR,
  vendor,
});

const removeVendor = (vendorId) => ({
  type: DELETE_VENDOR,
  vendorId,
});

// Thunks
export const thunkGetVendors = (companyId) => async (dispatch) => {
  const res = await csrfFetch(`/api/companies/${companyId}/vendors`);
  if (res.ok) {
    const data = await res.json();
    dispatch(loadVendors(data.vendors));
  }
};

export const thunkCreateVendor = (companyId, formData) => async (dispatch) => {
  const res = await csrfFetch(`/api/companies/${companyId}/vendors`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
  });

  if (res.ok) {
    const vendor = await res.json();
    dispatch(addVendor(vendor));
    return vendor;
  }
};

export const thunkUpdateVendor = (vendorId, formData) => async (dispatch) => {
  const res = await csrfFetch(`/api/vendors/${vendorId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
  });

  if (res.ok) {
    const vendor = await res.json();
    dispatch(updateVendor(vendor));
    return vendor;
  }
};

export const thunkDeleteVendor = (vendorId) => async (dispatch) => {
  const res = await csrfFetch(`/api/vendors/${vendorId}`, {
    method: "DELETE",
  });

  if (res.ok) {
    dispatch(removeVendor(vendorId));
  }
};

// Reducer
const vendorsReducer = (state = {}, action) => {
  switch (action.type) {
    case LOAD_VENDORS: {
      const newState = {};
      action.vendors.forEach((vendor) => {
        newState[vendor.id] = vendor;
      });
      return newState;
    }
    case ADD_VENDOR:
    case UPDATE_VENDOR:
      return { ...state, [action.vendor.id]: action.vendor };
    case DELETE_VENDOR: {
      const newState = { ...state };
      delete newState[action.vendorId];
      return newState;
    }
    default:
      return state;
  }
};

export default vendorsReducer;
