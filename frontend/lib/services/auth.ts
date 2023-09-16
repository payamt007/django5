import { createSlice } from '@reduxjs/toolkit';

const authSlice = createSlice({
    name: 'auth',
    initialState: {
        redirectToLogin: false,
    },
    reducers: {
        redirectToLogin: (state) => {
            state.redirectToLogin = true;
        },
    },
});

export const { redirectToLogin } = authSlice.actions;
export default authSlice.reducer;