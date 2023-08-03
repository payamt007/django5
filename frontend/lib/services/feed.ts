import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { paginatedFeedType } from '../types/paginated'
import { feedType } from '../types/feeds'

// Define a service using a base URL and expected endpoints
export const feedsApi = createApi({
  reducerPath: 'feedApi',
  baseQuery: fetchBaseQuery({ baseUrl: 'http://127.0.0.1:8000/api' }),
  endpoints: (build) => ({
    getAllFeeds: build.query<paginatedFeedType, void>({
      query: () => `feeds`,
    }),
    updatePost: build.mutation<void, Pick<feedType, 'title' | 'link'>>({
      // note: an optional `queryFn` may be used in place of `query`
      query: ({ ...patch }) => ({
        url: `feeds`,
        method: 'POST',
        body: patch,
      }),
      // Pick out data and prevent nested properties in a hook or selector
      transformResponse: (response: { data: Post }, meta, arg) => response.data,
      // Pick out errors and prevent nested properties in a hook or selector
      transformErrorResponse: (
        response: { status: string | number },
        meta,
        arg
      ) => response.status,
      invalidatesTags: ['feedType'],
      // onQueryStarted is useful for optimistic updates
      // The 2nd parameter is the destructured `MutationLifecycleApi`
      async onQueryStarted(
        arg,
        { dispatch, getState, queryFulfilled, requestId, extra, getCacheEntry }
      ) { },
      // The 2nd parameter is the destructured `MutationCacheLifecycleApi`
      async onCacheEntryAdded(
        arg,
        {
          dispatch,
          getState,
          extra,
          requestId,
          cacheEntryRemoved,
          cacheDataLoaded,
          getCacheEntry,
        }
      ) { },
    }),
  })
})


// Export hooks for usage in functional components, which are
// auto-generated based on the defined endpoints
export const { useGetAllFeedsQuery } = feedsApi