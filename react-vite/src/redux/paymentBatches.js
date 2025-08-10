import { csrfFetch } from "../csrf";

// Action Types
const LOAD_BATCHES = "batches/load";
const ADD_BATCH = "batches/add";
const UPDATE_BATCH = "batches/update";
const DELETE_BATCH = "batches/delete";

// Action Creators
const loadBatches = (batches) => ({
  type: LOAD_BATCHES,
  batches,
});

const addBatch = (batch) => ({
  type: ADD_BATCH,
  batch,
});

const updateBatch = (batch) => ({
  type: UPDATE_BATCH,
  batch,
});

const removeBatch = (batchId) => ({
  type: DELETE_BATCH,
  batchId,
});

// Thunks
export const thunkGetBatches = (companyId) => async (dispatch) => {
  const res = await csrfFetch(`/api/companies/${companyId}/batches`);
  if (res.ok) {
    const data = await res.json(); // { batches: [...] }
    dispatch(loadBatches(data.batches));
  }
};

export const thunkCreateBatch = (companyId, formData) => async (dispatch) => {
  const res = await csrfFetch(`/api/companies/${companyId}/batches`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
  });

  if (res.ok) {
    const data = await res.json();
    dispatch(addBatch(data));
    return data;
  }
};

export const thunkUpdateBatch = (batchId, formData) => async (dispatch) => {
  const res = await csrfFetch(`/api/batches/${batchId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
  });

  if (res.ok) {
    const data = await res.json();
    dispatch(updateBatch(data));
    return data;
  }
};

export const thunkDeleteBatch = (batchId) => async (dispatch) => {
  const res = await csrfFetch(`/api/batches/${batchId}`, {
    method: "DELETE",
  });

  if (res.ok) {
    dispatch(removeBatch(batchId));
  }
};

// Reducer
const initialState = {};

export default function paymentBatchesReducer(state = initialState, action) {
  switch (action.type) {
    case LOAD_BATCHES: {
      const newState = {};
      action.batches.forEach((b) => {
        newState[b.id] = b;
      });
      return newState;
    }
    case ADD_BATCH:
    case UPDATE_BATCH:
      return { ...state, [action.batch.id]: action.batch };
    case DELETE_BATCH: {
      const newState = { ...state };
      delete newState[action.batchId];
      return newState;
    }
    default:
      return state;
  }
}
