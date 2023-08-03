import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import {paginatedFeedType} from '../types/paginated'

// Define a service using a base URL and expected endpoints
export const feedsApi = createApi({
  reducerPath: 'feedApi',
  baseQuery: fetchBaseQuery({ baseUrl: 'http://127.0.0.1:8000/api' }),
  endpoints: (builder) => ({
    getAllFeeds: builder.query<paginatedFeedType, void>({
      query: () => `feeds`,
    }),
  }),
})

// Export hooks for usage in functional components, which are
// auto-generated based on the defined endpoints
export const { useGetAllFeedsQuery } = feedsApi