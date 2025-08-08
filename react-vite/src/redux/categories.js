import { csrfFetch } from "../csrf";

// Action Types
const LOAD_CATEGORIES = "categories/load";
const ADD_CATEGORY = "categories/add";
const UPDATE_CATEGORY = "categories/update";
const DELETE_CATEGORY = "categories/delete";

// Action Creators
const loadCategories = (categories) => ({
  type: LOAD_CATEGORIES,
  categories,
});

const addCategory = (category) => ({
  type: ADD_CATEGORY,
  category,
});

const updateCategory = (category) => ({
  type: UPDATE_CATEGORY,
  category,
});

const removeCategory = (categoryId) => ({
  type: DELETE_CATEGORY,
  categoryId,
});

// Thunks
export const thunkGetCategories = (companyId) => async (dispatch) => {
  const res = await csrfFetch(`/api/companies/${companyId}/categories`);
  if (res.ok) {
    const data = await res.json();
    // expecting { categories: [...] }
    dispatch(loadCategories(data.categories));
  }
};

export const thunkCreateCategory =
  (companyId, formData) => async (dispatch) => {
    const res = await csrfFetch(`/api/companies/${companyId}/categories`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    if (res.ok) {
      const data = await res.json();
      dispatch(addCategory(data));
      return data;
    }
  };

export const thunkUpdateCategory =
  (categoryId, formData) => async (dispatch) => {
    const res = await csrfFetch(`/api/categories/${categoryId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    if (res.ok) {
      const data = await res.json();
      dispatch(updateCategory(data));
      return data;
    }
  };

export const thunkDeleteCategory = (categoryId) => async (dispatch) => {
  const res = await csrfFetch(`/api/categories/${categoryId}`, {
    method: "DELETE",
  });

  if (res.ok) {
    dispatch(removeCategory(categoryId));
  }
};

// Reducer
const initialState = {};

export default function categoriesReducer(state = initialState, action) {
  switch (action.type) {
    case LOAD_CATEGORIES: {
      const newState = {};
      action.categories.forEach((cat) => {
        newState[cat.id] = cat;
      });
      return newState;
    }
    case ADD_CATEGORY:
    case UPDATE_CATEGORY:
      return { ...state, [action.category.id]: action.category };
    case DELETE_CATEGORY: {
      const newState = { ...state };
      delete newState[action.categoryId];
      return newState;
    }
    default:
      return state;
  }
}
