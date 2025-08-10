import { csrfFetch } from "../csrf";

// Action Types
const LOAD_APPROVERS = "approvers/load";
const ADD_APPROVER = "approvers/add";
const UPDATE_APPROVER = "approvers/update";
const DELETE_APPROVER = "approvers/delete";

// Action Creators
const loadApprovers = (approvers) => ({ type: LOAD_APPROVERS, approvers });
const addApprover = (approver) => ({ type: ADD_APPROVER, approver });
const updateApprover = (approver) => ({ type: UPDATE_APPROVER, approver });
const removeApprover = (approverId) => ({ type: DELETE_APPROVER, approverId });

// Thunks
export const thunkGetApprovers = (companyId) => async (dispatch) => {
  const res = await csrfFetch(`/api/companies/${companyId}/approvers`);
  if (res.ok) {
    const data = await res.json(); // { approvers: [...] }
    dispatch(loadApprovers(data.approvers));
  }
};

export const thunkCreateApprover =
  (companyId, formData) => async (dispatch) => {
    const res = await csrfFetch(`/api/companies/${companyId}/approvers`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });
    if (res.ok) {
      const data = await res.json();
      dispatch(addApprover(data));
      return data;
    }
  };

export const thunkUpdateApprover =
  (approverId, formData) => async (dispatch) => {
    const res = await csrfFetch(`/api/approvers/${approverId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });
    if (res.ok) {
      const data = await res.json();
      dispatch(updateApprover(data));
      return data;
    }
  };

export const thunkDeleteApprover = (approverId) => async (dispatch) => {
  const res = await csrfFetch(`/api/approvers/${approverId}`, {
    method: "DELETE",
  });
  if (res.ok) dispatch(removeApprover(approverId));
};

// Reducer
const initialState = {};
export default function approversReducer(state = initialState, action) {
  switch (action.type) {
    case LOAD_APPROVERS: {
      const next = {};
      action.approvers.forEach((a) => (next[a.id] = a));
      return next;
    }
    case ADD_APPROVER:
    case UPDATE_APPROVER:
      return { ...state, [action.approver.id]: action.approver };
    case DELETE_APPROVER: {
      const next = { ...state };
      delete next[action.approverId];
      return next;
    }
    default:
      return state;
  }
}
