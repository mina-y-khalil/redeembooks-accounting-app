import { csrfFetch } from "../csrf";

// Action Types
const LOAD_AUDIT_LOGS = "auditLogs/load";

// Action Creators
const loadAuditLogs = (logs) => ({
  type: LOAD_AUDIT_LOGS,
  logs,
});

// Thunks (read-only)
export const thunkGetAuditLogs = (companyId) => async (dispatch) => {
  const res = await csrfFetch(`/api/companies/${companyId}/audit-logs`);
  if (res.ok) {
    const data = await res.json(); // { audit_logs: [...] }
    dispatch(loadAuditLogs(data.audit_logs));
  }
};

// Reducer
const initialState = {};
export default function auditLogsReducer(state = initialState, action) {
  switch (action.type) {
    case LOAD_AUDIT_LOGS: {
      const next = {};
      action.logs.forEach((log) => {
        next[log.id] = log;
      });
      return next;
    }
    default:
      return state;
  }
}
