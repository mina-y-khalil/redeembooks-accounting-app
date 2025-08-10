import { csrfFetch } from "../csrf";

// Action Types
const LOAD_COMPANIES = "companies/load";
const ADD_COMPANY = "companies/add";
const UPDATE_COMPANY = "companies/update";
const DELETE_COMPANY = "companies/delete";

// Action Creators
const loadCompanies = (companies) => ({
  type: LOAD_COMPANIES,
  companies,
});

const addCompany = (company) => ({
  type: ADD_COMPANY,
  company,
});

const updateCompany = (company) => ({
  type: UPDATE_COMPANY,
  company,
});

const deleteCompany = (companyId) => ({
  type: DELETE_COMPANY,
  companyId,
});

// Thunks
export const thunkGetCompanies = () => async (dispatch) => {
  const res = await csrfFetch("/api/companies/");
  if (res.ok) {
    const data = await res.json();
    dispatch(loadCompanies(data.companies));
  }
};

export const thunkCreateCompany = (formData) => async (dispatch) => {
  const res = await csrfFetch("/api/companies/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
  });

  if (res.ok) {
    const data = await res.json();
    dispatch(addCompany(data));
    return data;
  }
};

export const thunkUpdateCompany = (companyId, formData) => async (dispatch) => {
  const res = await csrfFetch(`/api/companies/${companyId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
  });

  if (res.ok) {
    const data = await res.json();
    dispatch(updateCompany(data));
    return data;
  }
};

export const thunkDeleteCompany = (companyId) => async (dispatch) => {
  const res = await csrfFetch(`/api/companies/${companyId}`, {
    method: "DELETE",
  });

  if (res.ok) {
    dispatch(deleteCompany(companyId));
  }
};

// Reducer
const initialState = {};

export default function companiesReducer(state = initialState, action) {
  switch (action.type) {
    case LOAD_COMPANIES: {
      const newState = {};
      action.companies.forEach((company) => {
        newState[company.id] = company;
      });
      return newState;
    }
    case ADD_COMPANY:
    case UPDATE_COMPANY:
      return { ...state, [action.company.id]: action.company };
    case DELETE_COMPANY: {
      const newState = { ...state };
      delete newState[action.companyId];
      return newState;
    }
    default:
      return state;
  }
}
