import { csrfFetch } from "../csrf";

// Action Types
const LOAD_BALANCES = "balances/load";
const ADD_BALANCE = "balances/add";
const UPDATE_BALANCE = "balances/update";
const DELETE_BALANCE = "balances/delete";

// Action Creators
const loadBalances = (balances) => ({ type: LOAD_BALANCES, balances });
const addBalance = (balance) => ({ type: ADD_BALANCE, balance });
const updateBalance = (balance) => ({ type: UPDATE_BALANCE, balance });
const removeBalance = (balanceId) => ({ type: DELETE_BALANCE, balanceId });

// Thunks
export const thunkGetBalances = (companyId) => async (dispatch) => {
  const res = await csrfFetch(`/api/companies/${companyId}/balances`);
  if (res.ok) {
    const data = await res.json(); // { balances: [...] }
    dispatch(loadBalances(data.balances));
  }
};

export const thunkCreateBalance = (companyId, formData) => async (dispatch) => {
  const res = await csrfFetch(`/api/companies/${companyId}/balances`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
  });
  if (res.ok) {
    const data = await res.json();
    dispatch(addBalance(data));
    return data;
  }
};

export const thunkUpdateBalance = (balanceId, formData) => async (dispatch) => {
  const res = await csrfFetch(`/api/balances/${balanceId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
  });
  if (res.ok) {
    const data = await res.json();
    dispatch(updateBalance(data));
    return data;
  }
};

export const thunkDeleteBalance = (balanceId) => async (dispatch) => {
  const res = await csrfFetch(`/api/balances/${balanceId}`, {
    method: "DELETE",
  });
  if (res.ok) dispatch(removeBalance(balanceId));
};

// Reducer
const initialState = {};
export default function bankBalancesReducer(state = initialState, action) {
  switch (action.type) {
    case LOAD_BALANCES: {
      const next = {};
      action.balances.forEach((b) => (next[b.id] = b));
      return next;
    }
    case ADD_BALANCE:
    case UPDATE_BALANCE:
      return { ...state, [action.balance.id]: action.balance };
    case DELETE_BALANCE: {
      const next = { ...state };
      delete next[action.balanceId];
      return next;
    }
    default:
      return state;
  }
}
