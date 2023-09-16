/* Core */
import {createLogger} from 'redux-logger'
import {redirectToLogin} from "@/lib/services/auth"
import {ReduxStore} from "@/lib/redux/store";
import Action from '@reduxjs/toolkit'
import {ReduxThunkAction} from "@/lib/redux/store";
import {MiddlewareAPI, isRejectedWithValue, Middleware} from '@reduxjs/toolkit';
import {redirect} from 'next/navigation'

const middleware = [
    createLogger({
        duration: true,
        timestamp: false,
        collapsed: true,
        colors: {
            title: () => '#139BFE',
            prevState: () => '#1C5FAF',
            action: () => '#149945',
            nextState: () => '#A47104',
            error: () => '#ff0005',
        },
        predicate: () => typeof window !== 'undefined',
    }),
]

interface ActionType {
    type: string;
    payload: { status: number };
    meta: {};
    error: {};
}

const redirectToLoginMiddleware: Middleware = (_api: MiddlewareAPI) => (next: (action: ActionType) => unknown) => (action: ActionType) => {
    //if (isRejectedWithValue(action)) {
    if (action.payload.status === 403) {
        // Dispatch a logout action
        //store.dispatch(logout());

        // Redirect to the login page
        //redirect('/cosmak');
        console.log("caught 403")
    }
    // }
    return next(action);
};

export const rtkQueryErrorLogger: Middleware =
    (api: MiddlewareAPI) => (next) => (action) => {
        // RTK Query uses `createAsyncThunk` from redux-toolkit under the hood, so we're able to utilize these matchers!
        if (isRejectedWithValue(action)) {
            console.warn('We got a rejected action!')
            //redirect('/cosmak')
            //toast.warn({title: 'Async error!', message: action.error.data.message})
        }

        return next(action)
    }


export {middleware, redirectToLoginMiddleware}
