/* Instruments */
//import { counterSlice } from './slices'
import { feedsApi } from '../services/feed'

export const reducer = {
  [feedsApi.reducerPath]: feedsApi.reducer,
}
